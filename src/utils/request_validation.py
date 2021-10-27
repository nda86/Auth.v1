from functools import wraps

from flask import request
from marshmallow import ValidationError, EXCLUDE

from core.logger import auth_logger
from exceptions import ApiValidationException


class RequestValidator:
    """Вспомогательный класс, проводит валидацию параметров во входящем запросе.
    Можно вместо этого класса использовать готовую библиотеку аналог.
    """

    @classmethod
    def validate_body(cls, schema):
        """Метод возвращает декоратор для валидации body
        :type schema: модель-схема описывает формат валидных входящих данных
        """
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                try:
                    if request.json:
                        data = schema().load(request.json, unknown=EXCLUDE)
                    elif request.form:
                        data = schema().load(request.form, unknown=EXCLUDE)
                    else:
                        auth_logger.error("В запросе нет данных")
                        raise ApiValidationException("Data not found")
                except ValidationError as err:
                    auth_logger.error(f"Ошибка валидации запроса {err.messages}")
                    raise ApiValidationException(err.messages)
                return f(*args, data=data, **kwargs)
            return decorated_function
        return decorator

    @classmethod
    def validate_view_args(cls, schema):
        """Метод возвращает декоратор для валидации аргументов из строки запроса
        :type schema: модель-схема описывает формат валидных входящих данных
        """
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                try:
                    if request.view_args:
                        schema().load(request.view_args, unknown=EXCLUDE)
                    else:
                        auth_logger.error("В запросе нет данных")
                        raise ApiValidationException("Data not found")
                except ValidationError as err:
                    auth_logger.error(f"Ошибка валидации запроса {err.messages}")
                    raise ApiValidationException(err.messages)
                return f(*args, **kwargs)
            return decorated_function
        return decorator
