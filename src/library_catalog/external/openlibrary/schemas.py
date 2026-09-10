"""
Pydantic модели для работы с Open Library API.

Содержит модели для валидации ответов от Open Library.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class OpenLibrarySearchDoc(BaseModel):
    """
    Документ из поиска Open Library.

    Представляет одну книгу в результатах поиска.
    """

    title: str = Field(..., description="Название книги")
    author_name: Optional[List[str]] = Field(None, alias="author_name", description="Имена авторов")
    cover_i: Optional[int] = Field(None, alias="cover_i", description="ID обложки")
    subject: Optional[List[str]] = Field(None, description="Темы/категории")
    publisher: Optional[List[str]] = Field(None, description="Издатели")
    language: Optional[List[str]] = Field(None, description="Языки")
    ratings_average: Optional[float] = Field(None, alias="ratings_average", description="Средний рейтинг")
    first_publish_year: Optional[int] = Field(None, alias="first_publish_year", description="Год первой публикации")
    number_of_pages_median: Optional[int] = Field(None, alias="number_of_pages_median",
                                                  description="Медианное количество страниц")
    isbn: Optional[List[str]] = Field(None, description="ISBN номера")
    key: Optional[str] = Field(None, description="Ключ книги в Open Library")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "title": "Clean Code",
                "author_name": ["Robert C. Martin"],
                "cover_i": 123456,
                "subject": ["Programming", "Software Engineering"],
                "publisher": ["Prentice Hall"],
                "language": ["eng"],
                "ratings_average": 4.5,
                "first_publish_year": 2008,
                "number_of_pages_median": 464,
                "isbn": ["9780132350884"],
                "key": "/works/OL1234567W"
            }
        }


class OpenLibrarySearchResponse(BaseModel):
    """
    Ответ от Open Library API /search.json.
    """

    numFound: int = Field(..., description="Общее количество найденных результатов")
    docs: List[OpenLibrarySearchDoc] = Field(..., description="Список найденных документов")
    start: int = Field(0, description="Начальный индекс в результатах")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "numFound": 42,
                "start": 0,
                "docs": []
            }
        }