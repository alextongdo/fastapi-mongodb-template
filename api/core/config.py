from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    APP_NAME: str = "FastAPI MongoDB Template"
    DEBUG: bool = False
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]
    SECRET_KEY: str
    SEED_IF_EMPTY: bool = False

    # Auth0
    ENABLE_FAKE_AUTH: bool = False
    AUTH0_DOMAIN: str
    AUTH0_API_AUDIENCE: str
    AUTH0_ISSUER: str
    AUTH0_ALGORITHMS: list[str] = ["RS256"]

    MONGO_URI: str
    MONGO_DB_NAME: str = "database"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
