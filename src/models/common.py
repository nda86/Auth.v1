import datetime
import uuid

from core import db


class UUIDMixin:
    """Миксин для добавления в модели первичного ключа в формате UUID
    Здесь сами эмулируем UUID, а не используем тип UUID из sqlalchemy.dialects.postgresql потому что он
    работает только в pg, а хотелось бы еще поддержку других бд.
    """

    id = db.Column(
        db.String(length=36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False
    )


class TimeStampedMixin:
    """Миксин для добавления в модели полей created_at и updated_at"""

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
