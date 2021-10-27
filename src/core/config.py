from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    SECRET_KEY: str = Field("fsdfvgdaCDFSGfdnsfmdnfmdnfsfgjdbdjgfkkndfmsdbfhsdvj", env="SECRET_KEY")
    SQLALCHEMY_DATABASE_URI: str = Field("sqlite:///auth.db", env="SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = True
    SQLALCHEMY_ECHO: bool = True
    DEBUG: bool = Field(False, env="DEBUG")

    # JWT
    JWT_REDIS_URL: str = Field("redis://127.0.0.1:6379/3", env="JWT_REDIS_URL", description="Редис для хранения jwt")
    JWT_REFRESH_TOKEN_EXPIRES: int = Field(30 * 24 * 60 * 60, env="JWT_REFRESH_TOKEN_EXPIRES")  # 30 дней
    JWT_ACCESS_TOKEN_EXPIRES: int = Field(15 * 60, env="JWT_ACCESS_TOKEN_EXPIRES")   # 15 минут


settings = Settings()
