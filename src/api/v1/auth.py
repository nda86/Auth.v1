from flask import Blueprint, request
from flask_pydantic import validate
from pydantic import BaseModel, Field, EmailStr


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


class ModelSignUP(BaseModel):
    """Модель для валидации body при регистрации пользователя"""
    username: str = Field(..., min_length=3, max_length=15)
    password: str = Field(..., min_length=8, max_length=30)
    first_name: str = Field("")
    last_name: str = Field("")
    email: EmailStr = Field(...)


@auth_bp.route("/sign-up", methods=["POST"])
@validate(body=ModelSignUP)
def sign_up():
    return request.json
