from http import HTTPStatus

from .validation.validator import Validator
from .validation.schema import JWTResponseSchema


# def test_success_logout(make_access_token):
#     """Проверка ответа при успешном выходе с текущего устройтва, "выход с этого устройства".
#     """
#
#
#     assert rv.status_code == HTTPStatus.OK
#     assert Validator.validate_response(rv, JWTResponseSchema)
