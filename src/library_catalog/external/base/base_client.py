"""
Базовый HTTP клиент для работы с внешними API.

Предоставляет абстрактный класс с:
- Retry логикой с exponential backoff
- Единой обработкой ошибок
- Timeout management
- Логированием
"""

from abc import ABC, abstractmethod
import httpx
import logging
import time
from typing import Dict, Optional, Any


class BaseApiClient(ABC):
    """
    Базовый класс для HTTP клиентов внешних API.
    
    Включает:
    - Retry логику с exponential backoff
    - Обработку ошибок
    - Логирование
    - Timeout management
    
    Attributes:
        base_url: Базовый URL внешнего API
        timeout: Таймаут запроса в секундах
        retries: Количество попыток при ошибке
        backoff: Начальная задержка между попытками
        _client: HTTP клиент для выполнения запросов
        logger: Логгер для клиента
    """
    
    def __init__(
        self,
        base_url: str,
        timeout: float = 10.0,
        retries: int = 3,
        backoff: float = 0.5,
        max_backoff: float = 30.0,
    ):
        """
        Инициализация базового HTTP клиента.
        
        Args:
            base_url: Базовый URL внешнего API
            timeout: Таймаут запроса в секундах (по умолчанию 10.0)
            retries: Количество попыток при ошибке (по умолчанию 3)
            backoff: Начальная задержка между попытками (по умолчанию 0.5)
            max_backoff: Максимальная задержка между попытками (по умолчанию 30.0)
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries
        self.backoff = backoff
        self.max_backoff = max_backoff
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            follow_redirects=True,
        )
        self.logger = logging.getLogger(self.client_name())
    
    @abstractmethod
    def client_name(self) -> str:
        """
        Имя клиента для логирования.
        
        Returns:
            str: Уникальное имя клиента
        """
        pass
    
    def _build_url(self, path: str) -> str:
        """
        Построить полный URL.
        
        Args:
            path: Относительный путь
            
        Returns:
            str: Полный URL
        """
        if not path.startswith("/"):
            path = "/" + path
        return self.base_url + path
    
    def _calculate_backoff(self, attempt: int) -> float:
        """
        Рассчитать задержку с exponential backoff.
        
        Args:
            attempt: Номер попытки (начиная с 0)
            
        Returns:
            float: Время задержки в секундах
        """
        wait_time = min(self.backoff * (2 ** attempt), self.max_backoff)
        # Добавляем небольшой случайный фактор для избежания "thundering herd"
        wait_time = wait_time * (0.8 + 0.4 * (time.time() % 1))
        return wait_time
    
    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Выполнить HTTP запрос с retry логикой.
        
        Args:
            method: HTTP метод (GET, POST, PUT, DELETE)
            path: Относительный путь
            params: Параметры запроса
            json: JSON данные для отправки
            headers: HTTP заголовки
            
        Returns:
            Dict[str, Any]: Ответ API в виде JSON
            
        Raises:
            httpx.TimeoutException: При таймауте после всех попыток
            httpx.HTTPStatusError: При HTTP ошибке после всех попыток
            Exception: При других ошибках
        """
        url = self._build_url(path)
        
        for attempt in range(self.retries):
            try:
                self.logger.debug(
                    f"{method} {url} params={params} (attempt {attempt + 1}/{self.retries})"
                )
                
                response = await self._client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                    headers=headers,
                )
                
                # Проверяем статус ответа
                response.raise_for_status()
                
                # Пытаемся распарсить JSON
                try:
                    return response.json()
                except ValueError as e:
                    self.logger.error(f"Failed to parse JSON response: {e}")
                    raise httpx.HTTPError(f"Invalid JSON response: {response.text[:100]}")
            
            except httpx.TimeoutException as e:
                # Таймаут - повторяем
                if attempt == self.retries - 1:
                    self.logger.error(
                        f"Timeout after {self.retries} attempts for {method} {url}"
                    )
                    raise
                
                wait_time = self._calculate_backoff(attempt)
                self.logger.warning(
                    f"Timeout on attempt {attempt + 1}, retrying in {wait_time:.2f}s..."
                )
                await self._sleep(wait_time)
            
            except httpx.HTTPStatusError as e:
                # 5xx ошибки - повторяем
                if e.response.status_code >= 500 and attempt < self.retries - 1:
                    wait_time = self._calculate_backoff(attempt)
                    self.logger.warning(
                        f"Server error {e.response.status_code} on attempt {attempt + 1}, "
                        f"retrying in {wait_time:.2f}s..."
                    )
                    await self._sleep(wait_time)
                else:
                    self.logger.error(
                        f"HTTP error on attempt {attempt + 1}: {e.response.status_code} - {e.response.text[:100]}"
                    )
                    raise
            
            except httpx.HTTPError as e:
                # Другие HTTP ошибки
                if attempt < self.retries - 1:
                    wait_time = self._calculate_backoff(attempt)
                    self.logger.warning(
                        f"HTTP error on attempt {attempt + 1}: {e}, "
                        f"retrying in {wait_time:.2f}s..."
                    )
                    await self._sleep(wait_time)
                else:
                    self.logger.error(f"HTTP error after {self.retries} attempts: {e}")
                    raise
            
            except Exception as e:
                # Неизвестные ошибки
                self.logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
                if attempt == self.retries - 1:
                    raise
                wait_time = self._calculate_backoff(attempt)
                await self._sleep(wait_time)
    
    async def _sleep(self, seconds: float) -> None:
        """
        Асинхронная задержка.
        
        Args:
            seconds: Время задержки в секундах
        """
        await asyncio.sleep(seconds)
    
    async def _get(self, path: str, **kwargs) -> Dict[str, Any]:
        """
        Выполнить GET запрос.
        
        Args:
            path: Относительный путь
            **kwargs: Дополнительные параметры для _request
            
        Returns:
            Dict[str, Any]: Ответ API
        """
        return await self._request("GET", path, **kwargs)
    
    async def _post(self, path: str, **kwargs) -> Dict[str, Any]:
        """
        Выполнить POST запрос.
        
        Args:
            path: Относительный путь
            **kwargs: Дополнительные параметры для _request
            
        Returns:
            Dict[str, Any]: Ответ API
        """
        return await self._request("POST", path, **kwargs)
    
    async def _put(self, path: str, **kwargs) -> Dict[str, Any]:
        """
        Выполнить PUT запрос.
        
        Args:
            path: Относительный путь
            **kwargs: Дополнительные параметры для _request
            
        Returns:
            Dict[str, Any]: Ответ API
        """
        return await self._request("PUT", path, **kwargs)
    
    async def _delete(self, path: str, **kwargs) -> Dict[str, Any]:
        """
        Выполнить DELETE запрос.
        
        Args:
            path: Относительный путь
            **kwargs: Дополнительные параметры для _request
            
        Returns:
            Dict[str, Any]: Ответ API
        """
        return await self._request("DELETE", path, **kwargs)
    
    async def close(self) -> None:
        """
        Закрыть HTTP клиент и освободить ресурсы.
        """
        await self._client.aclose()
        self.logger.info(f"{self.client_name()} closed")
    
    async def __aenter__(self):
        """Контекстный менеджер - вход."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Контекстный менеджер - выход."""
        await self.close()
