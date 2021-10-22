from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = Field("sqlite:///auth.db", env="SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = True
    AUTH_URL: str = Field("http://127.0.0.1:5000", env="AUTH_URL")


settings = Settings()
