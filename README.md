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
├── README.md                         # ← Создать: описание проекта
├── pyproject.toml                    # ← Создать: зависимости Poetry
├── .env.example                      # ← Создать: пример конфигурации
├── .gitignore                        # ← Создать для игнора добавления в GIT
├── docker-compose.yml                # ← Создать: PostgreSQL в Docker
├── alembic.ini                       # ← Создать: конфиг Alembic
│
├── src/
│   └── library_catalog/
│       ├── __init__.py
│       ├── main.py                   # ← Создать: точка входа
│       │
│       ├── api/                      # API LAYER
│       │   ├── __init__.py
│       │   ├── dependencies.py       # ← Создать: DI контейнер
│       │   └── v1/
│       │       ├── __init__.py
│       │       ├── routers/
│       │       │   ├── __init__.py
│       │       │   ├── books.py      # ← Создать: CRUD эндпоинты
│       │       │   └── health.py     # ← Создать: health check
│       │       └── schemas/
│       │           ├── __init__.py
│       │           ├── book.py       # ← Создать: Pydantic схемы
│       │           └── common.py     # ← Создать: пагинация
│       │
│       ├── core/                     # CORE
│       │   ├── __init__.py
│       │   ├── config.py             # ← Создать: Settings
│       │   ├── database.py           # ← Создать: async engine
│       │   ├── logging_config.py     # ← Создать: логирование
│       │   └── exceptions.py         # ← Создать: базовые исключения
│       │
│       ├── data/                     # DATA LAYER
│       │   ├── __init__.py
│       │   ├── models/
│       │   │   ├── __init__.py
│       │   │   └── book.py           # ← Создать: SQLAlchemy модель
│       │   └── repositories/
│       │       ├── __init__.py
│       │       ├── base_repository.py # ← Создать: базовый класс
│       │       └── book_repository.py # ← Создать: CRUD для книг
│       │
│       ├── domain/                   # DOMAIN LAYER
│       │   ├── __init__.py
│       │   ├── services/
│       │   │   ├── __init__.py
│       │   │   └── book_service.py   # ← Создать: бизнес-логика
│       │   ├── exceptions.py         # ← Создать: доменные ошибки
│       │   └── mappers/
│       │       ├── __init__.py
│       │       └── book_mapper.py    # ← Создать: Entity ↔ DTO
│       │
│       ├── external/                 # EXTERNAL LAYER
│       │   ├── __init__.py
│       │   ├── base/
│       │   │   ├── __init__.py
│       │   │   └── base_client.py    # ← Создать: HTTP базовый клиент
│       │   ├── openlibrary/
│       │   │   ├── __init__.py
│       │   │   ├── client.py         # ← Создать: Open Library API
│       │   │   └── schemas.py        # ← Создать: схемы ответов
│       │   └── jsonbin/              # Опционально
│       │       ├── __init__.py
│       │       └── client.py
│       │
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
│
├── alembic/
│   ├── versions/                     # ← Миграции создаются автоматически
│   ├── env.py                        # ← Настроить для async
│   └── script.py.mako
│
└── tests/
    ├── __init__.py
    ├── conftest.py                   # ← Создать: фикстуры pytest
    ├── unit/
    │   ├── test_services/
    │   │   └── test_book_service.py  # ← Создать: тесты сервиса
    │   └── test_repositories/
    │       └── test_book_repository.py
    └── integration/
        └── test_api/
            └── test_books_api.py     # ← Создать: тесты API