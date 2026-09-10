"""
Настройка логирования для приложения.
"""

import logging
import sys


def setup_logging() -> None:
    """
    Настроить логирование приложения.
    
    Настройки:
    - Уровень логирования: INFO
    - Формат: время - имя - уровень - сообщение
    - Вывод в stdout
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
