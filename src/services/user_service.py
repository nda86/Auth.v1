from flask import jsonify
import sqlalchemy.exc

from src import db
from src.models.user import User, UserSchema
from src.exceptions import DBMaintainException
from src.core.logger import auth_logger


class UserService:
    """Сервис для выполнения необходимых действий над пользователями
    Создание пользователя, поиск пользователей в хранилище и т.д
    """
    model = User
    schema = UserSchema

    def create_user(self, data: dict):
        """Создание пользователя в БД - регистрация"""
        # здесь при загрузке данных в схему, будет проведена проверка уникальности username и email
        # в случае если поле не уникально будет кинуты соответсвующее исключение и на клиент вернётся описание ошибки
        self.schema().load(data)

        password = data.pop("password", None)
        # в метод не должны попадать данные пользователя  без пароля
        # необходимо обязательно проводить валидацию входных параметров перед вызовом этого метода
        assert password is not None
        user = self.model(**data)
        user.password = password
        db.session.add(user)
        try:
            db.session.commit()
        except sqlalchemy.exc.DatabaseError as e:
            """В случае ошибки создания записи в бд"""
            auth_logger.error(f"Неожиданная ошибка в бд при сохранение пользователя\n{str(e)}")
            raise DBMaintainException()
        else:
            return jsonify({"user": "created"}), 200

    def get_all(self):
        users = User.query.all()
        return users

    def is_username_registered(self, value):
        """Проверка на существующий `username`"""
        return bool(self.get_by_username(value))

    def is_email_registered(self, value):
        """Проверка на существующий `email`"""
        return bool(self.get_by_email(value))

    def get_by_username(self, value):
        """Поиск пользователя по `username`"""
        return self.model.query.filter_by(username=value).first()

    def get_by_email(self, value):
        """Поиск пользователя по `email`"""
        return self.model.query.filter_by(email=value).first()

    def get_by_id(self, value):
        """Поиск пользователя по `id`"""
        return self.model.query.filter_by(id=value).first()
