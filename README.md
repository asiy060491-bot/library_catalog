# 📚 Library Catalog API

REST API для управления библиотечным каталогом.

![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)




## 🛠 Технологии
- Python 3.11
- FastAPI
- SQLAlchemy 2.0 (Async)
- Alembic (Миграции)
- PostgreSQL
- Poetry (Управление зависимостями)
- Docker / Docker Compose

## Запуск
1. poetry install
2. docker-compose up -d
3. poetry run uvicorn src.library_catalog.main:app --reload

## 📁 Структура проекта

```
library_catalog/
│
├── README.md                         Описание проекта
├── pyproject.toml                    Зависимости Poetry
├── .env.example                      Пример конфигурации
├── .gitignore                        
├── docker-compose.yml                PostgreSQL в Docker
├── alembic.ini                       Конфиг Alembic
│
├── src/
│   └── library_catalog/
│       ├── __init__.py
│       ├── main.py                   Точка входа
│       │
│       ├── api/                      API LAYER
│       │   ├── __init__.py
│       │   ├── dependencies.py       DI контейнер
│       │   └── v1/
│       │       ├── __init__.py
│       │       ├── routers/
│       │       │   ├── __init__.py
│       │       │   ├── books.py      CRUD эндпоинты
│       │       │   └── health.py     health check
│       │       └── schemas/
│       │           ├── __init__.py
│       │           ├── book.py       Pydantic схемы
│       │           └── common.py     пагинация
│       │
│       ├── core/                     CORE
│       │   ├── __init__.py
│       │   ├── config.py             Settings
│       │   ├── database.py           async engine
│       │   ├── logging_config.py     логирование
│       │   └── exceptions.py         базовые исключения
│       │
│       ├── data/                     DATA LAYER
│       │   ├── __init__.py
│       │   ├── models/
│       │   │   ├── __init__.py
│       │   │   └── book.py           SQLAlchemy модель
│       │   └── repositories/
│       │       ├── __init__.py
│       │       ├── base_repository.py базовый класс
│       │       └── book_repository.py CRUD для книг
│       │
│       ├── domain/                    DOMAIN LAYER
│       │   ├── __init__.py
│       │   ├── services/
│       │   │   ├── __init__.py
│       │   │   └── book_service.py    бизнес-логика
│       │   ├── exceptions.py          доменные ошибки
│       │   └── mappers/
│       │       ├── __init__.py
│       │       └── book_mapper.py     Entity ↔ DTO
│       │
│       ├── external/                  EXTERNAL LAYER
│       │   ├── __init__.py
│       │   ├── base/
│       │   │   ├── __init__.py
│       │   │   └── base_client.py     HTTP базовый клиент
│       │   ├── openlibrary/
│       │       ├── __init__.py
│       │       ├── client.py          Open Library API
│       │       └── schemas.py         Схемы ответов
│       │               
│       │      
│       │
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
│
├── alembic/
│   ├── versions/                      
│   ├── env.py                      
│   └── script.py.mako
│
└── tests/
    ├── __init__.py
    ├── conftest.py                   Фикстуры pytest
    ├── unit/
    │   ├── test_services/
    │   │   └── test_book_service.py  Тесты сервиса
    │   └── test_repositories/
    │       └── test_book_repository.py
    └── integration/
        └── test_api/
            └── test_books_api.py     Тесты API