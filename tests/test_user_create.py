from http import HTTPStatus

import pytest

from .test_data.validations import (
    VALID_USER,
    check_password_validation, check_username_validation, check_email_validation,
)


@pytest.mark.parametrize("test_data, expected_response, expected_code", check_password_validation)
def test_password_validation(create_user, test_data, expected_response, expected_code):
    """"Тест валидации пароля """
    rv = create_user(test_data)

    assert rv.status_code == expected_code
    assert rv.json.get("description", {}).get("password") == expected_response


@pytest.mark.parametrize("test_data, expected_response, expected_code", check_username_validation)
def test_username_validation(create_user, test_data, expected_response, expected_code):
    """"Тест валидации username"""
    rv = create_user(test_data)

    assert rv.status_code == expected_code
    assert rv.json.get("description", {}).get("username") == expected_response


@pytest.mark.parametrize("test_data, expected_response, expected_code", check_email_validation)
def test_email_validation(create_user, test_data, expected_response, expected_code):
    """"Тест валидации email"""
    rv = create_user(test_data)

    assert rv.status_code == expected_code
    assert rv.json.get("description", {}).get("email") == expected_response


def test_registrations(create_user):
    """"Тест регистрации пользователя"""
    rv = create_user(VALID_USER)

    assert rv.status_code == HTTPStatus.OK


def test_username_unique(create_user):
    """"Тест на уже существующий username пользователя"""
    create_user(dict(username="Admin", password="123456789", email="aaa@mail.ru"))
    rv = create_user(dict(username="Admin", password="123456789", email="bbb@mail.ru"))

    assert rv.status_code == HTTPStatus.BAD_REQUEST
    assert rv.json.get("description") == "Username already exists."


def test_email_unique(create_user):
    """"Тест на уже существующий email пользователя"""
    create_user(dict(username="Admin", password="123456789", email="aaa@mail.ru"))
    rv = create_user(dict(username="Admin2", password="123456789", email="aaa@mail.ru"))

    assert rv.status_code == HTTPStatus.BAD_REQUEST
    assert rv.json.get("description") == "Email is already registered."
