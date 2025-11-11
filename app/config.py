"""Configuration helpers for the AI media generator application."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class VideoSettings:
    """Settings that drive video generation."""

    frame_count: int = 6
    fps: int = 4

    def validate(self) -> None:
        if self.frame_count <= 0:
            raise ValueError("frame_count must be greater than zero")
        if self.fps <= 0:
            raise ValueError("fps must be greater than zero")


@dataclass
class OutputSettings:
    """Settings that describe common output behaviour."""

    output_path: Path


@dataclass
class AppSettings:
    """Aggregate settings for the CLI."""

    prompt: str
    mode: str
    output: OutputSettings
    video: VideoSettings | None = None

    def validate(self) -> None:
        if not self.prompt.strip():
            raise ValueError("prompt must not be empty")
        if self.mode not in {"image", "video"}:
            raise ValueError("mode must be either 'image' or 'video'")
        if self.video is not None:
            self.video.validate()
