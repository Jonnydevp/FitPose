"""
API routes for exercise analysis
"""
from typing import Dict, Any, Optional
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse

from src.backend.services.video_service import VideoService
from src.backend.services.analysis_service import AnalysisService

router = APIRouter(prefix="/api/v1", tags=["exercise"])


@router.post(
    "/analyze-exercise",
    summary="Exercise analysis by video",
    description="""
    Uploads video file, processes it to extract movement vectors,
    sends data to AI for analysis and returns detailed feedback.
    
    Supported formats: MP4, AVI, MOV, MKV
    Maximum file size: 50MB
    """
)
async def analyze_exercise(
    file: UploadFile = File(...),
    exercise_type: Optional[str] = Form(None),
    strict: Optional[bool] = Form(False),
):
    """Main endpoint for exercise analysis"""
    
    video_service = VideoService()
    analysis_service = AnalysisService()
    
    # Process video
    vectors_data = await video_service.process_video(
        file,
        expected_exercise=exercise_type,
        strict=bool(strict),
    )
    
    # Analyze with AI
    result = await analysis_service.analyze_exercise_data(vectors_data)
    
    return JSONResponse(content=result)


@router.post(
    "/analyze-vectors",
    summary="Analysis of motion vectors",
    description="Analyzes extracted motion vectors using AI"
)
async def analyze_vectors(vectors_data: Dict[str, Any]):
    """Endpoint for analyzing motion vectors"""
    
    analysis_service = AnalysisService()
    
    # Validate data
    if not analysis_service.validate_vectors_data(vectors_data):
        raise HTTPException(
            status_code=400,
            detail="Invalid motion vector data format"
        )
    
    # Analyze with AI
    result = await analysis_service.analyze_exercise_data(vectors_data)
    
    return JSONResponse(content=result)
