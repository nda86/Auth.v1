from flask import Blueprint, Flask


def create_api(app: Flask) -> None:
    from .auth import auth_bp
    from .role import role_bp
    api_bp = Blueprint("api", __name__, url_prefix="/api/v1/")
    api_bp.register_blueprint(auth_bp)
    api_bp.register_blueprint(role_bp)
    app.register_blueprint(api_bp)
