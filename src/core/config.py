from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    SECRET_KEY: str = Field("fsdfvgdaCDFSGfdnsfmdnfmdnfsfgjdbdjgfkkndfmsdbfhsdvj", env="SECRET_KEY")


settings = Settings()
