from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # base
    SECRET_KEY: str = Field("fsdfvgdaCDFSGfdnsfmdnfmdnfsfgjdbdjgfkkndfmsdbfhsdvj", env="SECRET_KEY")
    DEBUG: bool = Field(False, env="DEBUG")

    # sqlalchemy
    SQLALCHEMY_DATABASE_URI: str = Field("sqlite:///auth.db", env="SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = True
    SQLALCHEMY_ECHO: bool = True

    # JWT
    JWT_REDIS_URL: str = Field("redis://127.0.0.1:6379/3", env="JWT_REDIS_URL", description="Редис для хранения jwt")
    JWT_REFRESH_TOKEN_EXPIRES: int = Field(30 * 24 * 60 * 60, env="JWT_REFRESH_TOKEN_EXPIRES")  # 30 дней
    JWT_ACCESS_TOKEN_EXPIRES: int = Field(15 * 60, env="JWT_ACCESS_TOKEN_EXPIRES")   # 15 минут

    # swagger
    SWAGGER_URL: str = Field("/api/docs", env="SWAGGER_URL")
    SWAGGER_JSON_URL: str = Field("/openapi/swagger.json", env="URL_SWAGGER_JSON")

    # limiter
    RATELIMIT_DEFAULT: str = Field("100/minute", env="RATELIMIT_DEFAULT")
    RATELIMIT_STORAGE_URL: str = Field("redis://127.0.0.1:6379/5", env="RATELIMIT_STORAGE_URL")


settings = Settings()
