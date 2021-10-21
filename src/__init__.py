import json
import typing as t

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException

from src.core.config import settings

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config: t.Optional[dict] = None) -> Flask:
    app = Flask(__name__)

    if test_config is None:
        app.config.from_object(settings)
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)  # инициализация БД
    with app.app_context():
        """Определяем движок бд. Если бд sqlite, то при инициализации инструмента миграций передаём флаг
        render_as_batch=True
        Подробности https://alembic.sqlalchemy.org/en/latest/batch.html
        """
        is_sqlite = db.engine.url.drivername == "sqlite"
    migrate.init_app(app, db, render_as_batch=is_sqlite, compare_type=True)

    from .api.v1 import create_api
    create_api(app)

    @app.errorhandler(HTTPException)
    def json_exc_handler(e: HTTPException):
        """Отлавливает все HTTPException и отдает ответ об ошибке в формате json"""
        resp = e.get_response()
        resp.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description
        })
        resp.content_type = "application/json"
        return resp

    @app.route("/ping")
    def hello():
        """Роут для проверки запуска flask"""
        return "pong"

    return app
