import sys
import typing as t
from dataclasses import dataclass
from functools import partial
from pathlib import Path

import pytest
import requests
from flask import Flask
from flask.testing import FlaskClient
from requests.structures import CaseInsensitiveDict
from werkzeug.test import TestResponse

from .config import settings

sys.path.append(str(Path(Path(__file__).parent.parent, "src")))
from core import create_app, db  # noqa
from models import Role, User  # noqa


@dataclass
class HTTPResponse:
    """Дата класс для модели http ответа"""

    body: str
    headers: CaseInsensitiveDict[str]
    status: int


@pytest.fixture()
def flask_app() -> Flask:
    """Экземпляр фласк приложения"""
    return create_app(settings)


@pytest.fixture()
def flask_client(flask_app) -> FlaskClient:
    """Клиент для тестирования сервиса на flask"""
    with flask_app.test_client() as client:
        yield client


@pytest.fixture()
def test_db(flask_app):
    """Создаем тестовую бд в пяти и инициализируем все таблицы"""
    with flask_app.app_context():
        db.create_all()


@pytest.fixture()
def test_super_db(flask_app):
    """Создаем тестовую бд в пяти и инициализируем все таблицы + добавляем в бд суперпользователя"""
    with flask_app.app_context():
        db.create_all()
        role_admin = Role(name="Admin")
        user_admin = User(username="admin", password="adminadmin")
        user_admin.roles.append(role_admin)
        db.session.add(user_admin)
        db.session.commit()


@pytest.fixture(scope="session")
def http_client() -> requests:
    """Объект для выполнения HTTP запросов"""
    return requests


@pytest.fixture
def make_flask_request(flask_client):
    """Выполнение тестового запроса"""
    def inner(verb: str, path: str, data: t.Optional[dict] = None, headers: t.Optional[dict] = None) -> TestResponse:
        path = path.lstrip("/")
        verb = verb.lower()
        flask_request = getattr(flask_client, verb)
        rv = flask_request(f"{settings.AUTH_API_URL}/{path}", data=data, headers=headers)
        return rv

    return inner


@pytest.fixture
def create_user(make_flask_request):
    """Фикстура для создания пользователя"""
    return partial(make_flask_request, verb="post", path="auth/sign-up")


@pytest.fixture
def login_user(make_flask_request):
    """Фикстура для логина пользователя через логи/пароль"""
    return partial(make_flask_request, verb="post", path="auth/sign-in")


@pytest.fixture
def logout_user(make_flask_request):
    """Фикстура для выхода пользователя"""
    return partial(make_flask_request, verb="get", path="auth/logout")


@pytest.fixture()
def admin_access_token(login_user):
    """Создаём токен админа для тестирования ендпоинтов доступных только для admina"""
    res = login_user(data=dict(username="admin", password="adminadmin"))
    return res.json.get("access_token")


@pytest.fixture
def make_refresh_request(flask_client):
    """Фикстура принимает словарь параметров и инициирует создание пользователя"""

    def inner(refresh_token: str):
        rv = flask_client.get(
            f"{settings.AUTH_API_URL}/auth/refresh", headers={"Authorization": f"Bearer {refresh_token}"}
        )
        return rv

    return inner


@pytest.fixture
def make_refresh_token(create_user, login_user):
    """Получаем refresh токен."""
    create_user(data=dict(username="test", password="testtest"))
    rv = login_user(data=dict(username="test", password="testtest"))
    return rv.json.get("refresh_token")


@pytest.fixture
def make_access_token(create_user, login_user):
    """Получаем refresh токен."""
    create_user(data=dict(username="test", password="testtest"))
    rv = login_user(data=dict(username="test", password="testtest"))
    return rv.json.get("access_token")


@pytest.fixture
def make_get_request(http_client):
    """Фикстура выполняет get запрос к тестируемому сервису.
    В этом случае не используем тестовый клиент фласка.
    """

    def inner(path: str, params: t.Optional[dict] = None, headers: t.Optional[dict] = None) -> HTTPResponse:
        path = path.lstrip("/")
        url = f"{settings.AUTH_SERVICE_URL}/{path}"
        res = http_client.get(url, params=params, headers=headers)
        return HTTPResponse(
            body=res.text,
            headers=res.headers,
            status=res.status_code,
        )

    return inner
