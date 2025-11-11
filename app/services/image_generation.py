"""Image generation helpers."""
from __future__ import annotations

from pathlib import Path

from .providers import ImageProvider, PollinationsImageProvider, save_image_bytes


class ImageGenerationError(RuntimeError):
    """Raised when the image generation workflow fails."""


def generate_image(
    prompt: str,
    output_path: Path,
    provider: ImageProvider | None = None,
) -> Path:
    """Generate a single image for ``prompt`` and store it at ``output_path``."""

    provider = provider or PollinationsImageProvider()

    try:
        image_bytes = provider.fetch_image(prompt)
    except Exception as exc:  # pragma: no cover - thin wrapper around provider
        raise ImageGenerationError("Failed to fetch image from provider") from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_image_bytes(image_bytes, output_path.write_bytes)
    return output_path
