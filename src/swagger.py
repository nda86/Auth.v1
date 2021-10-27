from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

from core.config import settings

SWAGGER_URL = settings.SWAGGER_URL
SWAGGER_JSON_URL = settings.SWAGGER_JSON_URL


def init_swagger_ui(app: Flask):
    swagger_bp = get_swaggerui_blueprint(
        SWAGGER_URL,
        SWAGGER_JSON_URL,
        config={"app_name": "Auth application"},
    )

    app.register_blueprint(swagger_bp)

    @app.route("/openapi/swagger.json")
    def get_openapi_spec():
        from openapi_spec import get_openapi_spec

        return jsonify(get_openapi_spec().to_dict())
