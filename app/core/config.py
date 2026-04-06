from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration using Pydantic Settings."""

    # Database
    database_url: str = "postgresql://relay:relay@localhost:5432/relay"

    # App
    app_name: str = "Relay URL Shortener"
    app_version: str = "0.1.0"
    base_url: str = "http://localhost:8000"

    class Config:
        env_file = ".env"


settings = Settings()