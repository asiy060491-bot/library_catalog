"""
ORM models for the application.

Экспортирует все модели и Base для Alembic.
"""

from src.library_catalog.core.database import Base
from .book import Book

__all__ = ["Base", "Book"]
