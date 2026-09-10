"""
Настройка подключения к базе данных PostgreSQL.
Использует асинхронный SQLAlchemy.
"""

from typing import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.library_catalog.core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    str(settings.database_url),
    pool_size=settings.database_pool_size,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_recycle=3600,
)


async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def check_db_connection() -> bool:
    """Проверяет доступность БД."""
    try:
        async with async_session_maker() as session:
            await session.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


async def dispose_engine() -> None:
    """Закрыть все соединения с БД."""
    await engine.dispose()


__all__ = [
    "Base",
    "engine",
    "async_session_maker",
    "get_db",
    "init_db",
    "check_db_connection",
    "dispose_engine",
]


