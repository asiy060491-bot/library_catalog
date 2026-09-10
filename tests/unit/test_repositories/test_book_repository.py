"""
Тесты для BookRepository.
"""

import pytest
from datetime import datetime
from src.library_catalog.data.models import Book


@pytest.mark.asyncio
async def test_create_book(book_repository, setup_database):
    """Тест создания книги в БД."""
    book_data = {
        "title": "Repository Test Book",
        "author": "Repository Author",
        "year": 2024,
        "genre": "Test",
        "pages": 150,
        "available": True,
        "isbn": "978-1111111111",
        "description": "Repository test description",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    
    book = await book_repository.create(**book_data)
    
    assert book is not None
    assert book.title == book_data["title"]
    assert book.author == book_data["author"]


@pytest.mark.asyncio
async def test_get_book_by_id(book_repository, setup_database):
    """Тест получения книги по ID."""
    # Создаем книгу
    book_data = {
        "title": "Get By ID Test",
        "author": "Test Author",
        "year": 2024,
        "genre": "Test",
        "pages": 100,
        "available": True,
        "isbn": "978-2222222222",
        "description": "Get by ID test",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    
    created = await book_repository.create(**book_data)
    
    # Получаем по ID
    found = await book_repository.get_by_id(created.book_id)
    
    assert found is not None
    assert found.book_id == created.book_id
    assert found.title == book_data["title"]


@pytest.mark.asyncio
async def test_get_all_books(book_repository, setup_database):
    """Тест получения всех книг."""
    # Создаем несколько книг
    for i in range(3):
        book_data = {
            "title": f"Test Book {i}",
            "author": f"Author {i}",
            "year": 2024,
            "genre": "Test",
            "pages": 100 + i,
            "available": True,
            "isbn": f"978-{i:010d}",
            "description": f"Description {i}",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        await book_repository.create(**book_data)
    
    # Получаем все книги
    books = await book_repository.get_all()
    
    assert len(books) >= 3


@pytest.mark.asyncio
async def test_find_by_isbn(book_repository, setup_database):
    """Тест поиска по ISBN."""
    test_isbn = "978-3333333333"
    
    book_data = {
        "title": "Find By ISBN Test",
        "author": "Test Author",
        "year": 2024,
        "genre": "Test",
        "pages": 100,
        "available": True,
        "isbn": test_isbn,
        "description": "Find by ISBN test",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    
    await book_repository.create(**book_data)
    
    # Ищем по ISBN
    found = await book_repository.find_by_isbn(test_isbn)
    
    assert found is not None
    assert found.isbn == test_isbn


@pytest.mark.asyncio
async def test_update_book(book_repository, setup_database):
    """Тест обновления книги."""
    # Создаем книгу
    book_data = {
        "title": "Update Test",
        "author": "Original Author",
        "year": 2024,
        "genre": "Test",
        "pages": 100,
        "available": True,
        "isbn": "978-4444444444",
        "description": "Update test",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    
    created = await book_repository.create(**book_data)
    
    # Обновляем
    updated = await book_repository.update(
        created.book_id,
        title="Updated Title",
        pages=200
    )
    
    assert updated.title == "Updated Title"
    assert updated.pages == 200
    assert updated.author == "Original Author"  # Не изменилось


@pytest.mark.asyncio
async def test_delete_book(book_repository, setup_database):
    """Тест удаления книги."""
    # Создаем книгу
    book_data = {
        "title": "Delete Test",
        "author": "Test Author",
        "year": 2024,
        "genre": "Test",
        "pages": 100,
        "available": True,
        "isbn": "978-5555555555",
        "description": "Delete test",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    
    created = await book_repository.create(**book_data)
    
    # Удаляем
    result = await book_repository.delete(created.book_id)
    assert result is True
    
    # Проверяем, что книги нет
    found = await book_repository.get_by_id(created.book_id)
    assert found is None
