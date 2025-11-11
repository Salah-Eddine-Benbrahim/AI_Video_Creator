"""Video generation helpers."""
from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Iterable

import imageio.v2 as imageio
import numpy as np
from PIL import Image

from .providers import ImageProvider, PollinationsImageProvider


class VideoGenerationError(RuntimeError):
    """Raised when the video generation workflow fails."""


def _prompt_variants(prompt: str, count: int) -> Iterable[str]:
    for index in range(count):
        if index == 0:
            yield prompt
        else:
            yield f"{prompt}, cinematic frame {index + 1}"


def generate_video(
    prompt: str,
    output_path: Path,
    frame_count: int,
    fps: int,
    provider: ImageProvider | None = None,
) -> Path:
    """Generate a simple slideshow video for ``prompt``."""

    provider = provider or PollinationsImageProvider()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    frames: list[np.ndarray] = []
    for variant in _prompt_variants(prompt, frame_count):
        try:
            image_bytes = provider.fetch_image(variant)
        except Exception as exc:  # pragma: no cover - provider specific
            raise VideoGenerationError("Failed to fetch frame from provider") from exc

        with Image.open(BytesIO(image_bytes)) as image:
            frame = image.convert("RGB")
            frames.append(np.array(frame))

    try:
        with imageio.get_writer(output_path, fps=fps, codec="libx264") as writer:
            for frame in frames:
                writer.append_data(frame)
    except ModuleNotFoundError as exc:  # pragma: no cover - environment specific
        raise VideoGenerationError(
            "Failed to encode video: missing imageio-ffmpeg dependency"
        ) from exc
    except Exception as exc:  # pragma: no cover - thin wrapper
        error_message = "Failed to encode video"
        if "ffmpeg" in str(exc).lower():
            error_message += "; ensure ffmpeg is installed and accessible"
        raise VideoGenerationError(error_message) from exc

    return output_path
