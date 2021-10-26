from http import HTTPStatus

from .validation.validator import Validator
from .validation.schema import JWTResponseSchema


def test_change_password(test_db, create_user, make_flask_request, login_user):
    """Тест на смену пароля
    Создаём пользователя, меняем пароль, пробуем зайти с новым паролем
    """
    create_user(data=dict(username="test", password="testtest"))
    res = login_user(data=dict(username="test", password="testtest"))
    access_token = res.json.get("access_token")
    make_flask_request(
        verb="post",
        path="auth/change_password",
        data={"password": "new_testtest"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    rv1 = login_user(data=dict(username="test", password="testtest"))  # сначала пробуем зайти под старым паролем
    rv2 = login_user(data=dict(username="test", password="new_testtest"))  # потом под изменённым

    assert rv1.status_code == HTTPStatus.UNAUTHORIZED
    assert rv2.status_code == HTTPStatus.OK
    assert Validator.validate_response(rv2, JWTResponseSchema)  # проверяем что ответ содержит jwt токены
