"""
Описываем собственные классы исключений.
Идея в том чтобы при возникновении определённых ситуаций кидать свои исключения, с определённой структурой.
Сейчас просто просто прописываем свои атрибуты, к которым можем обращаться в обработчиках исключений.
"""

from werkzeug.exceptions import HTTPException


class DBValidationException(HTTPException):
    """EXC бросаем его если пользователь при регистрации ввёл
    данные которые не проходят валидацию в бд"""
    code = 400
    name = "CONSTRANT: Already exists"

    def __init__(self, description: str):
        self.description = description
        super().__init__()


class ApiValidationException(HTTPException):
    """EXC бросаем его если пользователь при регистрации ввёл
    данные которые не проходят валидацию в API"""
    code = 400
    name = "API Validation error"

    def __init__(self, description: str):
        self.description = description
        super().__init__()


class DBMaintainException(HTTPException):
    """EXC бросаем его если в бд случилась непредвиденная ошибка.
    Клиенту просто отдаём код 500 с общим описание что-то пошло не так"""
    code = 500
    name = "System error in database"

    def __init__(self, description: str):
        self.description = description
        super().__init__()


class WrongCredentials(HTTPException):
    """EXC бросаем его если пользователь при аутентификации указал неверный логи или пароль"""
    code = 400
    name = "Wrong credentials"

    def __init__(self, description: str):
        self.description = description
        super().__init__()


class RefreshTokenInvalid(HTTPException):
    """EXC бросаем его если refresh token отсутствует в БД, то есть считаем его недействительным"""
    code = 401
    name = "Refresh token is unavailable"

    def __init__(self, description: str):
        self.description = description
        super().__init__()
