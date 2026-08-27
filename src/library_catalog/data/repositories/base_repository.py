"""
Базовый репозиторий с Generic CRUD операциями.
"""

from typing import Generic, TypeVar, Type, Optional, List, Any
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """
    Базовый репозиторий с CRUD операциями.
    
    Использование:
        class BookRepository(BaseRepository[Book]):
            def __init__(self, session: AsyncSession):
                super().__init__(session, Book)
    """
    
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model
    
    async def create(self, **kwargs) -> T:
        """Создать запись."""
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance
    
    async def get_by_id(self, id: UUID) -> Optional[T]:
        """
        Получить по ID.
        
        📝 Примечание: session.get() автоматически работает с primary key модели,
        независимо от его названия (id, book_id, user_id и т.д.)
        """
        return await self.session.get(self.model, id)
    
    async def update(self, id: UUID, **kwargs) -> Optional[T]:
        """Обновить запись."""
        instance = await self.get_by_id(id)
        if not instance:
            return None
        
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        
        await self.session.commit()
        await self.session.refresh(instance)
        return instance
    
    async def delete(self, id: UUID) -> bool:
        """Удалить запись."""
        instance = await self.get_by_id(id)
        if not instance:
            return False
        
        await self.session.delete(instance)
        await self.session.commit()
        return True
    
    async def get_all(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> List[T]:
        """Получить все записи с пагинацией."""
        result = await self.session.execute(
            select(self.model)
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())
    
    async def count(self) -> int:
        """Получить общее количество записей."""
        result = await self.session.execute(
            select(func.count()).select_from(self.model)
        )
        return result.scalar() or 0
