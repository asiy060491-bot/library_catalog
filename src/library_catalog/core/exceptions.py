"""
Базовые исключения и обработчики ошибок для приложения.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    """
    Базовое исключение приложения.

    Все пользовательские исключения должны наследоваться от этого класса.
    """

    def __init__(self, message: str, status_code: int = 400):
        """
        Инициализация базового исключения.

        Args:
            message: Сообщение об ошибке
            status_code: HTTP статус код (по умолчанию 400)
        """
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(AppException):
    """
    Исключение: ресурс не найден.

    Возникает когда запрашиваемый ресурс отсутствует в системе.
    """

    def __init__(self, resource: str, identifier: any):
        """
        Инициализация исключения о ненайденном ресурсе.

        Args:
            resource: Тип ресурса (например, "Book", "Author")
            identifier: Идентификатор ресурса (ID, ISBN, имя)
        """
        super().__init__(
            message=f"{resource} with id '{identifier}' not found",
            status_code=404,
        )
        self.resource = resource
        self.identifier = identifier


def register_exception_handlers(app: FastAPI) -> None:
    """
    Зарегистрировать обработчики исключений для FastAPI приложения.

    Args:
        app: FastAPI приложение
    """

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        """
        Обработчик для AppException.

        Returns:
            JSONResponse с деталями ошибки
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )

    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request: Request, exc: NotFoundException):
        """
        Обработчик для NotFoundException.

        Returns:
            JSONResponse с деталями ошибки
        """
        return JSONResponse(
            status_code=404,
            content={"detail": exc.message},
        )