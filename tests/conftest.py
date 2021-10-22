import sys
from pathlib import Path
from dataclasses import dataclass
import typing as t

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
def create_user(flask_client):
    """Фикстура принимает словарь параметров и инициирует создание пользователя"""
    def inner(user_data: dict):
        rv = flask_client.post("/auth/sign-up", data=user_data)
        return rv
    return inner


@pytest.fixture
def login_user(flask_client):
    """Фикстура принимает словарь параметров и инициирует создание пользователя"""
    def inner(data: dict):
        rv = flask_client.post("/auth/sign-in", data=data)
        return rv
    return inner


@pytest.fixture
def make_get_request(http_client):
    """Фикстура выполняет get запрос к тестируемому сервису"""
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
