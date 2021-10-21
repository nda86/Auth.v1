import datetime
import uuid

from src import db


class UUIDMixin:
    """Миксин для добавления в модели первичного ключа в формате UUID"""

    id = db.Column(db.Text(length=36), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)


class TimeStampedMixin:
    """Миксин для добавления в модели полей created_at и updated_at"""

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
