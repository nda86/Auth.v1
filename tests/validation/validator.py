import typing as t

from werkzeug.test import Response
from pydantic import BaseModel
from pydantic.errors import PydanticValueError


class Validator:

    @classmethod
    def validate_response(cls, resp: Response, schema: t.Type[BaseModel]) -> bool:
        """Функция для валидации переданных данных."""
        try:
            schema.parse_obj(resp.json)
            return True
        except PydanticValueError:
            return False
