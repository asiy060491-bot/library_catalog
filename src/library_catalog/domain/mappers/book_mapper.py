"""
Маппер для преобразования данных книг между слоями приложения.

Обеспечивает преобразование между ORM-моделью Book и DTO для API.
"""

from typing import List, Optional
from ...data.models.book import Book
from ...api.v1.schemas.book import ShowBook


class BookMapper:
    """
    Маппер для преобразования Book entity в DTO.
    
    Содержит статические методы для преобразования между
    различными представлениями данных книги.
    """
    
    @staticmethod
    def to_show_book(book: Book) -> ShowBook:
        """
        Преобразовать Book ORM модель в ShowBook DTO.
        
        Args:
            book: ORM модель из БД
            
        Returns:
            ShowBook: Pydantic модель для API
            
        Example:
            >>> book = Book(book_id=1, title="Python Programming", ...)
            >>> dto = BookMapper.to_show_book(book)
            >>> print(dto.title)
            "Python Programming"
        """
        return ShowBook(
            book_id=book.book_id,
            title=book.title,
            author=book.author,
            year=book.year,
            genre=book.genre,
            pages=book.pages,
            available=book.available,
            isbn=book.isbn,
            description=book.description,
            extra=book.extra,
            created_at=book.created_at,
            updated_at=book.updated_at,
        )
    
    @staticmethod
    def to_show_books(books: List[Book]) -> List[ShowBook]:
        """
        Преобразовать список книг в список ShowBook DTO.
        
        Args:
            books: Список ORM моделей книг
            
        Returns:
            List[ShowBook]: Список Pydantic моделей для API
            
        Example:
            >>> books = [book1, book2, book3]
            >>> dtos = BookMapper.to_show_books(books)
            >>> len(dtos)
            3
        """
        return [BookMapper.to_show_book(book) for book in books]
    
    @staticmethod
    def to_show_book_optional(book: Optional[Book]) -> Optional[ShowBook]:
        """
        Преобразовать опциональную Book модель в опциональный ShowBook DTO.
        
        Args:
            book: ORM модель из БД или None
            
        Returns:
            Optional[ShowBook]: Pydantic модель для API или None
        """
        if book is None:
            return None
        return BookMapper.to_show_book(book)
    
    @staticmethod
    def to_book_dict(show_book: ShowBook) -> dict:
        """
        Преобразовать ShowBook DTO в словарь для создания/обновления в БД.
        
        Args:
            show_book: Pydantic модель из API
            
        Returns:
            dict: Словарь с данными для ORM
            
        Example:
            >>> dto = ShowBook(title="New Book", ...)
            >>> data = BookMapper.to_book_dict(dto)
            >>> print(data['title'])
            "New Book"
        """
        return {
            "title": show_book.title,
            "author": show_book.author,
            "year": show_book.year,
            "genre": show_book.genre,
            "pages": show_book.pages,
            "available": show_book.available,
            "isbn": show_book.isbn,
            "description": show_book.description,
            "extra": show_book.extra,
        }
    
    @staticmethod
    def to_update_dict(show_book: ShowBook, exclude_unset: bool = True) -> dict:
        """
        Преобразовать ShowBook DTO в словарь для обновления,
        исключая незаданные поля.
        
        Args:
            show_book: Pydantic модель из API
            exclude_unset: Исключать ли незаданные поля
            
        Returns:
            dict: Словарь только с заданными полями
            
        Example:
            >>> dto = ShowBook(title="Updated Title")
            >>> data = BookMapper.to_update_dict(dto)
            >>> print(data)
            {'title': 'Updated Title'}
        """
        if exclude_unset:
            # Используем model_dump для получения только заданных полей
            return show_book.model_dump(exclude_unset=True)
        return show_book.model_dump()
    
    @staticmethod
    def merge_book_data(existing_book: Book, update_data: dict) -> dict:
        """
        Объединить существующие данные книги с обновлениями.
        
        Args:
            existing_book: Существующая ORM модель
            update_data: Словарь с данными для обновления
            
        Returns:
            dict: Объединенный словарь данных
            
        Example:
            >>> book = Book(title="Old Title", pages=100)
            >>> update = {"title": "New Title"}
            >>> merged = BookMapper.merge_book_data(book, update)
            >>> print(merged['title'])
            "New Title"
            >>> print(merged['pages'])
            100
        """
        # Базовые данные из существующей книги
        merged = {
            "title": existing_book.title,
            "author": existing_book.author,
            "year": existing_book.year,
            "genre": existing_book.genre,
            "pages": existing_book.pages,
            "available": existing_book.available,
            "isbn": existing_book.isbn,
            "description": existing_book.description,
            "extra": existing_book.extra,
        }
        
        # Обновляем только те поля, которые есть в update_data
        for key, value in update_data.items():
            if key in merged and value is not None:
                merged[key] = value
        
        return merged
