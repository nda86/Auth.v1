"""
Основная причина по которой в качестве хранилища был выбран именно `redis`.
Это возможность указать при записи refresh токена время его хранения в базе.
И сделав это время равным времени жизни токена, мы избежим ситуации когда
у нас бд будет захламлена просроченными токенами.
"""

import datetime
from functools import wraps

from redis import Redis
from redis.exceptions import RedisError
from flask_jwt_extended import get_jti, decode_token

from .jwt_storage import JWTStorage
from src.core.logger import auth_logger
from src.exceptions import DBMaintainException


def redis_error_wrapper(f):
    """Декоратор который перехватывает все возникающие ошибки при работе с redis.
    Пишет ошибку в лог и кидает кастомное исключение, которое обрабатывается дальше в программе."""
    @wraps(f)
    def inner(*args, **kwargs):
        try:
            ret = f(*args, **kwargs)
        except RedisError as e:
            auth_logger.error(f"При работе с редис хранилищем jwt токенов произошла ошибка\n {str(e)}")
            raise DBMaintainException()
        else:
            return ret
    return inner


class JWTRedisStorage(JWTStorage):
    """Реализация хранилища токенов на основе `redis`"""

    def __init__(self, redis: Redis):
        self.redis = redis

    @staticmethod
    def _get_name(user_id: str, token_jti: str) -> str:
        """Формирует и возвращает имя под которым будет сохранён токен"""
        return f"{user_id}-{token_jti}"

    @redis_error_wrapper
    def _get_ttl(self, token: str) -> datetime.timedelta:
        """Метод вычисляет с каким ttl сохранить токен в редисе.
        ttl будет равен количеству оставшихся секунд до момента когда токен "протухнет".
        Таким образом исключим хранение в бд просроченных токенов.
        """
        token_exp = decode_token(token).get("exp")
        ttl = datetime.datetime.fromtimestamp(token_exp) - datetime.datetime.now()
        return ttl

    @redis_error_wrapper
    def save_token(self, token: str, user_id: str) -> None:
        """Сохраняем jti токена в редис.
        """
        jti = get_jti(token)
        key = self._get_name(user_id, jti)
        value = jti
        ttl = self._get_ttl(token)
        self.redis.set(key, value, ex=ttl)

    @redis_error_wrapper
    def get_token_by_jti(self, token_jti: str, user_id: str) -> str:
        """Возвращает токен, конкретно его jti"""
        return self.redis.get(self._get_name(user_id, token_jti))

    @redis_error_wrapper
    def remove_token_by_jti(self, token_jti: str, user_id: str) -> None:
        """Удаляет токен из бд"""
        self.redis.delete(self._get_name(user_id, token_jti))

    @redis_error_wrapper
    def remove_all_user_tokens(self, user_id: str) -> None:
        """Удаляем все токены пользователя"""
        self.redis.delete(self._get_name(user_id, "*"))
