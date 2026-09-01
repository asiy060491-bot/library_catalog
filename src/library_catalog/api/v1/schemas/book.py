"""
Pydantic схемы для работы с книгами в API.

Содержит схемы для:
- Создания книги (BookCreate)
- Обновления книги (BookUpdate)
- Отображения книги (ShowBook)
- Фильтрации книг (BookFilters)
"""

from datetime import datetime
from uuid import UUID
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict


class BookBase(BaseModel):
    """
    Базовая схема с общими полями для книг.
    
    Используется как основа для других схем.
    """
    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Название книги"
    )
    author: str = Field(
        ...,
        min_length=1,
        max_length=300,
        description="Имя автора"
    )
    year: int = Field(
        ...,
        ge=1000,
        le=2100,
        description="Год издания"
    )
    genre: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Жанр книги"
    )
    pages: int = Field(
        ...,
        gt=0,
        description="Количество страниц"
    )


class BookCreate(BookBase):
    """
    Схема для создания новой книги.
    
    Все поля обязательны, кроме isbn и description.
    """
    isbn: Optional[str] = Field(
        None,
        min_length=10,
        max_length=20,
        description="ISBN-10 или ISBN-13"
    )
    description: Optional[str] = Field(
        None,
        max_length=5000,
        description="Описание книги"
    )
    
    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v: Optional[str]) -> Optional[str]:
        """
        Валидация формата ISBN.
        
        Поддерживает:
        - ISBN-10: 0132350882
        - ISBN-13: 9780132350884
        - С дефисами: 978-0-13-235088-4
        
        Args:
            v: ISBN для валидации
            
        Returns:
            Optional[str]: Валидированный ISBN
            
        Raises:
            ValueError: Если ISBN имеет неверный формат
        """
        if v is None:
            return v
        
        # Удаляем дефисы и пробелы
        clean = v.replace("-", "").replace(" ", "")
        
        # Проверяем, что только цифры (и X для ISBN-10)
        if not clean.replace("X", "").isdigit():
            raise ValueError("ISBN must contain only digits and optionally 'X'")
        
        # Проверяем длину
        if len(clean) not in (10, 13):
            raise ValueError("ISBN must be 10 or 13 characters long")
        
        # Дополнительная валидация для ISBN-10
        if len(clean) == 10:
            # Проверка контрольной суммы ISBN-10
            total = 0
            for i, char in enumerate(clean):
                if char == 'X':
                    digit = 10
                else:
                    digit = int(char)
                total += (10 - i) * digit
            
            if total % 11 != 0:
                raise ValueError("Invalid ISBN-10 checksum")
        
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Clean Code",
                    "author": "Robert C. Martin",
                    "year": 2008,
                    "genre": "Programming",
                    "pages": 464,
                    "isbn": "978-0132350884",
                    "description": "A Handbook of Agile Software Craftsmanship"
                },
                {
                    "title": "The Pragmatic Programmer",
                    "author": "David Thomas",
                    "year": 1999,
                    "genre": "Programming",
                    "pages": 352,
                    "isbn": "978-0201616224",
                    "description": "From Journeyman to Master"
                }
            ]
        }
    )


class BookUpdate(BaseModel):
    """
    Схема для обновления книги.
    
    Все поля опциональны - обновляются только переданные.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    author: Optional[str] = Field(None, min_length=1, max_length=300)
    year: Optional[int] = Field(None, ge=1000, le=2100)
    genre: Optional[str] = Field(None, min_length=1, max_length=100)
    pages: Optional[int] = Field(None, gt=0)
    available: Optional[bool] = Field(None, description="Доступность книги")
    isbn: Optional[str] = Field(None, min_length=10, max_length=20)
    description: Optional[str] = Field(None, max_length=5000)
    
    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v: Optional[str]) -> Optional[str]:
        """Валидация формата ISBN (та же логика что и в BookCreate)."""
        if v is None:
            return v
        
        clean = v.replace("-", "").replace(" ", "")
        
        if not clean.replace("X", "").isdigit():
            raise ValueError("ISBN must contain only digits and optionally 'X'")
        
        if len(clean) not in (10, 13):
            raise ValueError("ISBN must be 10 or 13 characters long")
        
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Clean Code (Updated)",
                    "year": 2024,
                    "pages": 500
                }
            ]
        }
    )


class ShowBook(BookBase):
    """
    Схема для отображения книги (ответ API).
    
    Содержит все поля книги, включая дополнительные данные из БД.
    """
    book_id: UUID = Field(..., description="Уникальный идентификатор книги")
    available: bool = Field(..., description="Доступна ли книга")
    isbn: Optional[str] = Field(None, description="ISBN книги")
    description: Optional[str] = Field(None, description="Описание книги")
    extra: Optional[Dict[str, Any]] = Field(
        None,
        description="Дополнительные данные (обложка, темы и т.д.)"
    )
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата последнего обновления")
    
    model_config = ConfigDict(
        from_attributes=True,  # Для работы с ORM моделями
        json_schema_extra={
            "examples": [
                {
                    "book_id": "123e4567-e89b-12d3-a456-426614174000",
                    "title": "Clean Code",
                    "author": "Robert C. Martin",
                    "year": 2008,
                    "genre": "Programming",
                    "pages": 464,
                    "available": True,
                    "isbn": "978-0132350884",
                    "description": "A Handbook of Agile Software Craftsmanship",
                    "extra": {
                        "cover_url": "https://covers.openlibrary.org/b/id/8065615-L.jpg",
                        "subjects": ["Computer Science", "Software Engineering"],
                        "language": "eng",
                        "publisher": "Prentice Hall"
                    },
                    "created_at": "2024-01-01T12:00:00Z",
                    "updated_at": "2024-01-01T12:00:00Z"
                }
            ]
        }
    )


class BookFilters(BaseModel):
    """
    Фильтры для поиска книг.
    
    Используется для фильтрации списка книг.
    """
    title: Optional[str] = Field(
        None,
        description="Поиск по названию (частичное совпадение)"
    )
    author: Optional[str] = Field(
        None,
        description="Поиск по автору (частичное совпадение)"
    )
    genre: Optional[str] = Field(
        None,
        description="Точное совпадение жанра"
    )
    year: Optional[int] = Field(
        None,
        ge=1000,
        le=2100,
        description="Точное совпадение года издания"
    )
    available: Optional[bool] = Field(
        None,
        description="Фильтр по доступности"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Clean",
                    "author": "Martin",
                    "genre": "Programming",
                    "year": 2008,
                    "available": True
                }
            ]
        }
    )
