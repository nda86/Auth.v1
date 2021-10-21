from http import HTTPStatus


def test_success(flask_client):
    """"Тест успешного создания пользователя"""
    rv = flask_client.post("/auth/sign-up", data=dict(username="foo111111", password="bar4444444"))

    assert rv.status_code == HTTPStatus.OK
