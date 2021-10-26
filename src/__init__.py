import typing as t

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_injector import FlaskInjector
from flask_jwt_extended import JWTManager

from src.core.config import settings
from src.core.logger import init_log_config

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()


def create_app(test_config: t.Optional[object] = None) -> Flask:
    app = Flask(__name__)

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

    from .services.user_service import UserService
    app.user_service = UserService()  # кладем в глобальный объект фласка инстанс UserService

    from .api.v1 import create_api
    create_api(app)  # регистрируем blueprint для API v1

    from .commands import init_commands
    init_commands(app)  # инициализируем свои команды

    from .exceptions import init_error_handler
    init_error_handler(app)  # подключаем обработчики ошибок

    @app.route("/ping")
    def hello():
        """Роут для проверки запуска flask"""
        return "pong"

    from .di import ServiceInjector
    FlaskInjector(app=app, modules=[ServiceInjector])  # внедряем DI

    return app
