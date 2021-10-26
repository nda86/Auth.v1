"""
Обрабатывает входящие запросы на /auth/*
"""

from flask import Blueprint, jsonify, Response
from flask_jwt_extended import jwt_required

from src.schemas.user_schema import SignUpSchema, SignInSchema, UpdatePasswordSchema
from src.services import AuthService


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/secure", methods=["GET", "POST"])
@jwt_required()
def test_route():
    """Роут для проверки доступа только с access токеном"""
    return jsonify("secure")


@auth_bp.route("/sign-up", methods=["POST"])
@AuthService.validate_request(SignUpSchema)
def sign_up(data, auth_service: AuthService) -> Response:
    """Запрос на регистрацию пользователя
    data это словарь данных возвращаемым декоратором @validate_request.
    Объект типа UserService попадает сюда с помощью DI, реализованной библиотекой flask_injector
    Подробности: https://github.com/alecthomas/flask_injector
    """
    return auth_service.sign_up(data)


@auth_bp.route("/sign-in", methods=["POST"])
@AuthService.validate_request(schema=SignInSchema)
def sign_in(data, auth_service: AuthService) -> Response:
    """Запрос на вход пользователя в систему"""
    return auth_service.sign_in(data)


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh(auth_service: AuthService) -> Response:
    """Запрос на обновление access токена"""
    return auth_service.refresh_jwt()


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout(auth_service: AuthService) -> Response:
    """Запрос на выход из аккаунта на текущем устройстве"""
    return auth_service.logout()


@auth_bp.route("/logout_all", methods=["POST"])
@jwt_required()
def logout_all(auth_service: AuthService) -> Response:
    """Запрос на выход из аккаунта со всех устройств"""
    return auth_service.logout_all()


@auth_bp.route("/login_history", methods=["GET"])
@jwt_required()
def login_history(auth_service: AuthService) -> Response:
    """Запрос истории посещений"""
    return auth_service.login_history()


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me(auth_service: AuthService) -> Response:
    """Запрос пользовательского профиля"""
    return auth_service.me()


@auth_bp.route("/change_password", methods=["POST"])
@jwt_required(fresh=True)
@AuthService.validate_request(schema=UpdatePasswordSchema)
def change_password(data, auth_service: AuthService) -> Response:
    """Запрос пользовательского профиля.
    Смена пароля это важная операция, поэтому о первых для неё сделаем отдельный endpoint и обработчики,
    а также ограничиваем доступ к ней, только access токен с fresh флагом будут иметь доступ, т.е токен
    полученный только при вводе логина/пароля, т.е перед сменой пароля пользователю нужно будет сначала
    залогиниться, если он давно этого не делал.
    """
    return auth_service.change_password(data)
