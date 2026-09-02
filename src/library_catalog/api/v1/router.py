"""
Главный роутер для API версии 1.
"""

from fastapi import APIRouter
from .routers import books_router, health_router

# Создаем главный роутер для v1
router = APIRouter(prefix="/api/v1")

# Подключаем все роутеры
router.include_router(books_router)
router.include_router(health_router)
