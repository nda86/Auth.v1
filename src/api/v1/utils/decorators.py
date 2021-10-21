import functools

from flask import request
from marshmallow import ValidationError, EXCLUDE

from src.exceptions import ApiValidationException


def validate_request(schema):
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                if request.json:
                    data = schema().load(request.json, unknown=EXCLUDE)
                elif request.form:
                    data = schema().load(request.form, unknown=EXCLUDE)
                else:
                    raise ApiValidationException("Data not found")
            except ValidationError as err:
                raise ApiValidationException(err.messages)
            return f(*args, data=data, **kwargs)

        return decorated_function

    return decorator
