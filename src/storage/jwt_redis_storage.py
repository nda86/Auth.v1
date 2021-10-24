from redis import Redis

from .jwt_storage import JWTStorage


class JWTRedisStorage(JWTStorage):
    """Реализация хранилища токенов на основе `redis`"""

    def __init__(self, redis: Redis):
        self.redis = redis

    def save_token(self, token_jti: str, user_id: str) -> None:
        pass

    def get_token(self, token_jti: str, user_id: str) -> str:
        pass

    def remove_token(self, token_jti: str, user_id: str) -> None:
        pass

    def remove_all_token(self, user_id: str) -> None:
        pass
