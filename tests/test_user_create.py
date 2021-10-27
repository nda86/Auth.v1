from http import HTTPStatus

import pytest

from .test_data.validations import (VALID_USER, check_email_validation,
                                    check_password_validation,
                                    check_username_validation)


@pytest.mark.parametrize("test_data, expected_response, expected_code", check_password_validation)
def test_password_validation(test_db, create_user, test_data, expected_response, expected_code):
    """"Тест валидации пароля """
    rv = create_user(data=test_data)

    assert rv.status_code == expected_code
    assert rv.json.get("description", {}).get("password") == expected_response


@pytest.mark.parametrize("test_data, expected_response, expected_code", check_username_validation)
def test_username_validation(test_db, create_user, test_data, expected_response, expected_code):
    """"Тест валидации username"""
    rv = create_user(data=test_data)

    assert rv.status_code == expected_code
    assert rv.json.get("description", {}).get("username") == expected_response


@pytest.mark.parametrize("test_data, expected_response, expected_code", check_email_validation)
def test_email_validation(test_db, create_user, test_data, expected_response, expected_code):
    """"Тест валидации email"""
    rv = create_user(data=test_data)

    assert rv.status_code == expected_code
    assert rv.json.get("description", {}).get("email") == expected_response


def test_registrations(test_db, create_user):
    """"Тест регистрации пользователя"""
    rv = create_user(data=VALID_USER)

    assert rv.status_code == HTTPStatus.OK


def test_username_unique(test_db, create_user):
    """"Тест на уже существующий username пользователя"""
    create_user(data=dict(username="Admin", password="123456789", email="aaa@mail.ru"))
    rv = create_user(data=dict(username="Admin", password="123456789", email="bbb@mail.ru"))

    assert rv.status_code == HTTPStatus.BAD_REQUEST
    assert rv.json.get("description") == "Username already exists."


def test_email_unique(test_db, create_user):
    """"Тест на уже существующий email пользователя"""
    create_user(data=dict(username="Admin", password="123456789", email="aaa@mail.ru"))
    rv = create_user(data=dict(username="Admin2", password="123456789", email="aaa@mail.ru"))

    assert rv.status_code == HTTPStatus.BAD_REQUEST
    assert rv.json.get("description") == "Email is already registered."
