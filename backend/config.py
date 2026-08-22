import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./tutor.db"
    GROK_API_KEY: str = "mock_key"
    JWT_SECRET: str = "super_secret_key"
    MCP_SERVER_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
