from marshmallow import fields, validate

from src import ma


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
