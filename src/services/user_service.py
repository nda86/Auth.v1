from pydantic import BaseModel

from src import db
from src.models.user import User


class UserService:
    """Класс для выполнения необходимых действий над пользователями"""

    model = User

    def create(self, data: dict):
        user = self.model({})
        db.session.add(user)
        db.session.commit()

    def get_all(self):
        users = User.query.all()
        return users