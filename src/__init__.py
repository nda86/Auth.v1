import typing as t

from flask import Flask, jsonify

from src.core.config import settings


def create_app(test_config: t.Optional[dict] = None) -> Flask:
    app = Flask(__name__)

    if test_config is None:
        app.config.from_object(settings)
    else:
        app.config.from_mapping(test_config)

    @app.route("/hello")
    def hello():
        """Роут для проверки запуска flask"""
        return jsonify("Hello, World!")

    return app
