"""
Роутеры API версии 1.
"""

from .books import router as books_router
from .health import router as health_router

__all__ = ["books_router", "health_router"]