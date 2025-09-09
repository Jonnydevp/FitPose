"""
System API routes
"""
from datetime import datetime
from fastapi import APIRouter

from src.backend.core.config import settings
from src.cv.video_processor import VideoProcessor
import os

router = APIRouter(tags=["system"])


@router.get(
    "/",
    summary="Root endpoint",
    description="Returns service information"
)
async def root():
    """Root endpoint"""
    return {
        "message": f"{settings.app_name} is running!",
        "version": settings.app_version,
        "docs": "/docs"
    }


@router.get(
    "/health",
    summary="Service health check",
    description="Health check endpoint for monitoring"
)
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "timestamp": datetime.now().isoformat()
    }


@router.get(
    "/debug/cv",
    summary="Computer vision status",
    description="Returns availability of CV stack and basic environment info"
)
async def cv_debug():
    vp = VideoProcessor()
    info = {
        "cv_available": vp.pose is not None,
        "mediapipe_disable_gpu": os.getenv("MEDIAPIPE_DISABLE_GPU", ""),
    }
    try:
        import cv2  # type: ignore
        info["opencv_version"] = getattr(cv2, "__version__", "unknown")
    except Exception as e:
        info["opencv_error"] = str(e)
    try:
        import mediapipe as mp  # type: ignore
        info["mediapipe_version"] = getattr(mp, "__version__", "unknown")
    except Exception as e:
        info["mediapipe_error"] = str(e)
    try:
        import numpy as np  # type: ignore
        info["numpy_version"] = getattr(np, "__version__", "unknown")
    except Exception as e:
        info["numpy_error"] = str(e)

    return info
