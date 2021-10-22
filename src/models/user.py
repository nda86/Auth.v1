from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from injector import inject
from marshmallow import EXCLUDE, validates

from .common import UUIDMixin, TimeStampedMixin
from src import db, ma
from src.exceptions import DBValidationException


class User(db.Model, UUIDMixin, TimeStampedMixin):
    """
    Модель данных Пользователи.
    """
    __tablename__ = "users"

    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, unique=True, nullable=True)

    def __repr__(self):
        return f"<User {self.username}>"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def password(self):
        """Делаем поле пароль недоступным для чтения"""
        raise AttributeError("Field password does not available")

    @password.setter
    def password(self, password: str):
        """В поле пароль будет хранится пароль в зашифрованном виде"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """Метод для проверки пользователя"""
        return check_password_hash(self.password_hash, password)


class UserSchema(ma.SQLAlchemyAutoSchema):
    """Класс для валидации создаваемой модели,
    перед записью в бд. Проверяет на существующие username и email
    """

    # @inject
    # def __init__(self, service: "UserService"):
    #     """Инжектим UserService"""
    #     self.service = service
    #     super().__init__()

    class Meta:
        model = User
        exclude = ("password_hash",)
        unknown = EXCLUDE

    @validates("username")
    def validate_username(self, value):
        if current_app.user_service.is_username_registered(value):
            raise DBValidationException("Username already exists.")

    @validates("email")
    def validate_email(self, value):
        if current_app.user_service.is_email_registered(value):
            raise DBValidationException("Email is already registered.")
