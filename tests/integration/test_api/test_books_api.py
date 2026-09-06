"""
Интеграционные тесты для API книг.
"""

import pytest
from uuid import uuid4


@pytest.mark.asyncio
async def test_get_books_empty(client, setup_database):
    """Тест получения списка книг (пустой)."""
    response = await client.get("/api/v1/books/")
    
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data


@pytest.mark.asyncio
async def test_create_book(client, sample_book_data, setup_database):
    """Тест создания книги через API."""
    response = await client.post("/api/v1/books/", json=sample_book_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == sample_book_data["title"]
    assert data["author"] == sample_book_data["author"]
    assert data["isbn"] == sample_book_data["isbn"]


@pytest.mark.asyncio
async def test_create_book_invalid_data(client, setup_database):
    """Тест создания книги с невалидными данными."""
    invalid_data = {
        "title": "Test",
        "author": "Test",
        "year": 3000,  # Невалидный год
        "genre": "Test",
        "pages": 100,
    }
    
    response = await client.post("/api/v1/books/", json=invalid_data)
    
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_book_by_id(client, sample_book_data, setup_database):
    """Тест получения книги по ID через API."""
    # Создаем книгу
    create_response = await client.post("/api/v1/books/", json=sample_book_data)
    assert create_response.status_code == 201
    
    book_id = create_response.json()["book_id"]
    
    # Получаем по ID
    response = await client.get(f"/api/v1/books/{book_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["book_id"] == book_id
    assert data["title"] == sample_book_data["title"]


@pytest.mark.asyncio
async def test_get_book_not_found(client, setup_database):
    """Тест получения несуществующей книги."""
    response = await client.get(f"/api/v1/books/{uuid4()}")
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_book(client, sample_book_data, setup_database):
    """Тест обновления книги через API."""
    # Создаем книгу
    create_response = await client.post("/api/v1/books/", json=sample_book_data)
    assert create_response.status_code == 201
    
    book_id = create_response.json()["book_id"]
    
    # Обновляем
    update_data = {"title": "Updated Title", "pages": 200}
    response = await client.patch(f"/api/v1/books/{book_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["pages"] == 200


@pytest.mark.asyncio
async def test_delete_book(client, sample_book_data, setup_database):
    """Тест удаления книги через API."""
    # Создаем книгу
    create_response = await client.post("/api/v1/books/", json=sample_book_data)
    assert create_response.status_code == 201
    
    book_id = create_response.json()["book_id"]
    
    # Удаляем
    response = await client.delete(f"/api/v1/books/{book_id}")
    
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_get_books_with_pagination(client, sample_book_data, setup_database):
    """Тест пагинации."""
    # Создаем несколько книг
    for i in range(5):
        book_data = sample_book_data.copy()
        book_data["title"] = f"Pagination Test {i}"
        book_data["isbn"] = f"978-{i:010d}"
        await client.post("/api/v1/books/", json=book_data)
    
    # Получаем с пагинацией
    response = await client.get("/api/v1/books/?page=1&page_size=2")
    
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert len(data["items"]) <= 2
