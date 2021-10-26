import functools
import typing as t

from flask import request, Response, jsonify, abort
from marshmallow import ValidationError, EXCLUDE
from sqlalchemy.exc import SQLAlchemyError
from injector import inject

from src.exceptions import ApiValidationException, WrongCredentials, RefreshTokenInvalid, DBMaintainException
from src.core.logger import auth_logger
from src import db
from src.models import LoginHistory, User
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
                        auth_logger.error("В запросе нет данных")
                        raise ApiValidationException("Data not found")
                except ValidationError as err:
                    auth_logger.error(f"Ошибка валидации запроса {err.messages}")
                    raise ApiValidationException(err.messages)
                return f(*args, data=data, **kwargs)

            return decorated_function

        return decorator

    @staticmethod
    def _make_response(data: t.Union[dict, str, list]) -> Response:
        """Метод формирует и возвращает окончательный Response"""
        return jsonify(data)

    def _make_tokens(self, user, fresh: t.Optional[bool] = False) -> tuple[str, str]:
        """Формируем токены"""
        access_token, refresh_token = self.token_service.gen_tokens(user, fresh)
        # сохраняем рефреш токен в бд
        self.token_service.save_refresh_token(token=refresh_token, user_id=user.id)
        auth_logger.debug(f"Создана пар токенов для пользователя с id {user.id}")
        return access_token, refresh_token

    @staticmethod
    def _add_login_history(user: User) -> None:
        """
        Добавляем запись в историю входов пользователя
        """
        rec_login_history = LoginHistory()
        rec_login_history.user_id = user.id
        rec_login_history.user_agent = request.user_agent.string
        rec_login_history.ip = request.remote_addr
        db.session.add(rec_login_history)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            # в случае ошибка процесс логина не прерываем, а просто заносим данные в лог в лог
            auth_logger.error(f"Ошибка при добавлении записи в историю посещений\n{str(e)}")
            auth_logger.error(f"{rec_login_history.user_id=}/n{rec_login_history.user_agent=}\n{rec_login_history.ip}")

    def sign_in(self, data: dict) -> Response:
        """Метод выполняет процедуру входа пользователя в сервис
        data - провалидированные данные полученные от пользователя
        """
        user = self.user_service.get_by_username(data["username"])
        if not user or not user.verify_password(data["password"]):
            auth_logger.debug("Попытка входа с неверными учётными данными")
            raise WrongCredentials("Wrong username or password")
        self._add_login_history(user)
        access_token, refresh_token = self._make_tokens(user, fresh=True)
        return self._make_response(dict(access_token=access_token, refresh_token=refresh_token))

    def sign_up(self, data: dict) -> Response:
        """Метод выполняет процедуру регистрации пользователя в сервисе
        data - провалидированные данные полученные от пользователя
        """
        user = self.user_service.create_user(data)
        if user:
            return self._make_response({f"user:{user.id}": "created"})
        else:
            return self._make_response({f"user:{user.id}": "not created"})

    def refresh_jwt(self) -> Response:
        """Метод выполняет процедуру refresh jwt.
        Если refresh token из запроса есть в бд то всё ок, удаляем его из бд и выдаем новые токены, а если нет то отказ
        """
        is_exists, old_refresh_token_jti, user = self.token_service.is_exists_refresh_token()
        if is_exists:
            self.token_service.remove_refresh_token(token_jti=old_refresh_token_jti, user_id=user.id)
            access_token, refresh_token = self._make_tokens(user)
            return self._make_response(dict(access_token=access_token, refresh_token=refresh_token))
        else:
            auth_logger.debug("Попытка получить новый access token по несуществующему refresh токену")
            raise RefreshTokenInvalid(
                "Refresh token not found or was stolen. Please make sign-in and logout all other devices"
            )

    def logout(self) -> Response:
        """Метод выполняет процедуру выхода из аккаунта с "этого устройства".
        Ддя этого удаляем refresh токен связанный с access токеном из запроса
        """
        refresh_jti = self.token_service.get_claim_from_token("rt")
        user_id = self.token_service.get_claim_from_token("sub")
        self.token_service.remove_refresh_token(token_jti=refresh_jti, user_id=user_id)
        return self._make_response({"logout": "ok"})

    def logout_all(self) -> Response:
        """Метод выполняет процедуру выхода из аккаунта "со всех устройств".
        Для этого просто удаляем все refresh токены пользователя
        """
        user_id = self.token_service.get_claim_from_token("sub")
        self.token_service.remove_refresh_tokens(user_id=user_id)
        return self._make_response({"logout_all": "ok"})

    def login_history(self) -> Response:
        """Метод возвращает историю посещений пользователя".
        """
        user_id = self.token_service.get_claim_from_token("sub")  # получаем id текущего пользователя
        query = db.session.query(LoginHistory).filter(LoginHistory.user_id == user_id)
        try:
            history_log = query.all()
        except SQLAlchemyError as e:
            auth_logger.error(f"Ошибка при запросе истории логинов пользователя {user_id}\n{str(e)}")
            raise DBMaintainException()
        else:
            return self._make_response([log.dict() for log in history_log])

    def me(self) -> Response:
        """Метод возвращает профиль пользователя".
        """
        user_id = self.token_service.get_claim_from_token("sub")  # получаем id текущего пользователя
        user = self.user_service.get_by_id(user_id)
        if not user:
            abort(404, description="Пользователь не найден")
        return self._make_response(user.dict())

    def change_password(self, data: dict) -> Response:
        """Метод для смены пароля"
        data - провалидированные данные полученные от пользователя.
        """
        user_id = self.token_service.get_claim_from_token("sub")  # получаем id текущего пользователя
        user = self.user_service.get_by_id(user_id)
        if not user:
            auth_logger.debug(f"Попытка смены пароля для пользователя не существующего в бд\n{user.id=}")
            abort(404, description="Пользователь не найден")
        self.user_service.change_password(user=user, password=data["password"])
        auth_logger.debug(f"Пароль для пользователя {user.id} изменён")
        return self._make_response("Password successfully changed")
