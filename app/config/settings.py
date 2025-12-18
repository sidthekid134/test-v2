import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    APP_NAME: str = "11"
    APP_VERSION: str = "0.1.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./eleven.db")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    class Config:
        env_file = ".env"

settings = Settings()