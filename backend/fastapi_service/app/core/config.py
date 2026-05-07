from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Sentiment Intelligence Platform"
    environment: str = "development"
    api_version: str = "v1"
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    postgres_dsn: str = "postgresql+psycopg://sip:sip@localhost:5432/sip"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 30
    refresh_token_days: int = 14
    nlp_model_name: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
