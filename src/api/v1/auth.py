"""
Обрабатывает входящие запросы на /auth/*
"""

from flask import Blueprint, Response, jsonify
from flask_jwt_extended import jwt_required

from schemas import SignInSchema, SignUpSchema, UpdatePasswordSchema
from services import AuthService
from utils import RequestValidator

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/secure", methods=["GET", "POST"])
@jwt_required()
def test_route():
    """Роут для проверки доступа только с access токеном"""
    return jsonify("secure")


@auth_bp.route("/sign-up", methods=["POST"])
@RequestValidator.validate_body(SignUpSchema)
def sign_up(data, auth_service: AuthService) -> Response:
    """Запрос на регистрацию пользователя
    data это словарь данных возвращаемым декоратором @validate_request.
    Объект типа UserService попадает сюда с помощью DI, реализованной библиотекой flask_injector
    Подробности: https://github.com/alecthomas/flask_injector
    ---
    post:
      description: Регистрация пользователя
      requestBody:
        content:
          application/json:
            schema: SignUpSchema
      responses:
        200:
          description: Пользователь успешно создан
          content:
            application/json:
              schema: UserResponseSchema
        400:
          description: Некорректный запрос
      tags:
        - Аккаунты пользователей
    """
    return auth_service.sign_up(data)


@auth_bp.route("/sign-in", methods=["POST"])
@RequestValidator.validate_body(schema=SignInSchema)
def sign_in(data, auth_service: AuthService) -> Response:
    """Запрос на вход пользователя в систему
    ---
    post:
      description: Вход пользователя в аккаунт
      requestBody:
        content:
          application/json:
            schema: SignInSchema
      responses:
        200:
          description: Успешный вход
          content:
            application/json:
              schema: JWTResponseSchema
        400:
          description: Некорректный запрос
      tags:
        - Аккаунты пользователей
    """
    return auth_service.sign_in(data)


@auth_bp.route("/refresh", methods=["GET"])
@jwt_required(refresh=True)
def refresh(auth_service: AuthService) -> Response:
    """Запрос на обновление access токена
    ---
    get:
      description: Получение новых токенов по refresh токену
      security:
        - jwt_token: []
      responses:
        200:
          description: Новые токены успешно получены
          content:
            application/json:
              schema: JWTResponseSchema
        400:
          description: Некорректный запрос
        401:
          description: Необходима авторизация
      tags:
        - Аккаунты пользователей
    """
    return auth_service.refresh_jwt()


@auth_bp.route("/logout", methods=["GET"])
@jwt_required()
def logout(auth_service: AuthService) -> Response:
    """Запрос на выход из аккаунта на текущем устройстве
    ---
    get:
      description: Выход из аккаунта
      security:
        - jwt_token: []
      responses:
        200:
          description: Успешный выход из аккаунта
        400:
          description: Некорректный запрос
        401:
          description: Необходима авторизация
      tags:
        - Аккаунты пользователей
    """
    return auth_service.logout()


@auth_bp.route("/logout_all", methods=["GET"])
@jwt_required()
def logout_all(auth_service: AuthService) -> Response:
    """Запрос на выход из аккаунта со всех устройств
    ---
    get:
      description: Выход из аккаунта на всех устройствах
      security:
        - jwt_token: []
      responses:
        200:
          description: Успешный выход из аккаунта на всех устройствах
        400:
          description: Некорректный запрос
        401:
          description: Необходима авторизация
      tags:
        - Аккаунты пользователей
    """
    return auth_service.logout_all()


@auth_bp.route("/login_history", methods=["GET"])
@jwt_required()
def login_history(auth_service: AuthService) -> Response:
    """Запрос истории посещений
    ---
    get:
      description: Получение информации об истории посещений
      security:
        - jwt_token: []
      responses:
        200:
          description: История посещений успешно получены
        400:
          description: Некорректный запрос
        401:
          description: Необходима авторизация
      tags:
        - Аккаунты пользователей
    """
    return auth_service.login_history()


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me(auth_service: AuthService) -> Response:
    """Запрос пользовательского профиля
    ---
    get:
      description: Получение информации об учетной записи
      security:
        - jwt_token: []
      responses:
        200:
          description: Сведения об учётной записи успешно получены
        400:
          description: Некорректный запрос
        401:
          description: Необходима авторизация
      tags:
        - Аккаунты пользователей
    """
    return auth_service.me()


@auth_bp.route("/change_password", methods=["POST"])
@jwt_required(fresh=True)
@RequestValidator.validate_body(schema=UpdatePasswordSchema)
def change_password(data, auth_service: AuthService) -> Response:
    """Запрос пользовательского профиля.
    Смена пароля это важная операция, поэтому о первых для неё сделаем отдельный endpoint и обработчики,
    а также ограничиваем доступ к ней, только access токен с fresh флагом будут иметь доступ, т.е токен
    полученный только при вводе логина/пароля, т.е перед сменой пароля пользователю нужно будет сначала
    залогиниться, если он давно этого не делал.
    ---
    post:
      description: Изменение пароля учетной записи
      security:
        - jwt_token: []
      requestBody:
        content:
          application/json:
            schema: UpdatePasswordSchema
      responses:
        200:
          description: Пароль успешно изменён
        400:
          description: Некорректный запрос
        401:
          description: Необходима авторизация
      tags:
        - Аккаунты пользователей
    """
    return auth_service.change_password(data)


@auth_bp.route("/authorize", methods=["GET"])
@jwt_required()
def authorize(auth_service: AuthService) -> Response:
    """Запрос на авторизацию
    get:
      description: Авторизация, получение списка доступных ролей
      security:
        - jwt_token: []
      responses:
        200:
          description: Список ролей успешно получен
          type: array
            items:
              type: string
        400:
          description: Некорректный запрос
        401:
          description: Необходима авторизация
      tags:
        - Аккаунты пользователей
    """
    return auth_service.authorize()
