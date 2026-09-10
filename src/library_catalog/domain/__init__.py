"""
Domain слой с бизнес-логикой.

Содержит:
- Доменные исключения (exceptions)
- Сервисы (services)
- Мапперы (mappers)
"""

from .exceptions import (
    BookNotFoundException,
    BookAlreadyExistsException,
    InvalidYearException,
    InvalidPagesException,
    OpenLibraryException,
    OpenLibraryTimeoutException,
)
from .services import BookService
from .mappers import BookMapper

__all__ = [
    # Exceptions
    "BookNotFoundException",
    "BookAlreadyExistsException",
    "InvalidYearException",
    "InvalidPagesException",
    "OpenLibraryException",
    "OpenLibraryTimeoutException",
    # Services
    "BookService",
    # Mappers
    "BookMapper",
]