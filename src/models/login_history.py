from src import db

from .common import UUIDMixin


class LoginHistory(db.Model, UUIDMixin):
    """Модель для таблицы, которая будет хранить историю пользовательских логинов"""
    pass
