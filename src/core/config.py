from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    SECRET_KEY: str = Field("fsdfvgdaCDFSGfdnsfmdnfmdnfsfgjdbdjgfkkndfmsdbfhsdvj", env="SECRET_KEY")
    SQLALCHEMY_DATABASE_URI: str = Field("sqlite:///auth.db", env="SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = True


settings = Settings()
