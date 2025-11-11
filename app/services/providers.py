"""Provider abstractions for generating media using third-party services."""
from __future__ import annotations

import base64
import sys
from abc import ABC, abstractmethod
from typing import Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen


class ImageProvider(ABC):
    """Abstract base class for image providers."""

    @abstractmethod
    def fetch_image(self, prompt: str) -> bytes:
        """Return the raw bytes for an image that represents ``prompt``."""


class PollinationsImageProvider(ImageProvider):
    """Fetch images from the public pollinations.ai endpoint."""

    base_url: str = "https://image.pollinations.ai/prompt/"
    _fallback_placeholder: bytes = base64.b64decode(
        (
            "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDABALChAYKDM9DAwOExo6PDcODRAYKDlFOA4RFh0zV1A+"
            "EhYlOERtZ00YIzdAUWhxXDFATldneXhlSFxfYnBkZ2P/wAALCAAIAAgBAREA/8QAEwABAAAAAAAAAAAA"
            "AAAAAAAAAP/EABMQAQAAAAAAAAAAAAAAAAAAAAD/2gAIAQEAAD8AP//Z"
        )
    )
    _warned_about_fallback: bool = False

    def __init__(self, timeout: int = 90) -> None:
        self._timeout = timeout

    def fetch_image(self, prompt: str) -> bytes:
        encoded_prompt = quote_plus(prompt)
        request = Request(
            f"{self.base_url}{encoded_prompt}",
            headers={"User-Agent": "ai-video-creator/1.0"},
        )
        try:
            with urlopen(request, timeout=self._timeout) as response:  # noqa: S310
                data = response.read()
        except (HTTPError, URLError) as exc:  # pragma: no cover - network issues
            return self._handle_failure(
                f"network error: {exc}",
            )

        if not data.startswith(b"\xFF\xD8"):
            return self._handle_failure("provider returned non-JPEG payload")

        return data

    def _handle_failure(self, message: str) -> bytes:
        if not self.__class__._warned_about_fallback:
            print(
                "Warning: pollinations.ai unavailable ("
                f"{message}). Using placeholder artwork instead.",
                file=sys.stderr,
            )
            self.__class__._warned_about_fallback = True
        return self._fallback_placeholder


class ImageWriter(Protocol):
    """Callable protocol used for writing image bytes to a destination."""

    def __call__(self, data: bytes) -> None:
        ...


def save_image_bytes(image_bytes: bytes, writer: ImageWriter) -> None:
    """Save ``image_bytes`` using the provided ``writer`` callable."""

    writer(image_bytes)
