from http import HTTPStatus


def test_role_access(test_db, make_flask_request):
    """Тестируем доступ к ролям только для admin
    Передаваемые параметры не будут парсится, так ак запрос отсечется еще до них
    """
    rv1 = make_flask_request(verb="post", path="roles")
    rv2 = make_flask_request(verb="get", path="roles")
    rv3 = make_flask_request(verb="put", path="roles")
    rv4 = make_flask_request(verb="delete", path="roles/11111")

    assert rv1.status_code == HTTPStatus.UNAUTHORIZED
    assert rv2.status_code == HTTPStatus.UNAUTHORIZED
    assert rv3.status_code == HTTPStatus.UNAUTHORIZED
    assert rv4.status_code == HTTPStatus.UNAUTHORIZED


def test_role_create(test_super_db, make_flask_request, admin_access_token):
    """Тестируем создание новой роли, доступно только Admin"""
    rv = make_flask_request(
        verb="post",
        path="roles",
        data=dict(name="superrole"),
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert rv.status_code == HTTPStatus.OK
    assert rv.json.get("name") == "superrole"


def test_role_list(test_super_db, make_flask_request, admin_access_token):
    """Тест вывода списка ролей.
    Создаём несколько ролей потом проверяем список, доступно только Admin
    """
    make_flask_request(
        verb="post",
        path="roles",
        data=dict(name="superrole1"),
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    make_flask_request(
        verb="post",
        path="roles",
        data=dict(name="superrole2"),
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    rv = make_flask_request(verb="get", path="roles", headers={"Authorization": f"Bearer {admin_access_token}"})

    assert rv.status_code == HTTPStatus.OK
    assert "superrole1" in rv.data.decode()
    assert "superrole2" in rv.data.decode()


def test_role_update(test_super_db, make_flask_request, admin_access_token):
    """Тест изменения роли, доступно только Admin
    Создаём роль потом меняем ей имя и проверяем
    """
    res = make_flask_request(
        verb="post",
        path="roles",
        data=dict(name="superrole1"),
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    role_id = res.json.get("id")
    rv = make_flask_request(
        verb="put",
        path="roles",
        data=dict(id=role_id, name="change_role"),
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )

    assert rv.status_code == HTTPStatus.OK
    assert rv.json.get("name") == "change_role"


def test_role_delete(test_super_db, make_flask_request, admin_access_token):
    """Тест удаления роли, доступно только Admin
    Создаём роль потом удаляем её и проверяем что её не в списке
    """
    res = make_flask_request(
        verb="post",
        path="roles",
        data=dict(name="superrole1"),
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    role_id = res.json.get("id")
    rv1 = make_flask_request(verb="get", path="roles", headers={"Authorization": f"Bearer {admin_access_token}"})
    make_flask_request(
        verb="delete", path=f"roles/{role_id}", headers={"Authorization": f"Bearer {admin_access_token}"}
    )
    rv2 = make_flask_request(verb="get", path="roles", headers={"Authorization": f"Bearer {admin_access_token}"})

    assert "superrole1" in rv1.data.decode()
    assert "superrole1" not in rv2.data.decode()
