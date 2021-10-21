from http import HTTPStatus


def test_flask_run(make_get_request):
    """Тест проверки что flask запущен и отвечает на тестовый запрос"""
    response = make_get_request("ping")

    assert response.status == HTTPStatus.OK
    assert response.body == "pong"
