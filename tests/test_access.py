from http import HTTPStatus


def test_secure_data(test_db, make_access_token, make_flask_request):
    """Тест на проверку доступа с защищённой информации"""
    headers = {
        "Authorization": f"Bearer {make_access_token}"
    }
    rv1 = make_flask_request(verb="post", path="auth/secure", headers=headers)
    rv2 = make_flask_request(verb="post", path="auth/secure")

    assert rv1.status_code == HTTPStatus.OK
    assert rv2.status_code == HTTPStatus.UNAUTHORIZED
