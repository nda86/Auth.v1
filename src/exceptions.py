"""
Описываем собственные классы исключений.
Идея в том чтобы при возникновении определённых ситуаций кидать свои исключения, с определённой структурой.
Сейчас просто просто прописываем свои атрибуты, к которым можем обращаться в обработчиках исключений.
"""

import json
import typing as t
from http import HTTPStatus

from flask import Flask
from werkzeug.exceptions import HTTPException

import const_messages


class DBValidationException(HTTPException):
    """EXC бросаем его если пользователь при регистрации ввёл
    данные которые не проходят валидацию в бд"""
    code = HTTPStatus.BAD_REQUEST
    name = "CONSTRANT: Already exists"

    def __init__(self, description: str):
        self.description = description
        super().__init__()


class ApiValidationException(HTTPException):
    """EXC бросаем его если пользователь при регистрации ввёл
    данные которые не проходят валидацию в API"""
    code = HTTPStatus.BAD_REQUEST
    name = "API Validation error"

    def __init__(self, description: str):
        self.description = description
        super().__init__()


class DBMaintainException(HTTPException):
    """EXC бросаем его если при работе с каким то хранилищем postgres, redis и т.д случилась непредвиденная ошибка.
    Клиенту просто отдаём код 500 с общим описание что-то пошло не так. А в логах фиксируем реальную ошибку."""
    code = HTTPStatus.INTERNAL_SERVER_ERROR
    name = "System error in database"

    def __init__(self, description: t.Optional[str] = None):
        self.description = description or const_messages.EXC_SOMETHING_WENT_WRONG
        super().__init__()


class WrongCredentials(HTTPException):
    """EXC бросаем его если пользователь при аутентификации указал неверный логи или пароль"""
    code = HTTPStatus.UNAUTHORIZED
    name = "Wrong credentials"

    def __init__(self, description: str):
        self.description = description
        super().__init__()


class RefreshTokenInvalid(HTTPException):
    """EXC бросаем его если refresh token отсутствует в БД, то есть считаем его недействительным"""
    code = HTTPStatus.UNAUTHORIZED
    name = "Refresh token is unavailable"

    def __init__(self, description: str):
        self.description = description
        super().__init__()


def init_error_handler(app: Flask):
    """Подключаем к приложению обработчики ошибок"""

    @app.errorhandler(HTTPException)
    def json_exc_handler(e: HTTPException):
        """Отлавливает все HTTPException и отдает ответ об ошибке в формате json"""
        resp = e.get_response()
        resp.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description
        })
        resp.content_type = "application/json"
        return resp
