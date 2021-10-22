from flask import Flask


def create_api(app: Flask) -> None:
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
