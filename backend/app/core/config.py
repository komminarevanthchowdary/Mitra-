from functools import lru_cache
from typing import Literal

from pydantic import AliasChoices, Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "Mitra Solar Enterprises API"
    environment: Literal["development", "test", "production"] = Field(
        default="development", validation_alias=AliasChoices("ENVIRONMENT", "ENV")
    )
    database_url: str = "postgresql+psycopg://USER:PASSWORD@HOST/DATABASE?sslmode=require"
    jwt_secret: SecretStr = SecretStr("development-only-change-me-before-deploying")
    jwt_algorithm: Literal["HS256"] = "HS256"
    access_token_minutes: int = Field(default=15, ge=5, le=60)
    refresh_token_days: int = Field(default=7, ge=1, le=30)
    frontend_origins: str = Field(
        default="http://localhost:3000",
        validation_alias=AliasChoices("FRONTEND_ORIGINS", "CORS_ORIGINS"),
    )

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip().rstrip("/") for origin in self.frontend_origins.split(",") if origin.strip()]

    @model_validator(mode="after")
    def validate_production_settings(self) -> "Settings":
        if self.environment == "production":
            secret = self.jwt_secret.get_secret_value()
            placeholder_secret = secret.casefold()
            if (
                len(secret) < 32
                or placeholder_secret == "development-only-change-me-before-deploying"
                or any(marker in placeholder_secret for marker in ("replace", "change-me", "placeholder"))
            ):
                raise ValueError("JWT_SECRET must be a unique random value of at least 32 characters in production.")
            if not self.cors_origins or "*" in self.cors_origins:
                raise ValueError("FRONTEND_ORIGINS must contain explicit origins in production.")
            if any(origin.startswith(("http://localhost", "http://127.0.0.1")) for origin in self.cors_origins):
                raise ValueError("Production FRONTEND_ORIGINS cannot contain a local development origin.")
            if any(marker in self.database_url.upper() for marker in ("USER:PASSWORD", "@HOST/", "/DATABASE")):
                raise ValueError("DATABASE_URL must point to the configured production database.")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
