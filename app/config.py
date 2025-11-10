"""Application configuration management"""
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    database_url: str
    db_user: str = "energy_user"
    db_password: str = "energy_password"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "smart_energy"
    environment: str = "development"
    debug: bool = False
    log_level: str = "INFO"
    api_title: str = "Smart Energy Monitoring API"
    api_version: str = "1.0.0"
    cors_origins: List[str] = ["http://localhost:3000"]
    model_path: str = "./ml/models/lstm_model.h5"
    batch_size: int = 32
    epochs: int = 50
    lookback_window: int = 48
    synthetic_data_enabled: bool = True
    sensor_count: int = 3
    data_generation_interval: int = 60
    cache_expiration: int = 3600
    redis_url: str = "redis://localhost:6379"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()