from injector import Module, Binder, singleton
from flask_injector import request
import redis

from .services import UserService, AuthService, JWTService, RoleService
from .storage import JWTStorage, JWTRedisStorage
from .core.config import settings


class ServiceInjector(Module):
    """Класс биндит на интерфейсы конкретные реализации. Которые будут инжектится в проект при запуске.
    Для DI используется библиотека flask-injector
    """
    def configure(self, binder: Binder) -> None:
        redis_client = redis.Redis.from_url(url=settings.JWT_REDIS_URL, decode_responses=True)
        jwt_redis_storage = JWTRedisStorage(redis=redis_client)

        binder.bind(interface=UserService, to=UserService, scope=request)
        binder.bind(interface=AuthService, to=AuthService, scope=request)
        binder.bind(interface=JWTService, to=JWTService, scope=request)
        binder.bind(interface=RoleService, to=RoleService, scope=request)
        binder.bind(interface=JWTStorage, to=jwt_redis_storage, scope=singleton)
