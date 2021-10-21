from werkzeug.exceptions import HTTPException


class DBValidationException(HTTPException):
    code = 401
    name = "CONSTRANT: Already exists"

    def __init__(self, description: str):
        self.description = description
        super().__init__()
