"""
Конфигурация приложения Library Catalog.
Загружает настройки из .env файла с валидацией.
"""

from functools import lru_cache
from typing import Literal
from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Настройки приложения.
    Загружаются из .env файла с валидацией.
    """
    
    # Базовые настройки (обязательные)
    app_name: str = "Library Catalog API"
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = True
    database_url: PostgresDsn
    
    # Остальные поля добавляются по мере необходимости
    database_pool_size: int = 20
    api_v1_prefix: str = "/api/v1"
    log_level: str = "INFO"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    cors_origins: list[str] = ["*"]
    openlibrary_base_url: str = "https://openlibrary.org"
    openlibrary_timeout: float = 10.0
    
    @field_validator("database_url")
    @classmethod
    def validate_postgres_url(cls, v: PostgresDsn) -> PostgresDsn:
        """
        Проверяет, что используется PostgreSQL.
        """
        if not str(v).startswith("postgresql"):
            raise ValueError("Only PostgreSQL is supported")
        return v
    
    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """
        Проверяет, что уровень логирования корректен.
        """
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"log_level must be one of {allowed}")
        return v.upper()
    
    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """
        Проверяет, что окружение корректно.
        """
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"environment must be one of {allowed}")
        return v
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Возвращает настройки с кешированием.
    Использует lru_cache для предотвращения повторной загрузки.
    """
    return Settings()


# Создаём глобальный экземпляр настроек для удобства
settings = get_settings()
