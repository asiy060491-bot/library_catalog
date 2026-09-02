"""
Dependency Injection контейнер для API.

Содержит фабрики для создания сервисов.
Использует FastAPI Depends для внедрения зависимостей.
"""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from ..core.config import settings
from ..domain.services.book_service import BookService
from ..external.openlibrary import OpenLibraryClient


# ========== EXTERNAL CLIENTS (Singletons) ==========

@lru_cache(maxsize=1)
def get_openlibrary_client() -> OpenLibraryClient:
    """
    Получить singleton OpenLibraryClient.

    lru_cache создает клиент один раз и переиспользует его
    для всех последующих запросов.

    Returns:
        OpenLibraryClient: Экземпляр клиента Open Library
    """
    return OpenLibraryClient(
        base_url=settings.openlibrary_base_url,
        timeout=settings.openlibrary_timeout,
        retries=settings.openlibrary_retries,
    )


# ========== REPOSITORIES ==========

# TODO: Будет добавлено в задании с БД
# async def get_book_repository(...)


# ========== SERVICES ==========

async def get_book_service(
        ol_client: Annotated[OpenLibraryClient, Depends(get_openlibrary_client)],
) -> BookService:
    """
    Создать BookService с внедренными зависимостями.

    Args:
        ol_client: Клиент Open Library

    Returns:
        BookService: Экземпляр сервиса книг
    """
    # TODO: Добавить book_repository когда будет готова БД
    return BookService(
        book_repository=None,  # Временно None
        openlibrary_client=ol_client,
    )


# ========== TYPE ALIASES ДЛЯ УДОБСТВА ==========

BookServiceDep = Annotated[BookService, Depends(get_book_service)]
OpenLibraryClientDep = Annotated[OpenLibraryClient, Depends(get_openlibrary_client)]