"""
Core модуль с базовыми компонентами приложения.
"""

from .exceptions import (
    AppException,
    NotFoundException,
    ValidationException,
    ConflictException,
    UnauthorizedException,
    ForbiddenException,
    ServiceUnavailableException,
    GatewayTimeoutException,
)

__all__ = [
    "AppException",
    "NotFoundException",
    "ValidationException",
    "ConflictException",
    "UnauthorizedException",
    "ForbiddenException",
    "ServiceUnavailableException",
    "GatewayTimeoutException",
]