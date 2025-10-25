import os

from pydantic import Extra
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
        extra = Extra.allow

settings = Settings()
