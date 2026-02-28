from typing import List
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "CodeViz 2.0"
    API_V1_STR: str = "/api/v1"
    # In production, this should be a comma-separated list of allowed origins
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    NGROK_KAGGLE_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
