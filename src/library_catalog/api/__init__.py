"""
API слой приложения.

Содержит роутеры, схемы и DI контейнер.
"""

from .v1 import router
from .dependencies import (
    get_book_service,
    get_book_repository,
    get_openlibrary_client,
    BookServiceDep,
    BookRepoDep,
    DbSessionDep,
    OpenLibraryClientDep,
)

__all__ = [
    "router",
    "get_book_service",
    "get_book_repository",
    "get_openlibrary_client",
    "BookServiceDep",
    "BookRepoDep",
    "DbSessionDep",
    "OpenLibraryClientDep",
]