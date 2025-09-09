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
    
    # OpenAI / LLM Provider
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    # Base URL can be switched to OpenRouter or Azure, etc.
    # Examples:
    #  - OpenAI:    https://api.openai.com/v1
    #  - OpenRouter: https://openrouter.ai/api/v1
    openai_api_base: str = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    # Model name; on OpenRouter prefer vendor-prefixed names, e.g. "openai/gpt-4o-mini"
    openai_model: str = os.getenv("AI_MODEL", "gpt-4")
    ai_timeout_seconds: int = int(os.getenv("AI_TIMEOUT_SECONDS", "30"))
    
    # CORS - Allow Vercel domains and localhost
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173", 
        "http://localhost:8080",
        "https://fit-pose.vercel.app",
        "https://fit-pose-git-main-jonnydevps-projects.vercel.app",
        "https://fit-pose-7x5lbb2vd-jonnydevps-projects.vercel.app",
        "*"  # Allow all origins for testing
    ]
    
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
