import typing as t

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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
        is_sqlite = db.engine.url.drivername == "sqlite"
    migrate.init_app(app, db, render_as_batch=is_sqlite, compare_type=True)

    @app.route("/ping")
    def hello():
        """Роут для проверки запуска flask"""
        return "pong"

    return app
