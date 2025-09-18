"""
Application configuration settings
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Satoshi Sensei"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # API
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_HOSTS: List[str] = [
        "http://localhost:3000", 
        "http://localhost:8000",
        "https://satochi-sensei.netlify.app",
        "https://main--satochi-sensei.netlify.app"
    ]
    
    # Database
    DATABASE_URL: str = "sqlite:///./satoshi_sensei.db"
    DATABASE_TEST_URL: str = "sqlite:///./satoshi_sensei_test.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 300  # 5 minutes
    
    # Groq API
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama3-8b-8192"
    
    # Stacks Network
    STACKS_NETWORK: str = "testnet"  # mainnet or testnet
    STACKS_API_URL: str = "https://api.testnet.hiro.so"
    STACKS_EXPLORER_URL: str = "https://explorer.stacks.co"
    
    # Bitcoin
    BITCOIN_NETWORK: str = "testnet"  # mainnet or testnet
    BITCOIN_API_URL: str = "https://blockstream.info/testnet/api"
    
    # DeFi APIs
    ALEX_API_URL: str = "https://api.alexlab.co/v1"
    ARKADIKO_API_URL: str = "https://api.arkadiko.finance"
    VELAR_API_URL: str = "https://api.velar.co"
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    PROMETHEUS_ENABLED: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
