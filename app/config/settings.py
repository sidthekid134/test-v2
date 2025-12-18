import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    
    APP_NAME: str = "11"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./11.db"
    
    class Config:
        env_file = ".env"
        
settings = Settings()