from pydantic import BaseSettings, BaseModel


class TestSettings(BaseSettings):
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = True
    AUTH_URL: str = "http://127.0.0.1:5000"
    JWT_SECRET_KEY: str = "test_secret_key"


settings = TestSettings()
