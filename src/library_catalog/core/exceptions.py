"""
Базовые исключения для всего приложения.

Содержит фундаментальные классы исключений,
от которых наследуются все остальные исключения.
"""

from typing import Any, Optional
from uuid import UUID


class AppException(Exception):
    """
    Базовое исключение приложения.
    
    Все пользовательские исключения должны наследоваться от этого класса.
    
    Attributes:
        message: Сообщение об ошибке
        status_code: HTTP статус код (для API)
        details: Дополнительные детали ошибки
    """
    
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        details: Optional[dict] = None,
    ):
        """
        Инициализация базового исключения.
        
        Args:
            message: Сообщение об ошибке
            status_code: HTTP статус код (по умолчанию 400)
            details: Дополнительные детали ошибки
        """
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)
    
    def to_dict(self) -> dict:
        """
        Преобразовать исключение в словарь для API ответа.
        
        Returns:
            dict: Словарь с информацией об ошибке
        """
        return {
            "error": self.__class__.__name__,
            "message": self.message,
            "status_code": self.status_code,
            "details": self.details,
        }


class NotFoundException(AppException):
    """
    Исключение: ресурс не найден.
    
    Возникает когда запрашиваемый ресурс отсутствует в системе.
    """
    
    def __init__(
        self,
        resource: str,
        identifier: Optional[Any] = None,
        message: Optional[str] = None,
    ):
        """
        Инициализация исключения о ненайденном ресурсе.
        
        Args:
            resource: Тип ресурса (например, "Book", "Author")
            identifier: Идентификатор ресурса (ID, ISBN, имя)
            message: Пользовательское сообщение (опционально)
        """
        if message is None:
            if identifier:
                message = f"{resource} with identifier '{identifier}' not found"
            else:
                message = f"{resource} not found"
        
        super().__init__(
            message=message,
            status_code=404,
        )
        self.resource = resource
        self.identifier = identifier


class ValidationException(AppException):
    """
    Исключение: ошибка валидации данных.
    
    Возникает когда переданные данные не проходят валидацию.
    """
    
    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        value: Optional[Any] = None,
    ):
        """
        Инициализация исключения валидации.
        
        Args:
            message: Сообщение об ошибке
            field: Поле, в котором произошла ошибка
            value: Значение, которое вызвало ошибку
        """
        details = {}
        if field:
            details["field"] = field
        if value is not None:
            details["value"] = value
        
        super().__init__(
            message=message,
            status_code=422,
            details=details,
        )
        self.field = field
        self.value = value


class ConflictException(AppException):
    """
    Исключение: конфликт данных.
    
    Возникает когда операция противоречит существующим данным.
    """
    
    def __init__(
        self,
        message: str,
        resource: Optional[str] = None,
        identifier: Optional[Any] = None,
    ):
        """
        Инициализация исключения конфликта.
        
        Args:
            message: Сообщение об ошибке
            resource: Тип ресурса
            identifier: Идентификатор ресурса
        """
        details = {}
        if resource:
            details["resource"] = resource
        if identifier:
            details["identifier"] = identifier
        
        super().__init__(
            message=message,
            status_code=409,
            details=details,
        )
        self.resource = resource
        self.identifier = identifier


class UnauthorizedException(AppException):
    """
    Исключение: неавторизованный доступ.
    
    Возникает когда пользователь не авторизован.
    """
    
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(
            message=message,
            status_code=401,
        )


class ForbiddenException(AppException):
    """
    Исключение: доступ запрещен.
    
    Возникает когда у пользователя нет прав.
    """
    
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(
            message=message,
            status_code=403,
        )


class ServiceUnavailableException(AppException):
    """
    Исключение: сервис недоступен.
    
    Возникает когда внешний сервис не отвечает.
    """
    
    def __init__(self, service: str, message: Optional[str] = None):
        """
        Инициализация исключения о недоступном сервисе.
        
        Args:
            service: Имя сервиса
            message: Пользовательское сообщение
        """
        if message is None:
            message = f"Service '{service}' is currently unavailable"
        
        super().__init__(
            message=message,
            status_code=503,
        )
        self.service = service


class GatewayTimeoutException(AppException):
    """
    Исключение: таймаут шлюза.
    
    Возникает когда внешний сервис не отвечает в течение таймаута.
    """
    
    def __init__(self, service: str, timeout: float):
        """
        Инициализация исключения о таймауте.
        
        Args:
            service: Имя сервиса
            timeout: Время таймаута в секундах
        """
        super().__init__(
            message=f"Gateway timeout: {service} did not respond within {timeout}s",
            status_code=504,
        )
        self.service = service
        self.timeout = timeout
