import os
from pydantic import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    """Application settings."""
    APP_NAME: str = "11 API"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "API for implementing '11' efficiently"
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./eleven.db")
    
    # API settings
    API_PREFIX: str = "/api"
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Eleven-specific settings
    ELEVEN_VALUE: int = 11
    ELEVEN_PATTERNS_ENABLED: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()