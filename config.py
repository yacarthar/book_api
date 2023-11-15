import base64
import json
import os
from typing import Union

from pydantic import validator, Field
from pydantic_settings import BaseSettings


def decoded_route():
    try:
        routes_byte: bytes = base64.b64decode(os.getenv("PLATFORM_ROUTES"))
        routes: dict = json.loads(routes_byte)
        return [*routes][0]  # get first key: https route
    except (base64.binascii.Error, json.JSONDecodeError):
        raise ValueError("Invalid routes env variable")


def get_db_config(field_name):
    try:
        config_raw: str = os.getenv("PLATFORM_RELATIONSHIPS")
        config_byte: bytes = base64.b64decode(config_raw)
        db_config: dict = json.loads(config_byte)["postgres"][0]
        return db_config.get(field_name)
    except (base64.binascii.Error, json.JSONDecodeError):
        raise ValueError("Invalid relationship env variable")


class Base(BaseSettings):
    SECRET_KEY: str = "tempkey"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DB_SCHEME: str = "postgresql"

    class Config:
        env_file_encoding = "utf-8"
        extra = "ignore"

    @property
    def db_uri(self):
        return (
            f"{self.DB_SCHEME}://{self.DB_USERNAME}:{self.DB_PASSWORD}"
            + f"@{self.DB_HOST}:{str(self.DB_PORT)}/{self.DB_PATH}"
        )

class Local(Base):
    APP_BASE_URL: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_PATH: str

    class Config:
        env_file = ".local.env"


class Prod(Base):
    APP_BASE_URL: str = Field(default_factory=decoded_route)

    DB_USERNAME: str = Field(default_factory=lambda: get_db_config("username"))
    DB_PASSWORD: str = Field(default_factory=lambda: get_db_config("password"))
    DB_HOST: str = Field(default_factory=lambda: get_db_config("host"))
    DB_PORT: int = Field(default_factory=lambda: get_db_config("port"))
    DB_PATH: str = Field(default_factory=lambda: get_db_config("path"))

    class Config:
        env_file = ".prod.env"


config = dict(
    local=Local,
    # development=Dev,
    # staging=Staging,
    production=Prod,
)
Settings: Union[Local, Prod] = config[os.getenv("PLATFORM_ENVIRONMENT_TYPE", "local")]

settings = Settings()
