from http import HTTPStatus


def test_success_logout(test_db, make_refresh_token, make_refresh_request, logout_user):
    """Проверка ответа при успешном выходе с текущего устройтва, "выход с этого устройства".
    Успешный выход означает невозможность получить новый access токен по рефреш токену
    Последовательность теста:
      1. создаём тестовый рефреш токен,
      2. по нему получаем новые access и refresh
      3. делаем logout используя access токен полученный на шаге 2
      4. пробуем получить access токен используя refresh токен полученный на шаге 2
      Как итог мы должны получить 401 код
    """

    res = make_refresh_request(make_refresh_token)
    access_token, refresh_token = res.json.get("access_token"), res.json.get("refresh_token")
    logout_user(headers={"Authorization": f"Bearer {access_token}"})
    rv = make_refresh_request(refresh_token)

    assert rv.status_code == HTTPStatus.UNAUTHORIZED
