import typing as t

import sqlalchemy.exc
from flask import Response, abort, jsonify
from injector import inject

from core import db
from core.logger import auth_logger
from exceptions import DBMaintainException
from models import Role, RoleSchema

from .jwt_service import JWTService
from .user_service import UserService


class RoleService:
    """
    Сервис отвечает за работу с ролями пользователя
    Предоставляет методы для обработки запросов на создание роли, удаление роли, добавление/убирание роли пользователю
    Обрабатывает запросы на /roles/*
    """

    @inject
    def __init__(self, user_service: UserService, token_service: JWTService):
        self.user_service = user_service
        self.token_service = token_service
        self.model = Role
        self.schema = RoleSchema

    @staticmethod
    def _make_response(data: t.Union[dict, str, list]) -> Response:
        """Метод формирует и возвращает окончательный Response"""
        return jsonify(data)

    def create_role(self, data: dict) -> Response:
        """Метод выполняет создание роли
        data - провалидированные данные полученные от пользователя
        """
        # здесь при загрузке данных в схему, будет проведена проверка уникальности названия роли
        # в случае если поле не уникально будет кинуты соответсвующее исключение и на клиент вернётся описание ошибки
        self.schema().load(data)

        role = self.model(**data)
        db.session.add(role)
        try:
            db.session.commit()
        except sqlalchemy.exc.DatabaseError as e:
            auth_logger.error(f"Неожиданная ошибка в бд при сохранение роли пользователя {data}\n{str(e)}")
            raise DBMaintainException()
        else:
            return self._make_response(role.dict())

    def delete_role(self, role_id: str) -> Response:
        """Метод выполняет удаление роли
        """
        # здесь при загрузке данных в схему, будет проведена проверка уникальности названия роли
        # в случае если поле не уникально будет кинуты соответсвующее исключение и на клиент вернётся описание ошибки

        role = self.model.query.get_or_404(role_id, description="Роль с таким id не существует")
        db.session.delete(role)
        try:
            db.session.commit()
        except sqlalchemy.exc.DatabaseError as e:
            auth_logger.error(f"Неожиданная ошибка в бд при сохранение роли пользователя {role}\n{str(e)}")
            raise DBMaintainException()
        else:
            return self._make_response(f"Role {role} successfully deleted")

    def list_roles(self) -> Response:
        """Метод возвращает список ролей в бд
        """
        try:
            roles = self.model.query.all()
        except sqlalchemy.exc.DatabaseError as e:
            auth_logger.error(f"Неожиданная ошибка в бд при запросе списка ролей\n{str(e)}")
            raise DBMaintainException()
        else:
            return self._make_response([role.dict() for role in roles])

    def update_role(self, data: dict) -> Response:
        """Метод обновляет роль в бд
        """
        role = self.model.query.get_or_404(str(data.get("id")), description="Роль с данным id отсутствует в бд")
        role.name = data.get("name")
        role.description = data.get("description")
        db.session.add(role)
        try:
            db.session.commit()
        except sqlalchemy.exc.DatabaseError as e:
            auth_logger.error(f"Неожиданная ошибка в бд при изменении роли\n{str(e)}")
            raise DBMaintainException()
        else:
            return self._make_response(role.dict())

    def assign_role(self, data: dict) -> Response:
        """Метод добавляет роль пользователю
        """
        role = self._get_role(data)
        user = self._get_user(data)
        user.roles.append(role)
        db.session.add(user)
        try:
            db.session.commit()
        except sqlalchemy.exc.DatabaseError as e:
            auth_logger.error(f"Неожиданная ошибка в бд при добавлении роли\n{str(e)}")
            raise DBMaintainException()
        else:
            return self._make_response("Role successfully assign")

    def unassign_role(self, data: dict) -> Response:
        """Метод убирает роль у пользователя в бд
        """
        role = self._get_role(data)
        user = self._get_user(data)
        user.roles.remove(role)
        db.session.add(user)
        try:
            db.session.commit()
        except sqlalchemy.exc.DatabaseError as e:
            auth_logger.error(f"Неожиданная ошибка в бд при удалении роли у пользователя\n{str(e)}")
            raise DBMaintainException()
        else:
            return self._make_response("Role successfully unassign")

    def _get_role(self, data):
        """Получаем объекты роли"""
        role = self.model.query.filter_by(name=data.get("role_name")).first()
        if not role:
            auth_logger.debug(f"При удалении роли у пользователя. Роль {data.get('role_name')} не найдена")
            abort(404, description=f"Роль {data.get('role_name')} не найдена")
        return role

    def _get_user(self, data):
        """Получаем объекты пользователя"""
        user = self.user_service.get_by_id(data.get("user_id"))
        if not user:
            auth_logger.debug(f"При удалении роли у пользователя. Пользователь с {data.get('user_id')} не найден")
            abort(404, description=f"Пользователь с {data.get('user_id')} не найден")
        return user
