"""
Тесты для BookService.
"""

import pytest
from uuid import uuid4
from src.library_catalog.domain.exceptions import (
    BookNotFoundException,
    BookAlreadyExistsException,
    InvalidYearException,
    InvalidPagesException,
)


@pytest.mark.asyncio
async def test_create_book(book_service, sample_book_data, setup_database):
    """Тест создания книги."""
    from src.library_catalog.api.v1.schemas.book import BookCreate
    
    book_create = BookCreate(**sample_book_data)
    result = await book_service.create_book(book_create)
    
    assert result is not None
    assert result.title == sample_book_data["title"]
    assert result.author == sample_book_data["author"]
    assert result.isbn == sample_book_data["isbn"]


@pytest.mark.asyncio
async def test_create_book_duplicate_isbn(book_service, sample_book_data, setup_database):
    """Тест создания книги с дублирующимся ISBN."""
    from src.library_catalog.api.v1.schemas.book import BookCreate
    
    book_create = BookCreate(**sample_book_data)
    await book_service.create_book(book_create)
    
    # Пытаемся создать книгу с тем же ISBN
    with pytest.raises(BookAlreadyExistsException):
        await book_service.create_book(book_create)


@pytest.mark.asyncio
async def test_create_book_invalid_year(book_service, sample_book_data, setup_database):
    """Тест создания книги с невалидным годом."""
    from src.library_catalog.api.v1.schemas.book import BookCreate
    
    invalid_data = sample_book_data.copy()
    invalid_data["year"] = 3000  # Невалидный год
    
    book_create = BookCreate(**invalid_data)
    
    with pytest.raises(InvalidYearException):
        await book_service.create_book(book_create)


@pytest.mark.asyncio
async def test_create_book_invalid_pages(book_service, sample_book_data, setup_database):
    """Тест создания книги с невалидным количеством страниц."""
    from src.library_catalog.api.v1.schemas.book import BookCreate
    
    invalid_data = sample_book_data.copy()
    invalid_data["pages"] = -10  # Невалидное количество страниц
    
    book_create = BookCreate(**invalid_data)
    
    with pytest.raises(InvalidPagesException):
        await book_service.create_book(book_create)


@pytest.mark.asyncio
async def test_get_book(book_service, sample_book_data, setup_database):
    """Тест получения книги по ID."""
    from src.library_catalog.api.v1.schemas.book import BookCreate
    
    book_create = BookCreate(**sample_book_data)
    created = await book_service.create_book(book_create)
    
    result = await book_service.get_book(created.book_id)
    
    assert result is not None
    assert result.book_id == created.book_id
    assert result.title == sample_book_data["title"]


@pytest.mark.asyncio
async def test_get_book_not_found(book_service, setup_database):
    """Тест получения несуществующей книги."""
    with pytest.raises(BookNotFoundException):
        await book_service.get_book(uuid4())


@pytest.mark.asyncio
async def test_search_books(book_service, sample_book_data, sample_book_data_2, setup_database):
    """Тест поиска книг."""
    from src.library_catalog.api.v1.schemas.book import BookCreate
    
    # Создаем две книги
    book1 = await book_service.create_book(BookCreate(**sample_book_data))
    book2 = await book_service.create_book(BookCreate(**sample_book_data_2))
    
    # Ищем по названию
    results, total = await book_service.search_books(title="Test")
    assert total >= 1
    assert len(results) >= 1
    
    # Ищем по автору
    results, total = await book_service.search_books(author="Another")
    assert total >= 1
    assert len(results) >= 1


@pytest.mark.asyncio
async def test_update_book(book_service, sample_book_data, setup_database):
    """Тест обновления книги."""
    from src.library_catalog.api.v1.schemas.book import BookCreate, BookUpdate
    
    book_create = BookCreate(**sample_book_data)
    created = await book_service.create_book(book_create)
    
    # Обновляем название
    update_data = BookUpdate(title="Updated Title")
    result = await book_service.update_book(created.book_id, update_data)
    
    assert result.title == "Updated Title"
    assert result.author == sample_book_data["author"]  # Не изменилось


@pytest.mark.asyncio
async def test_delete_book(book_service, sample_book_data, setup_database):
    """Тест удаления книги."""
    from src.library_catalog.api.v1.schemas.book import BookCreate
    
    book_create = BookCreate(**sample_book_data)
    created = await book_service.create_book(book_create)
    
    await book_service.delete_book(created.book_id)
    
    # Проверяем, что книга удалена
    with pytest.raises(BookNotFoundException):
        await book_service.get_book(created.book_id)
