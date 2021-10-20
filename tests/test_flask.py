def test_flask_run(flask_client):
    """Тест проверки что flask запущен и отвечает на тестовый запрос"""
    assert flask_client.get("/hello").json == "Hello, World!"
