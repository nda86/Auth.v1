from http import HTTPStatus


def test_login_history(create_user, login_user, make_flask_get_request):
    """
    Проверяем получение истории входов.
    Делаем 2 входа с разными User-Agent
    В истории должны быть записи с этими значениями
    """
    create_user(data=dict(username="test", password="testtest"))
    res = login_user(data=dict(username="test", password="testtest"), headers={"User-Agent": "Test Chrome"})
    access_token = res.json.get("access_token")
    login_user(data=dict(username="test", password="testtest"), headers={"User-Agent": "Test Mozilla"})
    rv = make_flask_get_request(path="login_history", headers={"Authorization": f"Bearer {access_token}"})

    assert rv.status_code == HTTPStatus.OK
    assert '"user_agent":"Test Mozilla"' in rv.data.decode()
    assert '"user_agent":"Test Chrome"' in rv.data.decode()
