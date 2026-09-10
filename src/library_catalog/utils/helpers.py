"""
Вспомогательные функции (helpers) для приложения.

Содержит общие утилиты, используемые в разных частях проекта.
"""

import re
import uuid
from datetime import datetime
from typing import Any, Dict, Optional, TypeVar, Generic, List
from uuid import UUID

# ========== РАБОТА СО СТРОКАМИ ==========

def slugify(text: str) -> str:
    """
    Преобразовать текст в slug (для URL).
    
    Args:
        text: Текст для преобразования
        
    Returns:
        str: Slug-версия текста
        
    Example:
        >>> slugify("Hello World!")
        'hello-world'
    """
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Обрезать текст до указанной длины.
    
    Args:
        text: Текст для обрезания
        max_length: Максимальная длина
        suffix: Суффикс для обрезанного текста
        
    Returns:
        str: Обрезанный текст
        
    Example:
        >>> truncate_text("Very long text...", 10)
        'Very long...'
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


# ========== РАБОТА С ДАТАМИ ==========

def get_current_year() -> int:
    """
    Получить текущий год.
    
    Returns:
        int: Текущий год
        
    Example:
        >>> get_current_year()
        2026
    """
    return datetime.now().year


def format_datetime(dt: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Форматировать дату и время.
    
    Args:
        dt: Дата и время
        format: Формат вывода
        
    Returns:
        str: Отформатированная дата
        
    Example:
        >>> format_datetime(datetime(2024, 1, 1))
        '2024-01-01 00:00:00'
    """
    return dt.strftime(format)


def parse_date(date_str: str, format: str = "%Y-%m-%d") -> Optional[datetime]:
    """
    Парсить строку с датой.
    
    Args:
        date_str: Строка с датой
        format: Формат даты
        
    Returns:
        Optional[datetime]: Дата или None если ошибка
    """
    try:
        return datetime.strptime(date_str, format)
    except ValueError:
        return None


# ========== РАБОТА С UUID ==========

def is_valid_uuid(uuid_string: str) -> bool:
    """
    Проверить, является ли строка валидным UUID.
    
    Args:
        uuid_string: Строка для проверки
        
    Returns:
        bool: True если валидный UUID
        
    Example:
        >>> is_valid_uuid("123e4567-e89b-12d3-a456-426614174000")
        True
    """
    try:
        UUID(uuid_string)
        return True
    except ValueError:
        return False


def generate_uuid() -> str:
    """
    Сгенерировать новый UUID.
    
    Returns:
        str: Новый UUID в виде строки
        
    Example:
        >>> generate_uuid()
        '123e4567-e89b-12d3-a456-426614174000'
    """
    return str(uuid.uuid4())


# ========== РАБОТА С ID ==========

def generate_short_id(length: int = 8) -> str:
    """
    Сгенерировать короткий ID.
    
    Args:
        length: Длина ID
        
    Returns:
        str: Короткий ID
        
    Example:
        >>> generate_short_id()
        'aBc123De'
    """
    import random
    import string
    
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


# ========== РАБОТА С ДАННЫМИ ==========

def filter_dict(data: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
    """
    Оставить только указанные ключи в словаре.
    
    Args:
        data: Исходный словарь
        keys: Ключи для фильтрации
        
    Returns:
        Dict[str, Any]: Отфильтрованный словарь
        
    Example:
        >>> filter_dict({"a": 1, "b": 2, "c": 3}, ["a", "c"])
        {'a': 1, 'c': 3}
    """
    return {k: v for k, v in data.items() if k in keys}


def exclude_keys(data: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
    """
    Исключить указанные ключи из словаря.
    
    Args:
        data: Исходный словарь
        keys: Ключи для исключения
        
    Returns:
        Dict[str, Any]: Словарь без исключенных ключей
        
    Example:
        >>> exclude_keys({"a": 1, "b": 2, "c": 3}, ["b"])
        {'a': 1, 'c': 3}
    """
    return {k: v for k, v in data.items() if k not in keys}


def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Безопасно получить значение из словаря.
    
    Args:
        data: Словарь
        key: Ключ
        default: Значение по умолчанию
        
    Returns:
        Any: Значение или default
        
    Example:
        >>> safe_get({"name": "John"}, "name")
        'John'
        >>> safe_get({"name": "John"}, "age", 18)
        18
    """
    return data.get(key, default)


# ========== РАБОТА СО СПИСКАМИ ==========

def chunk_list(items: List[Any], size: int) -> List[List[Any]]:
    """
    Разбить список на чанки.
    
    Args:
        items: Исходный список
        size: Размер чанка
        
    Returns:
        List[List[Any]]: Список чанков
        
    Example:
        >>> chunk_list([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]
    """
    return [items[i:i + size] for i in range(0, len(items), size)]


def unique_items(items: List[Any]) -> List[Any]:
    """
    Получить уникальные элементы списка (сохраняя порядок).
    
    Args:
        items: Исходный список
        
    Returns:
        List[Any]: Список с уникальными элементами
        
    Example:
        >>> unique_items([1, 2, 2, 3, 3, 3])
        [1, 2, 3]
    """
    seen = set()
    return [x for x in items if x not in seen and not seen.add(x)]


# ========== РАБОТА С КЛАССАМИ ==========

def class_name(obj: Any) -> str:
    """
    Получить имя класса объекта.
    
    Args:
        obj: Объект
        
    Returns:
        str: Имя класса
        
    Example:
        >>> class_name(Book())
        'Book'
    """
    return obj.__class__.__name__


def get_attributes(obj: Any, include_private: bool = False) -> Dict[str, Any]:
    """
    Получить все атрибуты объекта.
    
    Args:
        obj: Объект
        include_private: Включать приватные атрибуты
        
    Returns:
        Dict[str, Any]: Словарь атрибутов
        
    Example:
        >>> get_attributes(book)
        {'title': 'Clean Code', 'author': 'Robert Martin', ...}
    """
    attrs = {}
    for key in dir(obj):
        if key.startswith('_') and not include_private:
            continue
        if not callable(getattr(obj, key)):
            attrs[key] = getattr(obj, key)
    return attrs
