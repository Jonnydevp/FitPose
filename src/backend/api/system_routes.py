"""
System API routes
"""
from datetime import datetime
from fastapi import APIRouter

from src.backend.core.config import settings

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
