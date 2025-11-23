import os
from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv

# Načtení .env souboru
load_dotenv()


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    app_name: str = "Compute Gateway API"
    app_version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    debug: bool = False
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    
    # Compute Service Configuration
    compute_service_url: str = "localhost:50051"
    grpc_timeout: int = 30
    grpc_max_retries: int = 3
    
    # Rate Limiting
    rate_limit_per_minute: int = 100
    rate_limit_burst: int = 20
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    # CORS
    cors_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]
    
    # Monitoring
    enable_metrics: bool = True
    metrics_port: int = 9090
    
    # Security
    api_key_header: str = "X-API-Key"
    enable_api_key_auth: bool = False
    valid_api_keys: list[str] = []
    
    # OpenAI Configuration
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_max_tokens: int = 1000
    openai_temperature: float = 0.7
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignorovat extra fieldy z .env


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
