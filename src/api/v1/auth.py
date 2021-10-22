from flask import Blueprint
from flask_jwt_extended import jwt_required


from src.schemas.user_schema import SignUpSchema, SignInSchema
from src.services import UserService, AuthService


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/sign-up", methods=["POST"])
@AuthService.validate_request(SignUpSchema)
def sign_up(data, user_service: UserService):
    """ data это словарь данных возвращаемым декоратором @validate_request.
    Объект типа UserService попадает сюда с помощью DI, реализованной библиотекой flask_injector
    Подробности: https://github.com/alecthomas/flask_injector
    """
    return user_service.create_user(data)


@auth_bp.route("/sign-in", methods=["POST"])
@AuthService.validate_request(schema=SignInSchema)
def sign_in(data, auth_service: AuthService):
    return auth_service.sign_in(data)


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh(auth_service: AuthService):
    return auth_service.refresh_jwt()
