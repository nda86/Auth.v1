from flask_jwt_extended import create_access_token


class JWTService:
    """Сервис для работы с JWT"""

    @staticmethod
    def gen_access_token(user: object) -> str:
        """Генерирует и возвращает access token"""
        access_token = create_access_token(identity=user)
        return access_token

    def gen_refresh_token(self) -> str:
        """Генерирует и возвращает access token"""
        pass
