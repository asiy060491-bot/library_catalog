"""
Репозиторий для работы с книгами.
"""

from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.library_catalog.data.models import Book
from src.library_catalog.data.repositories.base_repository import BaseRepository


class BookRepository(BaseRepository[Book]):
    """Репозиторий для работы с книгами."""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, Book)
    
    async def find_by_filters(
        self,
        title: Optional[str] = None,
        author: Optional[str] = None,
        genre: Optional[str] = None,
        year: Optional[int] = None,
        available: Optional[bool] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Book]:
        """
        Поиск книг с фильтрацией.
        
        Args:
            title: Поиск по названию (частичное совпадение)
            author: Поиск по автору (частичное совпадение)
            genre: Поиск по жанру (точное совпадение)
            year: Год издания (точное совпадение)
            available: Статус доступности
            limit: Максимальное количество записей
            offset: Смещение
            
        Returns:
            Список книг, соответствующих фильтрам
        """
        query = select(Book)
        filters = []
        
        if title:
            filters.append(Book.title.ilike(f"%{title}%"))
        if author:
            filters.append(Book.author.ilike(f"%{author}%"))
        if genre:
            filters.append(Book.genre == genre)
        if year:
            filters.append(Book.year == year)
        if available is not None:
            filters.append(Book.available == available)
        
        if filters:
            query = query.where(and_(*filters))
        
        query = query.limit(limit).offset(offset)
        
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def find_by_isbn(self, isbn: str) -> Optional[Book]:
        """Найти книгу по ISBN (точное совпадение)."""
        result = await self.session.execute(
            select(Book).where(Book.isbn == isbn)
        )
        return result.scalar_one_or_none()
    
    async def count_by_filters(
        self,
        title: Optional[str] = None,
        author: Optional[str] = None,
        genre: Optional[str] = None,
        year: Optional[int] = None,
        available: Optional[bool] = None,
    ) -> int:
        """
        Подсчитать количество книг по фильтрам.
        
        Args:
            title: Поиск по названию (частичное совпадение)
            author: Поиск по автору (частичное совпадение)
            genre: Жанр (точное совпадение)
            year: Год издания (точное совпадение)
            available: Статус доступности
            
        Returns:
            Количество книг, соответствующих фильтрам
        """
        query = select(func.count()).select_from(Book)
        filters = []
        
        if title:
            filters.append(Book.title.ilike(f"%{title}%"))
        if author:
            filters.append(Book.author.ilike(f"%{author}%"))
        if genre:
            filters.append(Book.genre == genre)
        if year:
            filters.append(Book.year == year)
        if available is not None:
            filters.append(Book.available == available)
        
        if filters:
            query = query.where(and_(*filters))
        
        result = await self.session.execute(query)
        return result.scalar() or 0
    
    async def find_available(
        self,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Book]:
        """Найти все доступные книги."""
        result = await self.session.execute(
            select(Book)
            .where(Book.available == True)
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())
    
    async def find_by_author(
        self,
        author: str,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Book]:
        """Найти книги по автору (частичное совпадение)."""
        result = await self.session.execute(
            select(Book)
            .where(Book.author.ilike(f"%{author}%"))
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())
    
    async def find_by_genre(
        self,
        genre: str,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Book]:
        """Найти книги по жанру."""
        result = await self.session.execute(
            select(Book)
            .where(Book.genre == genre)
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())
