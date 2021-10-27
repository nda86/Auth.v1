"""
Декораторы и функции для контроля доступа
"""
from functools import wraps

from flask import abort
from flask_jwt_extended import current_user


def admin_required(f):
    """Декоратор делает эндпоинты доступными только для пользователя с ролью `admin`"""
    @wraps(f)
    def inner(*args, **kwargs):
        if not current_user.has_role("Admin"):
            return abort(403, description="access only for admin")
        return f(*args, **kwargs)
    return inner
