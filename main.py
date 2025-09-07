"""
FitPose API - AI-powered exercise analysis
"""
try:
    import uvicorn
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
except ImportError as e:
    print(f"❌ Missing dependencies: {e}")
    print("📦 Run: pip install -r requirements.txt")
    exit(1)

from src.backend.core.config import settings
from src.backend.api.system_routes import router as system_router
from src.backend.api.exercise_routes import router as exercise_router


def create_app() -> FastAPI:
    """Creates and configures FastAPI application"""
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AI-powered exercise analysis API",
        debug=settings.debug
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Connect routes
    app.include_router(system_router)
    app.include_router(exercise_router)
    
    return app


# Create application
app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
