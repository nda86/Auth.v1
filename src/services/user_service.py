import sqlalchemy.exc

from src import db
from src.models.user import User
from src.exceptions import DBValidationException


class UserService:
    """Класс для выполнения необходимых действий над пользователями"""

    model = User

    def create(self, data: dict):
        """Создание пользователя в БД - регистрация"""
        password = data.pop("password", None)
        # в метод не должны попадать данные пользователя  без пароля
        # необходимо обязательно проводить валидацию данных перед вызовом этого метода
        assert password is not None
        user = self.model(**data)
        user.password = password
        db.session.add(user)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            """В случае ошибки создания записи в бд"""
            raise DBValidationException(description=e.detail)

    def get_all(self):
        users = User.query.all()
        return users

    def get_by_id(self, id: str):
        pass
