from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    sqlalchemy_database_uri: str

    model_config = SettingsConfigDict(env_file=".env")
