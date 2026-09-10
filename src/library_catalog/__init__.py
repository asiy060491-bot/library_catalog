"""
Library Catalog Application.

Библиотечный каталог с REST API.
"""

__version__ = "1.0.0"

from .api.v1 import router
from .core.config import settings
from .core.database import get_db, init_db, dispose_engine

__all__ = [
    "__version__",
    "router",
    "settings",
    "get_db",
    "init_db",
    "dispose_engine",
]