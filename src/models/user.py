from werkzeug.security import generate_password_hash, check_password_hash

from .common import UUIDMixin, TimeStampedMixin
from src import db


class User(db.Model, UUIDMixin, TimeStampedMixin):
    """
    Модель данных Пользователи.
    """
    __tablename__ = "users"

    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<User {self.username}>"

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
