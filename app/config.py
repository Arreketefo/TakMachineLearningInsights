import os
from typing import Optional

class Settings:
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "TAK Server ML Processor"
    
    # API Key Settings
    API_KEY: str = os.getenv("API_KEY", "default_secure_key")
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    # ML Model Settings
    MODEL_PATH: Optional[str] = os.getenv("MODEL_PATH", "models/isolation_forest.joblib")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000

settings = Settings()
