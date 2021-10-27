import datetime

from core import db

from .common import UUIDMixin


class LoginHistory(db.Model, UUIDMixin):
    """Модель для таблицы, которая будет хранить историю пользовательских логинов"""
    __tablename__ = "login_history"

    user_id = db.Column(db.String(length=36), db.ForeignKey("users.id"), nullable=False)
    user_agent = db.Column(db.Text, nullable=False)
    ip = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    def __repr__(self):
        return f"User {self.user_id} logged in {self.timestamp}"

    def dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "user_agent": self.user_agent,
            "ip": self.ip,
            "date": self.date
        }
