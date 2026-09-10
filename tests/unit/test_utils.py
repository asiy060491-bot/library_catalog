#!/usr/bin/env python3
"""
Тест для проверки утилит.
"""

from src.library_catalog.utils import (
    slugify,
    get_current_year,
    is_valid_uuid,
    generate_uuid,
    truncate_text,
    filter_dict,
    chunk_list,
    format_datetime,
    safe_get,
    unique_items,
)

def test_utils():
    """Тестирование всех утилит."""
    print("=" * 50)
    print("ТЕСТИРОВАНИЕ УТИЛИТ")
    print("=" * 50)
    
    # 1. slugify
    result = slugify("Hello World!")
    print(f"✅ slugify('Hello World!'): {result}")
    
    # 2. get_current_year
    result = get_current_year()
    print(f"✅ get_current_year(): {result}")
    
    # 3. is_valid_uuid
    result = is_valid_uuid("123e4567-e89b-12d3-a456-426614174000")
    print(f"✅ is_valid_uuid (valid): {result}")
    
    result = is_valid_uuid("invalid-uuid")
    print(f"✅ is_valid_uuid (invalid): {result}")
    
    # 4. generate_uuid
    result = generate_uuid()
    print(f"✅ generate_uuid(): {result}")
    
    # 5. truncate_text
    result = truncate_text("Very long text that needs truncation", 20)
    print(f"✅ truncate_text(): {result}")
    
    # 6. filter_dict
    result = filter_dict({"a": 1, "b": 2, "c": 3}, ["a", "c"])
    print(f"✅ filter_dict(): {result}")
    
    # 7. chunk_list
    result = chunk_list([1, 2, 3, 4, 5], 2)
    print(f"✅ chunk_list(): {result}")
    
    # 8. format_datetime
    from datetime import datetime
    now = datetime.now()
    result = format_datetime(now)
    print(f"✅ format_datetime(): {result}")
    
    # 9. safe_get
    data = {"name": "John", "age": 30}
    result = safe_get(data, "name")
    print(f"✅ safe_get(name): {result}")
    result = safe_get(data, "email", "default@email.com")
    print(f"✅ safe_get(email, default): {result}")
    
    # 10. unique_items
    result = unique_items([1, 2, 2, 3, 3, 3, 4])
    print(f"✅ unique_items(): {result}")
    
    print("\n" + "=" * 50)
    print("🎉 Все утилиты работают!")
    print("=" * 50)

if __name__ == "__main__":
    test_utils()
