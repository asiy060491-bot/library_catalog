"""
Клиент для работы с Open Library API.

Предоставляет методы для поиска книг по ISBN, названию и автору.
"""

import logging
from typing import Optional, Dict, Any, List
import httpx

from ..base.base_client import BaseApiClient
from ...domain.exceptions import (
    OpenLibraryException,
    OpenLibraryTimeoutException,
)
from .schemas import OpenLibrarySearchResponse, OpenLibrarySearchDoc

logger = logging.getLogger(__name__)


class OpenLibraryClient(BaseApiClient):
    """
    Клиент для Open Library API.

    Предоставляет методы для:
    - Поиска книг по ISBN
    - Поиска книг по названию и автору
    - Обогащения данных книги
    - Извлечения обложек, тем, описаний

    Examples:
        >>> client = OpenLibraryClient()
        >>> data = await client.search_by_isbn("9780132350884")
        >>> print(data['title'])
        "Clean Code"
    """

    def __init__(
            self,
            base_url: str = "https://openlibrary.org",
            timeout: float = 10.0,
            retries: int = 3,
            backoff: float = 0.5,
    ):
        """
        Инициализация клиента Open Library.

        Args:
            base_url: Базовый URL API
            timeout: Таймаут запроса в секундах
            retries: Количество попыток при ошибке
            backoff: Начальная задержка между попытками
        """
        super().__init__(
            base_url=base_url,
            timeout=timeout,
            retries=retries,
            backoff=backoff,
        )
        self.logger = logging.getLogger(f"{self.client_name()}.client")

    def client_name(self) -> str:
        """Имя клиента для логирования."""
        return "openlibrary"

    async def search_by_isbn(self, isbn: str) -> Dict[str, Any]:
        """
        Поиск книги по ISBN.

        Args:
            isbn: ISBN-10 или ISBN-13

        Returns:
            dict: Данные книги (cover_url, subjects, etc.)

        Raises:
            OpenLibraryException: При ошибке API
            OpenLibraryTimeoutException: При таймауте

        Examples:
            >>> client = OpenLibraryClient()
            >>> data = await client.search_by_isbn("9780132350884")
            >>> print(data.get('title'))
            "Clean Code"
        """
        self.logger.info(f"Searching book by ISBN: {isbn}")

        try:
            data = await self._get(
                "/search.json",
                params={"isbn": isbn, "limit": 1}
            )

            # Парсим ответ с помощью Pydantic
            response = OpenLibrarySearchResponse(**data)

            if not response.docs:
                self.logger.warning(f"No book found for ISBN: {isbn}")
                return {}

            # Извлекаем данные из первого документа
            result = self._extract_book_data(response.docs[0])
            result["isbn"] = isbn

            self.logger.info(f"Found book: {result.get('title', 'Unknown')}")
            return result

        except httpx.TimeoutException as e:
            self.logger.error(f"Timeout while searching by ISBN {isbn}: {e}")
            raise OpenLibraryTimeoutException(self.timeout)

        except httpx.HTTPError as e:
            self.logger.error(f"HTTP error while searching by ISBN {isbn}: {e}")
            raise OpenLibraryException(f"Failed to search by ISBN: {str(e)}")

        except Exception as e:
            self.logger.error(f"Unexpected error while searching by ISBN {isbn}: {e}")
            raise OpenLibraryException(f"Unexpected error: {str(e)}")

    async def search_by_title_author(
            self,
            title: str,
            author: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Поиск книги по названию и автору.

        Args:
            title: Название книги
            author: Имя автора (опционально)

        Returns:
            dict: Данные книги

        Raises:
            OpenLibraryException: При ошибке API
            OpenLibraryTimeoutException: При таймауте

        Examples:
            >>> client = OpenLibraryClient()
            >>> data = await client.search_by_title_author(
            ...     "Clean Code",
            ...     "Robert Martin"
            ... )
            >>> print(data.get('title'))
            "Clean Code"
        """
        self.logger.info(f"Searching book by title: '{title}', author: '{author}'")

        try:
            params = {"title": title, "limit": 1}
            if author:
                params["author"] = author

            data = await self._get("/search.json", params=params)

            # Парсим ответ с помощью Pydantic
            response = OpenLibrarySearchResponse(**data)

            if not response.docs:
                self.logger.warning(f"No book found for title: {title}, author: {author}")
                return {}

            # Извлекаем данные из первого документа
            result = self._extract_book_data(response.docs[0])

            self.logger.info(f"Found book: {result.get('title', 'Unknown')}")
            return result

        except httpx.TimeoutException as e:
            self.logger.error(f"Timeout while searching by title: {e}")
            raise OpenLibraryTimeoutException(self.timeout)

        except httpx.HTTPError as e:
            self.logger.error(f"HTTP error while searching by title: {e}")
            raise OpenLibraryException(f"Failed to search by title: {str(e)}")

        except Exception as e:
            self.logger.error(f"Unexpected error while searching by title: {e}")
            raise OpenLibraryException(f"Unexpected error: {str(e)}")

    async def enrich(
            self,
            title: str,
            author: Optional[str] = None,
            isbn: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Обогатить данные книги.

        Стратегия поиска:
        1. Если указан ISBN → поиск по ISBN
        2. Если не найден или нет ISBN → поиск по названию и автору
        3. Возвращает словарь с обогащенными данными или пустой словарь

        Args:
            title: Название книги
            author: Имя автора (опционально)
            isbn: ISBN (опционально)

        Returns:
            dict: Обогащенные данные или пустой словарь

        Examples:
            >>> client = OpenLibraryClient()
            >>> data = await client.enrich(
            ...     title="Clean Code",
            ...     author="Robert Martin",
            ...     isbn="9780132350884"
            ... )
            >>> print(data.get('subjects', []))
            ["Programming", "Software Engineering"]
        """
        self.logger.info(f"Enriching book data: '{title}' by '{author}' (ISBN: {isbn})")

        # Попытка 1: По ISBN (если указан)
        if isbn:
            self.logger.debug(f"Attempting to find by ISBN: {isbn}")
            result = await self.search_by_isbn(isbn)
            if result:
                self.logger.info(f"Book enriched by ISBN: {isbn}")
                return result

        # Попытка 2: По названию и автору
        if title:
            self.logger.debug(f"Attempting to find by title and author: '{title}' '{author}'")
            result = await self.search_by_title_author(title, author)
            if result:
                self.logger.info(f"Book enriched by title: '{title}'")
                return result

        self.logger.warning(f"Could not enrich book: '{title}' by '{author}' (ISBN: {isbn})")
        return {}

    def _extract_book_data(self, doc: OpenLibrarySearchDoc) -> Dict[str, Any]:
        """
        Извлечь нужные поля из документа Open Library.

        Args:
            doc: Документ из массива docs (Pydantic модель)

        Returns:
            dict: Обработанные данные книги
        """
        result = {
            "title": doc.title,
            "author": doc.author_name[0] if doc.author_name else None,
            "authors": doc.author_name or [],
        }

        # Cover URL (обложка)
        if doc.cover_i:
            result["cover_url"] = self._get_cover_url(doc.cover_i)
            result["cover_id"] = doc.cover_i

        # Subjects (темы/категории)
        if doc.subject:
            result["subjects"] = doc.subject[:10]  # Ограничиваем 10 темами

        # Publisher (издатель)
        if doc.publisher:
            result["publisher"] = doc.publisher[0] if doc.publisher else None
            result["publishers"] = doc.publisher

        # Language (язык)
        if doc.language:
            result["language"] = doc.language[0] if doc.language else None
            result["languages"] = doc.language

        # Ratings (рейтинг)
        if doc.ratings_average is not None:
            result["rating"] = doc.ratings_average

        # Additional fields
        if doc.first_publish_year:
            result["first_publish_year"] = doc.first_publish_year

        if doc.number_of_pages_median:
            result["pages"] = doc.number_of_pages_median

        if doc.isbn:
            result["isbns"] = doc.isbn

        if doc.key:
            result["key"] = doc.key

        return result

    def _get_cover_url(self, cover_id: int) -> str:
        """
        Получить URL обложки книги.

        Args:
            cover_id: ID обложки в Open Library

        Returns:
            str: URL обложки (крупный размер)
        """
        return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"