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

    # Gates thresholds (tunable via env)
    # Level 1: Critical gates (blocking) - только для явно плохих видео
    person_frames_ratio_min: float = float(os.getenv("PERSON_FRAMES_RATIO_MIN", "0.10"))  # Снижено с 0.20
    person_avg_visibility_min: float = float(os.getenv("PERSON_AVG_VIS_MIN", "0.35"))     # Снижено с 0.50
    person_min_keypoints: int = int(os.getenv("PERSON_MIN_KEYPOINTS", "6"))               # Снижено с 8

    motion_score_min: float = float(os.getenv("MOTION_SCORE_MIN", "0.40"))                # Снижено с 0.70
    exercise_confidence_min: float = float(os.getenv("EXERCISE_CONF_MIN", "0.60"))
    
    # Level 2: Quality gates (warnings) - для информирования AI о качестве
    person_frames_ratio_good: float = float(os.getenv("PERSON_FRAMES_RATIO_GOOD", "0.30"))
    person_avg_visibility_good: float = float(os.getenv("PERSON_AVG_VIS_GOOD", "0.60"))
    motion_score_good: float = float(os.getenv("MOTION_SCORE_GOOD", "0.80"))


# Global settings
settings = Settings()
