import typing as t

import sqlalchemy.exc

from src import db
from flask_jwt_extended import create_access_token, create_refresh_token, get_jti, current_user, get_jwt

from src.models.refresh_token import RefreshToken
from src.exceptions import DBMaintainException


class JWTService:
    """Сервис для работы с JWT.
    Генерация токенов, хранение и удаление токенов из хранилища и т.д
    """

    def gen_access_token(self, user: object, fresh: bool = False) -> str:
        """Генерирует и возвращает access token"""
        # важно: ставим флаг fresh=True только при регистрации через логин/пароль
        # при рефреше флаг fresh не ставим
        access_token = create_access_token(identity=user, fresh=fresh)
        return access_token

    def gen_refresh_token(self, user: object) -> str:
        """Генерирует и возвращает access token"""
        refresh_token = create_refresh_token(user)
        return refresh_token

    def save_refresh_token(self, token: str, user_id) -> None:
        """Сохраняем refresh token's jti в бд."""
        jti = get_jti(token)
        token_obj = RefreshToken(token=jti, user_id=user_id)
        db.session.add(token_obj)
        try:
            db.session.commit()
        except sqlalchemy.exc.DatabaseError:
            raise DBMaintainException("Something went wrong")

    def is_exists_refresh_token(self) -> tuple[bool, t.Optional["current_user"]]:
        """Проверяем есть ли в бд такой токен для пользователя.
        Если есть то удаляем его и возвращаем True, и current_user если такого токена нет,
        то False и None
        """
        jti = get_jwt()["jti"]
        refresh_token = RefreshToken.query.filter_by(user_id=current_user.id, token=jti).first()
        if refresh_token:
            db.session.delete(refresh_token)
            try:
                db.session.commit()
                return True, current_user
            except sqlalchemy.exc.DatabaseError:
                raise DBMaintainException("Something went wrong")
        else:
            return False, None
