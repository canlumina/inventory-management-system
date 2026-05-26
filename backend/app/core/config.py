from pydantic import model_validator
from pydantic_settings import BaseSettings
from typing import ClassVar, Optional


class Settings(BaseSettings):
    project_name: str = "进销存系统"
    version: str = "1.0.0"
    api_v1_str: str = "/api/v1"
    environment: str = "development"

    insecure_secret_keys: ClassVar[set[str]] = {
        "your-secret-key-here",
        "your-secret-key-here-change-in-production",
        "your-secret-key-here-please-change-this-in-production",
    }
    insecure_admin_passwords: ClassVar[set[str]] = {"admin", "admin123", "password"}
    insecure_database_url_fragments: ClassVar[tuple[str, ...]] = (
        ":password@",
        "user:password@",
    )
    
    # Database
    database_url: str = "postgresql://user:password@localhost/inventory_db"
    
    # Security
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24小时

    # Development bootstrap
    create_default_admin: bool = False
    default_admin_username: str = "admin"
    default_admin_email: str = "admin@example.com"
    default_admin_password: Optional[str] = None
    
    # CORS
    backend_cors_origins: list = ["http://localhost:3000", "http://localhost:8080"]

    @model_validator(mode="after")
    def validate_production_security(self):
        if self.environment.lower() != "production":
            return self

        if self.secret_key in self.insecure_secret_keys or len(self.secret_key) < 32:
            raise ValueError(
                "SECRET_KEY must be unique and at least 32 characters when ENVIRONMENT=production"
            )

        if any(fragment in self.database_url for fragment in self.insecure_database_url_fragments):
            raise ValueError(
                "DATABASE_URL must not use the default database password when ENVIRONMENT=production"
            )

        if self.create_default_admin and (
            not self.default_admin_password
            or self.default_admin_password in self.insecure_admin_passwords
        ):
            raise ValueError(
                "DEFAULT_ADMIN_PASSWORD must be non-default when CREATE_DEFAULT_ADMIN=true and ENVIRONMENT=production"
            )

        return self
    
    class Config:
        env_file = ".env"


settings = Settings()
