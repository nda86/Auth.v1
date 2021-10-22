from http import HTTPStatus

from .validation.validator import Validator
from .validation.schema import JWTResponseSchema


def test_wrong_username(create_user, login_user):
    """Проверка попытки входа с неверным username"""
    create_user(dict(username="admin", password="admin", email="lol@mail.com"))
    rv = login_user(dict(username="wrong_username", password="admin"))
    assert rv.status_code == HTTPStatus.BAD_REQUEST
    assert rv.json.get("description") == "Wrong username or password"


def test_wrong_password(create_user, login_user):
    """Проверка попытки входа с неверным паролем"""
    create_user(dict(username="admin", password="admin", email="lol@mail.com"))
    rv = login_user(dict(username="admin", password="wrong_password"))
    assert rv.status_code == HTTPStatus.BAD_REQUEST
    assert rv.json.get("description") == "Wrong username or password"


def test_success_login(create_user, login_user):
    """Проверка ответа при успешном входе.
    Проверяется формат ответа, он должен соответсвовать заранее определённой структуре
    """
    create_user(dict(username="admin", password="adminadmin", email="lol@mail.com"))
    rv = login_user(dict(username="admin", password="adminadmin"))
    assert rv.status_code == HTTPStatus.OK
    assert Validator.validate_response(rv, JWTResponseSchema)
