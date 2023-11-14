from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    sqlalchemy_database_uri: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    APP_BASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
