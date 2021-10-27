def test_role_assign_unassign(test_super_db, admin_access_token, create_user, login_user, make_flask_request):
    """Тест на добавление/удаление роли пользователю"""

    name_test_role = "test_assigned_role"
    # создаём нового пользователя
    res = create_user(data=dict(username="test_assign", password="test_role_assign"))
    user_id = res.json.get("id")

    # создаём новую роль
    make_flask_request(
        verb="post",
        path="roles",
        data={"name": name_test_role},
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )

    # назначаем пользователю созданную роль
    make_flask_request(
        verb="post",
        path="roles/assign",
        data={"role_name": name_test_role, "user_id": user_id},
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )

    # логинемся пользователем и делаем авторизацию, в списке должна быть добавленная роль
    res = login_user(data=dict(username="test_assign", password="test_role_assign"))
    user_access_token = res.json.get("access_token")
    rv = make_flask_request(verb="get", path="auth/authorize", headers={"Authorization": f"Bearer {user_access_token}"})

    assert name_test_role in rv.json

    # далее удаляем эту роль у пользователя
    make_flask_request(
        verb="post",
        path="roles/unassign",
        data={"role_name": name_test_role, "user_id": user_id},
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )

    # еще раз делаем авторизацию, роли в списке быть не должно
    rv = make_flask_request(verb="get", path="auth/authorize", headers={"Authorization": f"Bearer {user_access_token}"})

    assert name_test_role not in rv.json
