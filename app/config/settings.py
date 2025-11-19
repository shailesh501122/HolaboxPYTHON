from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./holabox.db"
    SECRET_KEY: str = "your-secret-key-change-in-production-09876543210"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    STORAGE_PATH: str = "./storage"
    
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024 * 1024
    
    FREE_STORAGE_LIMIT: int = 20 * 1024 * 1024 * 1024
    PREMIUM_STORAGE_LIMIT: int = 1024 * 1024 * 1024 * 1024
    ULTRA_STORAGE_LIMIT: int = 2 * 1024 * 1024 * 1024 * 1024
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
