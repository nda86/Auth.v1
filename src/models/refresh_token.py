from src import db

from .common import UUIDMixin


class RefreshToken(db.Model, UUIDMixin):
    """
    Модель данных. Refresh токен
    """
    __tablename__ = "refresh_tokens"

    token = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Refresh token {self.token} for user {self.user_id} >"
