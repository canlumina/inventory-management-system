from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    project_name: str = "进销存系统"
    version: str = "1.0.0"
    api_v1_str: str = "/api/v1"
    
    # Database
    database_url: str = "postgresql://user:password@localhost/inventory_db"
    
    # Security
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24小时
    
    # CORS
    backend_cors_origins: list = ["http://localhost:3000", "http://localhost:8080"]
    
    class Config:
        env_file = ".env"


settings = Settings()