"""
External интеграции.

Содержит клиенты для внешних API и сервисов.
"""

from .openlibrary import OpenLibraryClient, OpenLibrarySearchDoc, OpenLibrarySearchResponse
from .base import BaseApiClient

__all__ = [
    "OpenLibraryClient",
    "OpenLibrarySearchDoc",
    "OpenLibrarySearchResponse",
    "BaseApiClient",
]