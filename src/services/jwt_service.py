import typing as t

import sqlalchemy.exc
from flask_jwt_extended import create_access_token, create_refresh_token, get_jti, current_user, get_jwt
from injector import inject


from src import db
from src.models.refresh_token import RefreshToken
from src.core.logger import auth_logger
from src.exceptions import DBMaintainException
from src.storage import JWTStorage


class JWTService:
    """Сервис для работы с JWT.
    Генерация токенов, хранение и удаление токенов из хранилища и т.д
    """

    @inject
    def __init__(self, storage: JWTStorage):
        self.storage = storage

    @staticmethod
    def gen_access_token(user: object, fresh: bool = False) -> str:
        """Генерирует и возвращает access token"""
        # важно: ставим флаг fresh=True только при регистрации через логин/пароль
        # при рефреше флаг fresh не ставим
        access_token = create_access_token(identity=user, fresh=fresh)
        return access_token

    @staticmethod
    def gen_refresh_token(user: object) -> str:
        """Генерирует и возвращает access token"""
        refresh_token = create_refresh_token(user)
        return refresh_token

    def save_refresh_token(self, token: str, user_id) -> None:
        """Сохраняем refresh token's jti в бд."""
        jti = get_jti(token)
        self.storage.save_token(token_jti=jti, user_id=user_id)

        # token_obj = RefreshToken(token=jti, user_id=user_id)
        # db.session.add(token_obj)
        # try:
        #     db.session.commit()
        # except sqlalchemy.exc.DatabaseError as e:
        #     auth_logger.error(f"Неожиданная ошибка в бд при сохранение refresh токена\n{str(e)}")
        #     raise DBMaintainException("Something went wrong")

    def remove_refresh_token(self, token_jti: str, user_id: str) -> None:
        """Метод для удаления рефреш токена из бд"""
        self.storage.remove_token(token_jti=token_jti, user_id=user_id)
        # db.session.delete(refresh_token)
        # try:
        #     db.session.commit()
        # except sqlalchemy.exc.DatabaseError as e:
        #     auth_logger.error(f"Неожиданная ошибка в бд при удалении refresh токена\n{str(e)}")
        #     raise DBMaintainException("Something went wrong")

    def is_exists_refresh_token(self) -> tuple[bool, t.Optional[str], t.Optional["current_user"]]:
        """Проверяем есть ли в бд такой токен для пользователя.
        """
        jti = get_jwt()["jti"]
        refresh_token = self.storage.get_token(token_jti=jti, user_id=current_user.id)
        # refresh_token = RefreshToken.query.filter_by(user_id=current_user.id, token=jti).first()
        if refresh_token:
            return True, jti, current_user
        else:
            return False, None, None
