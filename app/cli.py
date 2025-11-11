"""Command line interface for the AI media generator application."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import AppSettings, OutputSettings, VideoSettings
from .services.image_generation import ImageGenerationError, generate_image
from .services.video_generation import VideoGenerationError, generate_video


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate an AI-powered photo or slideshow video from a prompt.",
    )
    parser.add_argument("--prompt", required=True, help="Text prompt to send to the generator")
    parser.add_argument(
        "--mode",
        choices=["image", "video"],
        default="image",
        help="Type of media to generate",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output path for the generated media (e.g. result.jpg or result.avi)",
    )
    parser.add_argument(
        "--frame-count",
        type=int,
        default=6,
        help="Number of AI-generated frames to include in video mode",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=4,
        help="Frames per second for the resulting video",
    )
    return parser


def _validate_settings(args: argparse.Namespace) -> AppSettings:
    output_settings = OutputSettings(output_path=Path(args.output))
    video_settings = None
    if args.mode == "video":
        video_settings = VideoSettings(frame_count=args.frame_count, fps=args.fps)

    settings = AppSettings(
        prompt=args.prompt,
        mode=args.mode,
        output=output_settings,
        video=video_settings,
    )
    settings.validate()
    return settings


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        settings = _validate_settings(args)
    except ValueError as exc:
        parser.error(str(exc))

    if settings.mode == "image":
        try:
            generate_image(settings.prompt, settings.output.output_path)
        except ImageGenerationError as exc:
            parser.error(str(exc))
    else:
        assert settings.video is not None  # for mypy/static typing
        try:
            generate_video(
                settings.prompt,
                settings.output.output_path,
                frame_count=settings.video.frame_count,
                fps=settings.video.fps,
            )
        except VideoGenerationError as exc:
            parser.error(str(exc))

    print(f"Saved {settings.mode} to {settings.output.output_path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
