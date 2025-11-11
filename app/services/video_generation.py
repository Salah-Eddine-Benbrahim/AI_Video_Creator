"""Video generation helpers."""
from __future__ import annotations

import struct
from pathlib import Path
from typing import Iterable

from .providers import ImageProvider, PollinationsImageProvider


class VideoGenerationError(RuntimeError):
    """Raised when the video generation workflow fails."""


def _prompt_variants(prompt: str, count: int) -> Iterable[str]:
    for index in range(count):
        if index == 0:
            yield prompt
        else:
            yield f"{prompt}, cinematic frame {index + 1}"


def _parse_jpeg_dimensions(image_bytes: bytes) -> tuple[int, int]:
    """Return (width, height) by scanning the JPEG markers."""

    index = 0
    length = len(image_bytes)

    if length < 4 or image_bytes[0:2] != b"\xFF\xD8":
        raise VideoGenerationError("Unsupported image format for slideshow frames")

    index = 2
    while index + 3 < length:
        if image_bytes[index] != 0xFF:
            index += 1
            continue
        marker = image_bytes[index + 1]
        if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
            segment_length = int.from_bytes(image_bytes[index + 2 : index + 4], "big")
            height = int.from_bytes(image_bytes[index + 5 : index + 7], "big")
            width = int.from_bytes(image_bytes[index + 7 : index + 9], "big")
            return width, height
        elif marker == 0xDA:  # SOS - start of scan
            break
        else:
            segment_length = int.from_bytes(image_bytes[index + 2 : index + 4], "big")
            if segment_length <= 0:
                break
            index += 2 + segment_length
    raise VideoGenerationError("Failed to determine frame dimensions from JPEG data")


def _riff_chunk(fourcc: bytes, data: bytes) -> bytes:
    return fourcc + struct.pack("<I", len(data)) + data + (b"\x00" if len(data) % 2 else b"")


def _list_chunk(fourcc: bytes, data: bytes) -> bytes:
    payload = fourcc + data
    size = struct.pack("<I", len(payload))
    chunk = b"LIST" + size + payload
    if len(payload) % 2:
        chunk += b"\x00"
    return chunk


def _build_mjpeg_avi(frames: list[bytes], fps: int) -> bytes:
    if not frames:
        raise VideoGenerationError("No frames available for video generation")

    width, height = _parse_jpeg_dimensions(frames[0])
    max_frame_size = max(len(frame) for frame in frames)
    frame_count = len(frames)
    microsec_per_frame = int(1_000_000 / max(fps, 1))
    max_bytes_per_sec = max_frame_size * max(fps, 1)

    avih = struct.pack(
        "<IIIIIIIIII4I",
        microsec_per_frame,
        max_bytes_per_sec,
        0,
        0x10,  # AVIF_HASINDEX
        frame_count,
        0,
        1,
        max_frame_size,
        width,
        height,
        0,
        0,
        0,
        0,
    )
    avih_chunk = _riff_chunk(b"avih", avih)

    strh = struct.pack(
        "<4s4sIHHIIIIIIIIhhhh",
        b"vids",
        b"MJPG",
        0,
        0,
        0,
        0,
        1,
        fps,
        0,
        frame_count,
        max_frame_size,
        0xFFFFFFFF,
        0,
        0,
        0,
        width,
        height,
    )
    strh_chunk = _riff_chunk(b"strh", strh)

    strf = struct.pack(
        "<IiiHHIIIIII",
        40,
        width,
        height,
        1,
        24,
        0x47504A4D,  # 'MJPG'
        max_frame_size,
        0,
        0,
        0,
        0,
    )
    strf_chunk = _riff_chunk(b"strf", strf)

    strl_list = _list_chunk(b"strl", strh_chunk + strf_chunk)
    hdrl_list = _list_chunk(b"hdrl", avih_chunk + strl_list)

    movi_data = bytearray()
    idx_entries = bytearray()
    offset = 4  # account for 'movi'

    for frame in frames:
        chunk_id = b"00db"
        size = len(frame)
        chunk_header = chunk_id + struct.pack("<I", size)
        movi_data.extend(chunk_header)
        movi_data.extend(frame)
        if size % 2:
            movi_data.extend(b"\x00")
        idx_entries.extend(chunk_id)
        idx_entries.extend(struct.pack("<I", 0x10))  # keyframe flag
        idx_entries.extend(struct.pack("<I", offset))
        idx_entries.extend(struct.pack("<I", size))
        offset += len(chunk_header) + size + (size % 2)

    movi_list = _list_chunk(b"movi", bytes(movi_data))
    idx1_chunk = _riff_chunk(b"idx1", bytes(idx_entries))

    riff_size = 4 + len(hdrl_list) + len(movi_list) + len(idx1_chunk)
    riff_header = b"RIFF" + struct.pack("<I", riff_size) + b"AVI "

    return riff_header + hdrl_list + movi_list + idx1_chunk


def generate_video(
    prompt: str,
    output_path: Path,
    frame_count: int,
    fps: int,
    provider: ImageProvider | None = None,
) -> Path:
    """Generate a simple MJPEG slideshow video for ``prompt``."""

    provider = provider or PollinationsImageProvider()
    frames: list[bytes] = []

    for variant in _prompt_variants(prompt, frame_count):
        try:
            image_bytes = provider.fetch_image(variant)
        except Exception as exc:  # pragma: no cover - provider specific
            raise VideoGenerationError(
                f"Failed to fetch frame from provider: {exc}"
            ) from exc
        frames.append(image_bytes)

    avi_bytes = _build_mjpeg_avi(frames, fps)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(avi_bytes)
    return output_path
