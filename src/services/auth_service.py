import functools
import typing as t

from flask import request, Response, jsonify
from marshmallow import ValidationError, EXCLUDE
from injector import inject

from src.exceptions import ApiValidationException, WrongCredentials, RefreshTokenInvalid
from .user_service import UserService
from .jwt_service import JWTService


class AuthService:
    """
    Сервис отвечает за работу с задачами авторизации и аунтентификации.
    Предоставляет методы для обработки запросов на регистрацию пользователя, вход пользователя в систему,
    выход, валидацию входящего запроса и т.д Используется при обработке запросов на /auth/*
    """

    @inject
    def __init__(self, user_service: UserService, token_service: JWTService):
        self.user_service = user_service
        self.token_service = token_service

    @classmethod
    def validate_request(cls, schema):
        """Метод возвращает декоратор для валидации входящего запроса
        :type schema: модель-схема описывает формат валидных входящих данных
        """

        def decorator(f):
            @functools.wraps(f)
            def decorated_function(*args, **kwargs):
                try:
                    if request.json:
                        data = schema().load(request.json, unknown=EXCLUDE)
                    elif request.form:
                        data = schema().load(request.form, unknown=EXCLUDE)
                    else:
                        raise ApiValidationException("Data not found")
                except ValidationError as err:
                    raise ApiValidationException(err.messages)
                return f(*args, data=data, **kwargs)

            return decorated_function

        return decorator

    def _make_response(self, access_token: str, refresh_token: str) -> Response:
        """Метод формирует и возвращает окончательный Response"""
        return jsonify(access_token=access_token, refresh_token=refresh_token)

    def _make_tokens(self, user, fresh: t.Optional[bool] = False) -> tuple[str, str]:
        """Формируем токены"""
        access_token = self.token_service.gen_access_token(user, fresh)
        refresh_token = self.token_service.gen_refresh_token(user)
        # сохраняем рефреш токен в бд
        self.token_service.save_refresh_token(token=refresh_token, user_id=user.id)
        return access_token, refresh_token

    def sign_in(self, data: dict) -> Response:
        """Метод выполняет процедуру входа пользователя в сервис
        data - провалидированные данные полученные от пользователя
        """
        user = self.user_service.get_by_username(data["username"])
        if not user or not user.verify_password(data["password"]):
            raise WrongCredentials("Wrong username or password")
        access_token, refresh_token = self._make_tokens(user, fresh=True)
        return self._make_response(access_token, refresh_token)

    def refresh_jwt(self):
        """Метод выполняет процедуру refresh jwt.
        Если refresh token есть в бд то всё ок, выдаем новые токены, а если нет то отказ
        """
        is_exists, user = self.token_service.is_exists_refresh_token()
        if is_exists:
            access_token, refresh_token = self._make_tokens(user)
            return self._make_response(access_token, refresh_token)
        else:
            raise RefreshTokenInvalid("Refresh token not found or was revoked")
