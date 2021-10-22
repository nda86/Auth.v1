import functools

from flask import request, abort, jsonify
from marshmallow import ValidationError, EXCLUDE
from injector import inject


from src.exceptions import ApiValidationException, WrongCredentials
from .user_service import UserService
from .jwt_service import JWTService


class AuthService:

    @inject
    def __init__(self, user_service: UserService, token_service: JWTService):
        self.user_service = user_service
        self.token_service = token_service

    @classmethod
    def validate_request(cls, schema):
        """Метод возвращает декоратор для валидации входящего запроса"""
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

    def sign_in(self, data):
        """Метод выполняет процедуру входа пользователя в сервис"""
        user = self.user_service.get_by_username(data["username"])
        if not user or not user.verify_password(data["password"]):
            raise WrongCredentials("Wrong username or password")
        access_token = self.token_service.gen_access_token(user)
        return jsonify({"access_token": access_token})

    def _gen_jwt(self):
        """Метод генерирует и возвращает jwt"""


