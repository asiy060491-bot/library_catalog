"""
Модуль доменных исключений для библиотечного каталога.

Содержит специфичные для предметной области исключения,
наследующиеся от базовых исключений из core.exceptions.
"""

from uuid import UUID
from datetime import datetime
from ..core.exceptions import AppException, NotFoundException


# === Базовые исключения для книг ===

class BookNotFoundException(NotFoundException):
    """
    Исключение: книга не найдена в каталоге.
    
    Возникает при попытке получить, обновить или удалить книгу,
    которая отсутствует в базе данных.
    """
    def __init__(self, book_id: UUID):
        """
        Инициализация исключения.
        
        Args:
            book_id: UUID книги, которая не была найдена
        """
        super().__init__(resource="Book", identifier=book_id)


class BookAlreadyExistsException(AppException):
    """
    Исключение: книга с таким ISBN уже существует.
    
    Возникает при попытке создать книгу с ISBN, который уже
    зарегистрирован в каталоге.
    """
    def __init__(self, isbn: str):
        """
        Инициализация исключения.
        
        Args:
            isbn: ISBN книги, которая уже существует
        """
        super().__init__(
            message=f"Book with ISBN '{isbn}' already exists",
            status_code=409,  # Conflict
        )


# === Исключения валидации ===

class InvalidYearException(AppException):
    """
    Исключение: невалидный год издания.
    
    Возникает при попытке указать год издания вне допустимого
    диапазона (1000 - текущий год).
    """
    def __init__(self, year: int):
        """
        Инициализация исключения.
        
        Args:
            year: Некорректный год издания
        """
        current_year = datetime.now().year
        super().__init__(
            message=f"Year {year} is invalid (must be 1000-{current_year})",
            status_code=400,  # Bad Request
        )


class InvalidPagesException(AppException):
    """
    Исключение: невалидное количество страниц.
    
    Возникает при попытке указать количество страниц,
    которое не является положительным числом.
    """
    def __init__(self, pages: int):
        """
        Инициализация исключения.
        
        Args:
            pages: Некорректное количество страниц
        """
        super().__init__(
            message=f"Pages count must be positive, got {pages}",
            status_code=400,  # Bad Request
        )


# === Исключения интеграции с внешними API ===

class OpenLibraryException(AppException):
    """
    Исключение: ошибка при обращении к Open Library API.
    
    Возникает при любых ошибках, связанных с вызовом
    внешнего API Open Library.
    """
    def __init__(self, message: str):
        """
        Инициализация исключения.
        
        Args:
            message: Сообщение об ошибке от API
        """
        super().__init__(
            message=f"Open Library API error: {message}",
            status_code=503,  # Service Unavailable
        )


class OpenLibraryTimeoutException(AppException):
    """
    Исключение: таймаут при обращении к Open Library API.
    
    Возникает когда время ожидания ответа от Open Library API
    превышает установленный лимит.
    """
    def __init__(self, timeout: float):
        """
        Инициализация исключения.
        
        Args:
            timeout: Время таймаута в секундах
        """
        super().__init__(
            message=f"Open Library API timeout after {timeout}s",
            status_code=504,  # Gateway Timeout
        )


