from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    SECRET_KEY: str = Field("fsdfvgdaCDFSGfdnsfmdnfmdnfsfgjdbdjgfkkndfmsdbfhsdvj", env="SECRET_KEY")
    SQLALCHEMY_DATABASE_URI: str = Field("sqlite:///auth.db", env="SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = True
    AUTH_URL: str = Field("http://127.0.0.1:5000", env="AUTH_URL")

    JWT_REDIS_URL: str = Field("redis://127.0.0.1:6379/3", env="JWT_REDIS_URL", description="Редис для хранения jwt")


settings = Settings()
