"""
Общие фикстуры для тестов.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from src.library_catalog.main import app
from src.library_catalog.core.database import Base, get_db
from src.library_catalog.data.repositories.book_repository import BookRepository
from src.library_catalog.domain.services.book_service import BookService
from src.library_catalog.external.openlibrary import OpenLibraryClient


# ========== Тестовая БД ==========

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestAsyncSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def override_get_db():
    """Переопределение get_db для тестов."""
    async with TestAsyncSessionLocal() as session:
        yield session


# Подменяем зависимость для тестов
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def anyio_backend():
    """Настройка бекенда для anyio."""
    return "asyncio"


@pytest.fixture
async def client():
    """Фикстура для HTTP клиента."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
async def db_session():
    """Фикстура для сессии БД."""
    async with TestAsyncSessionLocal() as session:
        yield session


@pytest.fixture
async def book_repository(db_session):
    """Фикстура для репозитория книг."""
    return BookRepository(db_session)


@pytest.fixture
async def book_service(book_repository):
    """Фикстура для сервиса книг."""
    ol_client = OpenLibraryClient()
    return BookService(
        book_repository=book_repository,
        openlibrary_client=ol_client,
    )


@pytest.fixture
def sample_book_data():
    """Фикстура с данными для тестовой книги."""
    return {
        "title": "Test Book",
        "author": "Test Author",
        "year": 2024,
        "genre": "Test Genre",
        "pages": 100,
        "isbn": "978-1234567890",
        "description": "Test description"
    }


@pytest.fixture
def sample_book_data_2():
    """Фикстура с данными для второй тестовой книги."""
    return {
        "title": "Another Test Book",
        "author": "Another Author",
        "year": 2023,
        "genre": "Fiction",
        "pages": 200,
        "isbn": "978-0987654321",
        "description": "Another test description"
    }


@pytest.fixture
async def setup_database():
    """Фикстура для инициализации БД."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)