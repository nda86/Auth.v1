import typing as t

from flask import Flask
from flask_injector import FlaskInjector
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import settings
from .logger import init_log_config

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)


def create_app(test_config: t.Optional[object] = None) -> Flask:
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app=app.wsgi_app, x_for=1, x_proto=1)  # для определения ip клиента за прокси

    if test_config is None:
        app.config.from_object(settings)
        init_log_config()  # инициализируем настройки логгера
    else:
        app.config.from_object(test_config)

    jwt.init_app(app)  # инициализация менеджера для работы с JWT

    @jwt.user_identity_loader
    def user_identity_loader(user) -> str:
        return str(user.id)

    @jwt.user_lookup_loader
    def user_lookup_loader(jwt_header: dict, jwt_payload: dict):
        return UserService().get_by_id(jwt_payload["sub"])

    ma.init_app(app)  # инициализация Marshmallow
    db.init_app(app)  # инициализация БД
    with app.app_context():
        """Определяем движок бд. Если бд sqlite, то при инициализации инструмента миграций передаём флаг
        render_as_batch=True
        Подробности https://alembic.sqlalchemy.org/en/latest/batch.html
        """
        is_sqlite = db.engine.url.drivername == "sqlite"

    migrate.init_app(app, db, render_as_batch=is_sqlite, compare_type=True)

    from services.user_service import UserService
    app.user_service = UserService()  # кладем в глобальный объект фласка инстанс UserService

    from api.v1 import create_api
    create_api(app)  # регистрируем blueprint для API v1

    from commands import init_commands
    init_commands(app)  # инициализируем свои команды

    from exceptions import init_error_handler
    init_error_handler(app)  # подключаем обработчики ошибок

    from swagger import init_swagger_ui
    init_swagger_ui(app)  # подключаем swagger

    limiter.init_app(app)  # инициализируем limiter

    @app.route("/ping")
    def hello():
        """Роут для проверки запуска flask"""
        return "pong"

    from di import ServiceInjector
    FlaskInjector(app=app, modules=[ServiceInjector])  # внедряем DI

    return app
