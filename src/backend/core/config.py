"""
Main application settings
"""
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings"""
    
    # Main settings
    app_name: str = "FitPose API"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Server
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("AI_MODEL", "gpt-4")
    ai_timeout_seconds: int = int(os.getenv("AI_TIMEOUT_SECONDS", "30"))
    
    # CORS
    cors_origins: List[str] = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Files
    max_file_size_mb: int = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
    supported_video_formats: List[str] = os.getenv(
        "SUPPORTED_VIDEO_FORMATS", 
        "mp4,avi,mov,mkv"
    ).split(",")
    
    # Paths (Railway compatible)
    temp_dir: str = os.getenv("TEMP_DIR", "/tmp" if os.name == "posix" else "temp")


# Global settings
settings = Settings()
