import sys
from pathlib import Path
from dataclasses import dataclass
import typing as t
from functools import partial

import pytest
import requests
from flask.testing import FlaskClient
from requests.structures import CaseInsensitiveDict

from .config import settings

sys.path.append(str(Path(__file__).parent.parent))
from src import create_app, db  # noqa


@dataclass
class HTTPResponse:
    """Дата класс для модели http ответа"""
    body: str
    headers: CaseInsensitiveDict[str]
    status: int


@pytest.fixture(scope="session")
def flask_client() -> FlaskClient:
    """Клиент для тестирования сервиса на flask"""
    app = create_app(settings)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


@pytest.fixture(scope="session")
def http_client() -> requests:
    """Объект для выполнения HTTP запросов"""
    return requests


@pytest.fixture
def flask_request(flask_client):
    """Выполнение тестового запроса"""
    def inner(path: str, data: t.Optional[dict] = None, headers: t.Optional[dict] = None):
        path = path.lstrip("/")
        rv = flask_client.post(f"/auth/{path}", data=data, headers=headers)
        return rv
    return inner


@pytest.fixture
def create_user(flask_request):
    """Фикстура для создания пользователя"""
    return partial(flask_request, path="sign-up")


@pytest.fixture
def login_user(flask_request):
    """Фикстура для логина пользователя через логи/пароль"""
    return partial(flask_request, path="sign-in")


@pytest.fixture
def logout_user(flask_client):
    """Фикстура для выхода пользователя"""
    def inner(data: dict):
        rv = flask_client.post("/auth/logout", data=data, headers=headers)
        return rv
    return inner


@pytest.fixture
def make_refresh_request(flask_client):
    """Фикстура принимает словарь параметров и инициирует создание пользователя"""
    def inner(refresh_token: str):
        rv = flask_client.post("/auth/refresh", headers={"Authorization": f"Bearer {refresh_token}"})
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
    create_user(data=dict(username="test", password="test"))
    rv = login_user(data=dict(username="test", password="testtest"))
    return rv.json.get("access_token")


@pytest.fixture
def make_get_request(http_client):
    """Фикстура выполняет get запрос к тестируемому сервису.
    В этом случае не используем тестовый клиент фласка.
    """
    def inner(path: str, params: t.Optional[dict] = None, headers: t.Optional[dict] = None) -> HTTPResponse:
        path = path.lstrip("/")
        url = f"{settings.AUTH_URL}/{path}"
        res = http_client.get(url, params=params, headers=headers)
        return HTTPResponse(
            body=res.text,
            headers=res.headers,
            status=res.status_code,
        )
    return inner
