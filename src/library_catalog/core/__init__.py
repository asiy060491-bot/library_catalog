"""
Core модуль с базовыми компонентами.

Содержит:
- Конфигурацию (config)
- Подключение к БД (database)
- Базовые исключения (exceptions)
- Настройку логирования (logging_config)
"""

from .config import settings
from .database import get_db, init_db, dispose_engine, Base
from .exceptions import (
    AppException,
    NotFoundException,
    register_exception_handlers,
)
from .logging_config import setup_logging

__all__ = [
    "settings",
    "get_db",
    "init_db",
    "dispose_engine",
    "Base",
    "AppException",
    "NotFoundException",
    "register_exception_handlers",
    "setup_logging",
]