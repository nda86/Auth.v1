from flask import current_app
from marshmallow import EXCLUDE, validates
from werkzeug.security import check_password_hash, generate_password_hash

from core import db, ma
from core.logger import auth_logger
from exceptions import DBValidationException

from .common import TimeStampedMixin, UUIDMixin

# таблица для many-to-many связи между User и Role
user_role = db.Table(
    "user_role",
    db.Column("user_id", db.String(36), db.ForeignKey("users.id")),
    db.Column("role_id", db.String(36), db.ForeignKey("roles.id")),
    db.UniqueConstraint("user_id", "role_id", name="uniq_user_role")
)


class Role(db.Model, UUIDMixin, TimeStampedMixin):
    """
    Модель данных Роли пользователей.
    """

    __tablename__ = "roles"

    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Role {self.name}>"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def dict(self) -> dict:
        """Приводит объект role к типу dict"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


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
    roles = db.relationship("Role", secondary=user_role, backref=db.backref("users", lazy="dynamic"))

    def __repr__(self):
        return f"<User {self.username}>"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def dict(self) -> dict:
        """Приводит объект user к типу dict"""
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }

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

    def get_roles(self) -> list[Role]:
        """Метод возвращает список ролей пользователя"""
        return [role.name for role in self.roles]

    def has_role(self, role_name: str) -> bool:
        """Метод для проверки есть ли у пользователя определённая роль"""
        return role_name in self.get_roles()


class UserSchema(ma.SQLAlchemyAutoSchema):
    """Класс для валидации создаваемой модели User(пользователь),
    перед записью в бд. Проверяет на существующие username и email
    """

    class Meta:
        model = User
        exclude = ("password_hash",)
        unknown = EXCLUDE

    @validates("username")
    def validate_username(self, value):
        if current_app.user_service.is_username_registered(value):
            auth_logger.debug(f"Ошибка регистрации пользователя. Username {value} уже занято")
            raise DBValidationException("Username already exists.")

    @validates("email")
    def validate_email(self, value):
        if current_app.user_service.is_email_registered(value):
            auth_logger.debug(f"Ошибка регистрации пользователя. Email {value} уже использован")
            raise DBValidationException("Email is already registered.")


class RoleSchema(ma.SQLAlchemyAutoSchema):
    """Класс для валидации создаваемой модели Role(роль пользователя),
    перед записью в бд.
    """

    class Meta:
        model = Role
        unknown = EXCLUDE

    @validates("name")
    def validate_role_name(self, value):
        if Role.query.filter_by(name=value).first():
            auth_logger.debug(f"Ошибка создания роли. name {value} уже занято")
            raise DBValidationException("Role's name already exists.")
