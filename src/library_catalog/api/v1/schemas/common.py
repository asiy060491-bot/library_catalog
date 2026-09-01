"""
Общие схемы для API.

Содержит:
- Пагинацию
- Generic ответы
- Health check
"""

from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel, Field, ConfigDict

T = TypeVar('T')


class PaginationParams(BaseModel):
    """
    Параметры пагинации для запросов.
    
    Используется для GET запросов с пагинацией.
    """
    page: int = Field(
        1,
        ge=1,
        description="Номер страницы (начиная с 1)"
    )
    page_size: int = Field(
        20,
        ge=1,
        le=100,
        description="Количество элементов на странице"
    )
    
    @property
    def offset(self) -> int:
        """
        Вычислить offset для SQL запроса.
        
        Returns:
            int: Значение OFFSET для SQL
        """
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        """
        Получить limit для SQL запроса.
        
        Returns:
            int: Значение LIMIT для SQL
        """
        return self.page_size
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"page": 1, "page_size": 20},
                {"page": 2, "page_size": 50}
            ]
        }
    )


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Generic схема для пагинированных ответов.
    
    Используется для ответов с пагинацией.
    """
    items: List[T] = Field(..., description="Список элементов на странице")
    total: int = Field(..., description="Общее количество элементов")
    page: int = Field(..., description="Текущая страница")
    page_size: int = Field(..., description="Размер страницы")
    pages: int = Field(..., description="Общее количество страниц")
    
    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        pagination: PaginationParams,
    ) -> "PaginatedResponse[T]":
        """
        Создать пагинированный ответ из данных.
        
        Args:
            items: Список элементов на странице
            total: Общее количество элементов
            pagination: Параметры пагинации
            
        Returns:
            PaginatedResponse[T]: Пагинированный ответ
        """
        pages = (total + pagination.page_size - 1) // pagination.page_size
        
        return cls(
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            pages=pages,
        )
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "items": [],
                    "total": 100,
                    "page": 1,
                    "page_size": 20,
                    "pages": 5
                }
            ]
        }
    )


class HealthCheckResponse(BaseModel):
    """
    Схема для health check эндпоинта.
    """
    status: str = Field("healthy", description="Статус сервиса")
    database: str = Field("connected", description="Статус подключения к БД")
    version: Optional[str] = Field(None, description="Версия API")
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "status": "healthy",
                    "database": "connected",
                    "version": "1.0.0"
                }
            ]
        }
    )


class ErrorResponse(BaseModel):
    """
    Схема для ответа с ошибкой.
    """
    error: str = Field(..., description="Тип ошибки")
    message: str = Field(..., description="Сообщение об ошибке")
    status_code: int = Field(..., description="HTTP статус код")
    details: Optional[dict] = Field(None, description="Дополнительные детали")
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "error": "BookNotFoundException",
                    "message": "Book with identifier '123e4567-e89b-12d3-a456-426614174000' not found",
                    "status_code": 404,
                    "details": {"resource": "Book", "identifier": "123e4567-e89b-12d3-a456-426614174000"}
                }
            ]
        }
    )
