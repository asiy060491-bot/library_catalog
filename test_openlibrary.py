"""
Тест из задания.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.library_catalog.external.openlibrary import OpenLibraryClient


async def test():
    client = OpenLibraryClient()

    try:
        # Тест по ISBN
        print("=" * 60)
        print("ТЕСТ ПО ISBN")
        print("=" * 60)
        data = await client.search_by_isbn("9780132350884")
        print(f"Found: {data}")

        # Тест по title+author
        print("\n" + "=" * 60)
        print("ТЕСТ ПО НАЗВАНИЮ И АВТОРУ")
        print("=" * 60)
        data = await client.search_by_title_author(
            "Clean Code",
            "Robert Martin"
        )
        print(f"Found: {data}")

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(test())