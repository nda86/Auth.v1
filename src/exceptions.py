from werkzeug.exceptions import HTTPException


class DBValidationException(HTTPException):
    code = 400
    name = "CONSTRANT: Already exists"

    def __init__(self, description: str):
        self.description = description
        super().__init__()


class ApiValidationException(HTTPException):
    code = 400
    name = "API Validation error"

    def __init__(self, description: str):
        self.description = description
        super().__init__()


class DBMaintainException(HTTPException):
    code = 500
    name = "System error in database"

    def __init__(self, description: str):
        self.description = description
        super().__init__()
