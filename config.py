from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    sqlalchemy_database_uri: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
