from flask import Blueprint, request, current_app

from .utils.decorators import validate_request
from src.schemas.user_schema import SignUpSchema
from src.services.user_service import UserService

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/sign-up", methods=["POST"])
@validate_request(SignUpSchema)
def sign_up(data, service: UserService):
    """ data это словарь данных возвращаемым декоратором @validate_request.
    Объект типа UserService попадает сюда с помощью DI, реализованной библиотекой flask_injector
    Подробности: https://github.com/alecthomas/flask_injector
    """
    return service.create(data)
