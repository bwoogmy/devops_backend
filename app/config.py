from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "Twitter Clone API"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    
    # Database settings - can use full URL or separate vars
    database_url: Optional[str] = None
    postgres_host: Optional[str] = None
    postgres_port: int = 5432
    postgres_user: Optional[str] = None
    postgres_password: Optional[str] = None
    postgres_db: Optional[str] = None
    
    host: str = "0.0.0.0"
    port: int = 8000
    
    @property
    def db_url(self) -> str:
        """Build database URL from components or use provided URL"""
        if self.database_url:
            return self.database_url
        
        if all([self.postgres_host, self.postgres_user, self.postgres_password, self.postgres_db]):
            return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        
        raise ValueError("Either DATABASE_URL or POSTGRES_* variables must be set")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings():
    return Settings()