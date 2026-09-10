"""
Схемы для API версии 1.
"""

from .book import BookBase, BookCreate, BookUpdate, ShowBook, BookFilters
from .common import (
    PaginationParams,
    PaginatedResponse,
    HealthCheckResponse,
    ErrorResponse,
)

__all__ = [
    # Book schemas
    "BookBase",
    "BookCreate",
    "BookUpdate",
    "ShowBook",
    "BookFilters",
    # Common schemas
    "PaginationParams",
    "PaginatedResponse",
    "HealthCheckResponse",
    "ErrorResponse",
]