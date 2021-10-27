"""
Схемы используемые для валидации входящих запросов
"""

from marshmallow import fields, validate

from core import ma


class SignUpSchema(ma.Schema):
    """Схема для валидации входящих данных при регистрации пользователя"""
    username = fields.String(required=True, validate=[validate.Length(min=3, max=15)])
    password = fields.String(required=True, load_only=True, validate=[validate.Length(min=8, max=20)])
    first_name = fields.String(validate=[validate.Length(max=30)])
    last_name = fields.String(validate=[validate.Length(max=30)])
    email = fields.Email()


class SignInSchema(ma.Schema):
    """Схема для валидации входящих данных при логине пользователя"""
    username = fields.String(required=True)
    password = fields.String(required=True)


class UpdatePasswordSchema(ma.Schema):
    """Схема для валидации входящих данных при смене пароля"""
    password = fields.String(required=True, load_only=True, validate=[validate.Length(min=8, max=20)])


class CreateRoleSchema(ma.Schema):
    """Схема для валидации входящих данных при создании роли"""
    name = fields.String(required=True)
    description = fields.Str(required=False)


class DeleteRoleSchema(ma.Schema):
    """Схема для валидации входящих данных при создании роли"""
    role_id = fields.UUID(required=True)


class UpdateRoleSchema(ma.Schema):
    """Схема для валидации входящих данных при создании роли"""
    id = fields.UUID(required=True)
    name = fields.String(required=True)
    description = fields.Str(required=False)


class AssignRoleSchema(ma.Schema):
    """Схема для валидации входящих данных при добавлении роли пользователю"""
    role_name = fields.String(required=True)
    user_id = fields.UUID(required=True)


class UnassignRoleSchema(ma.Schema):
    """Схема для валидации входящих данных при удалении роли у пользователя"""
    role_name = fields.String(required=True)
    user_id = fields.UUID(required=True)
