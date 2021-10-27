"""
Обрабатывает входящие запросы на /role/*
"""

from flask import Blueprint, Response
from flask_jwt_extended import jwt_required

from schemas import (
    CreateRoleSchema, DeleteRoleSchema,
    UpdateRoleSchema, AssignRoleSchema,
    UnassignRoleSchema
)
from services import RoleService
from utils import RequestValidator, admin_required


role_bp = Blueprint("role", __name__, url_prefix="/roles")


@role_bp.route("", methods=["POST"])
@jwt_required()
@admin_required
@RequestValidator.validate_body(CreateRoleSchema)
def create_role(data, role_service: RoleService) -> Response:
    """Запрос на создание роли
    data это словарь данных возвращаемым декоратором @validate_request.
    """
    return role_service.create_role(data)


@role_bp.route("", methods=["GET"])
@jwt_required()
@admin_required
def list_roles(role_service: RoleService) -> Response:
    """Запрос на список все ролей в бд
    """
    return role_service.list_roles()


@role_bp.route("/<role_id>", methods=["DELETE"])
@jwt_required()
@admin_required
@RequestValidator.validate_view_args(schema=DeleteRoleSchema)
def delete_role(role_id: str, role_service: RoleService) -> Response:
    """Запрос на удаление роли"""
    return role_service.delete_role(role_id)


@role_bp.route("", methods=["PUT"])
@jwt_required()
@admin_required
@RequestValidator.validate_body(schema=UpdateRoleSchema)
def update_role(data, role_service: RoleService) -> Response:
    """Запрос на обновление роли
    data - провалидированные данные"""
    return role_service.update_role(data)


@role_bp.route("/assign", methods=["POST"])
@jwt_required()
@admin_required
@RequestValidator.validate_body(schema=AssignRoleSchema)
def assign_role(data, role_service: RoleService) -> Response:
    """Запрос на добавление роли
    data - провалидированные данные"""
    return role_service.assign_role(data)


@role_bp.route("/unassign", methods=["POST"])
@jwt_required()
@admin_required
@RequestValidator.validate_body(schema=UnassignRoleSchema)
def unassign_role(data, role_service: RoleService) -> Response:
    """Запрос на удаление роли у пользователя
    data - провалидированные данные"""
    return role_service.unassign_role(data)
