"""
Модель Book (Книга) для библиотечного каталога.

Хранит информацию о книгах: название, автор, год издания,
жанр, количество страниц, доступность и дополнительные метаданные.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, JSON, String, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.library_catalog.core.database import Base


class Book(Base):
    """
    Модель книги в библиотеке.
    
    Атрибуты:
        book_id: Уникальный идентификатор книги (UUID)
        title: Название книги
        author: Автор книги
        year: Год издания
        genre: Жанр книги
        pages: Количество страниц
        available: Доступна ли книга для выдачи
        isbn: Международный стандартный книжный номер (уникальный)
        description: Описание книги
        extra: Дополнительные метаданные в формате JSON
        created_at: Дата создания записи
        updated_at: Дата последнего обновления
    """
    
    __tablename__ = "books"
    
    # Первичный ключ (UUID)
    book_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        doc="Уникальный идентификатор книги"
    )
    
    # Обязательные поля
    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        index=True,
        doc="Название книги"
    )
    
    author: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
        index=True,
        doc="Автор книги"
    )
    
    year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
        doc="Год издания"
    )
    
    genre: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        doc="Жанр книги"
    )
    
    pages: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Количество страниц"
    )
    
    available: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        doc="Доступна ли книга для выдачи"
    )
    
    # Опциональные поля
    isbn: Mapped[Optional[str]] = mapped_column(
        String(20),
        unique=True,
        nullable=True,
        index=True,
        doc="Международный стандартный книжный номер (ISBN)"
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Описание книги"
    )
    
    extra: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
        doc="Дополнительные метаданные (JSON)"
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        doc="Дата создания записи"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        doc="Дата последнего обновления"
    )
    
    # Составной индекс для частых запросов (автор + год)
    __table_args__ = (
        Index("idx_book_author_year", "author", "year"),
        Index("idx_book_title_author", "title", "author"),
    )
    
    def __repr__(self) -> str:
        """Строковое представление модели."""
        return f"<Book(id={self.book_id}, title='{self.title}', author='{self.author}')>"
    
    def __str__(self) -> str:
        """Пользовательское строковое представление."""
        return f"{self.title} by {self.author} ({self.year})"
