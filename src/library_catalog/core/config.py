"""
Конфигурация приложения.
"""

from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Настройки приложения.
    """

    # Environment
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/library_catalog"
    database_pool_size: int = 5

    # API
    api_v1_prefix: str = "/api/v1"

    # OpenLibrary
    openlibrary_base_url: str = "https://openlibrary.org"
    openlibrary_timeout: float = 10.0
    openlibrary_retries: int = 3

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        # Разрешаем любые дополнительные поля, если они есть в .env
        extra = "ignore"


# Создаем экземпляр настроек
settings = Settings()

__all__ = [
    "settings",
    "Settings",
]