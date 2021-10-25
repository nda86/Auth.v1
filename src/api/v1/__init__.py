from flask import Flask, Blueprint


def create_api(app: Flask) -> None:
    from .auth import auth_bp
    api_bp = Blueprint("api", __name__, url_prefix="/api/v1/")
    api_bp.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
