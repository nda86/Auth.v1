from pydantic import BaseModel, Field


class JWTResponseSchema(BaseModel):
    """Модель для валидации в тестах ответа с jwt при успешном логине в сервис"""
    access_token: str = Field(..., regex=r"^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$")
    refresh_token: str = Field(..., regex=r"^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$")
