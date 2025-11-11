"""Provider abstractions for generating media using third-party services."""
from __future__ import annotations

from abc import ABC, abstractmethod
from io import BytesIO
from typing import Protocol
from urllib.parse import quote_plus

import requests


class ImageProvider(ABC):
    """Abstract base class for image providers."""

    @abstractmethod
    def fetch_image(self, prompt: str) -> bytes:
        """Return the raw bytes for an image that represents ``prompt``."""


class PollinationsImageProvider(ImageProvider):
    """Fetch images from the public pollinations.ai endpoint."""

    base_url: str = "https://image.pollinations.ai/prompt/"

    def __init__(self, session: requests.Session | None = None) -> None:
        self._session = session or requests.Session()

    def fetch_image(self, prompt: str) -> bytes:
        encoded_prompt = quote_plus(prompt)
        response = self._session.get(f"{self.base_url}{encoded_prompt}", timeout=90)
        response.raise_for_status()
        return response.content


class ImageWriter(Protocol):
    """Callable protocol used for writing image bytes to a destination."""

    def __call__(self, data: bytes) -> None:
        ...


def save_image_bytes(image_bytes: bytes, writer: ImageWriter) -> None:
    """Save ``image_bytes`` using the provided ``writer`` callable."""

    buffer = BytesIO(image_bytes)
    writer(buffer.read())
