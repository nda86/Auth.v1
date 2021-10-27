from http import HTTPStatus


def test_user_get_profile(test_db, create_user, login_user, make_flask_request):
    """Тест получения профиля пользователя"""
    create_user(data=dict(username="test", password="testtest", email="test@test.ru"))
    res = login_user(data=dict(username="test", password="testtest"))
    access_token = res.json.get("access_token")
    rv = make_flask_request(verb="get", path="auth/me", headers={"Authorization": f"Bearer {access_token}"})

    assert rv.status_code == HTTPStatus.OK
    assert rv.json.get("email") == "test@test.ru"
    assert rv.json.get("username") == "test"
