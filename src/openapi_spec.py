from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import current_app


def get_openapi_spec() -> APISpec:
    """Формируем объект который будет генерировать спеку для swagger"""
    spec = APISpec(
        title="Auth - сервис аутентификации и авторизации",
        version="0.1.0",
        openapi_version="3.0.2",
        info=dict(
            description="Сервис выполняет регистрацию пользователей, работу с JWT токенами, "
                        "управление ролями пользователей"
        ),
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )

    jwt_token = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    spec.components.security_scheme("jwt_token", jwt_token)

    with current_app.test_request_context():
        for rule in current_app.url_map.iter_rules():
            spec.path(view=current_app.view_functions[rule.endpoint])

    return spec
