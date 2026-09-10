"""
Тест для OpenLibraryClient.
"""

import pytest
import asyncio
from src.library_catalog.external.openlibrary import OpenLibraryClient


@pytest.mark.asyncio
async def test_openlibrary_client():
    """Тест OpenLibraryClient."""
    client = OpenLibraryClient()

    try:
        # Тест по ISBN
        data = await client.search_by_isbn("9780132350884")
        assert data is not None
        assert "title" in data

        # Тест по title+author
        data = await client.search_by_title_author(
            "Clean Code",
            "Robert Martin"
        )
        assert data is not None
        assert "title" in data

    finally:
        await client.close()