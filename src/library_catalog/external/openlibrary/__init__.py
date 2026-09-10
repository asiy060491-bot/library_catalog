"""
Модуль для работы с Open Library API.
"""

from .client import OpenLibraryClient
from .schemas import OpenLibrarySearchDoc, OpenLibrarySearchResponse

__all__ = [
    "OpenLibraryClient",
    "OpenLibrarySearchDoc",
    "OpenLibrarySearchResponse",
]