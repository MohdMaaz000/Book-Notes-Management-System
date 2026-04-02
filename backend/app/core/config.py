import json
from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="Book & Notes Management System", alias="APP_NAME")
    environment: Literal["development", "test", "production"] = Field(default="development", alias="ENVIRONMENT")
    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")

    database_url: str = Field(..., alias="DATABASE_URL")

    jwt_access_secret: str = Field(..., min_length=32, alias="JWT_ACCESS_SECRET")
    jwt_refresh_secret: str = Field(..., min_length=32, alias="JWT_REFRESH_SECRET")
    jwt_access_exp_minutes: int = Field(default=15, alias="JWT_ACCESS_EXP_MINUTES")
    jwt_refresh_exp_days: int = Field(default=7, alias="JWT_REFRESH_EXP_DAYS")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    refresh_cookie_name: str = Field(default="book_notes_refresh_token", alias="REFRESH_COOKIE_NAME")
    session_secret: str | None = Field(default=None, alias="SESSION_SECRET")

    bcrypt_rounds: int = Field(default=12, alias="BCRYPT_ROUNDS")
    cors_origins: str = Field(default='["http://localhost:3000"]', alias="CORS_ORIGINS")

    rate_limit_window_seconds: int = Field(default=900, alias="RATE_LIMIT_WINDOW_SECONDS")
    rate_limit_max_requests: int = Field(default=200, alias="RATE_LIMIT_MAX_REQUESTS")
    auth_rate_limit_max_requests: int = Field(default=20, alias="AUTH_RATE_LIMIT_MAX_REQUESTS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def sqlalchemy_database_url(self) -> str:
        url = self.database_url
        if url.startswith("postgresql://") and "+psycopg" not in url.split("://", 1)[0]:
            return url.replace("postgresql://", "postgresql+psycopg://", 1)
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql+psycopg://", 1)
        return url

    @property
    def cors_origin_list(self) -> list[str]:
        value = self.cors_origins
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, list) else [str(parsed)]
        except json.JSONDecodeError:
            return [item.strip() for item in value.split(",") if item.strip()]

    @property
    def session_secret_value(self) -> str:
        return self.session_secret or self.jwt_access_secret


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
