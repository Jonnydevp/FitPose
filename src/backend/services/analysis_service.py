"""
Service for AI analysis
"""
from typing import Dict, Any
from fastapi import HTTPException

from src.ml.ai_feedback import AIFeedbackService
from src.backend.core.config import settings


class AnalysisService:
    def __init__(self):
        self.ai_service = AIFeedbackService()
    
    async def analyze_exercise_data(self, vectors_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyzes exercise data using AI"""
        try:
            # Get AI analysis
            ai_result = await self.ai_service.analyze_exercise(vectors_data)
            
            # Format complete response
            response = {
                "status": "success",
                "analysis": ai_result,
                "metrics": {
                    "rep_count": vectors_data.get("rep_count", 0),
                    "total_frames": vectors_data.get("total_frames", 0),
                    "duration": vectors_data.get("duration", 0),
                    "fps": vectors_data.get("fps")
                }
            }
            
            return response
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"AI analysis error: {str(e)}"
            )
    
    def validate_vectors_data(self, data: Dict[str, Any]) -> bool:
        """Validates vector data"""
        required_fields = ['total_frames', 'duration', 'frames_data']
        
        for field in required_fields:
            if field not in data:
                return False
        
        if not data['frames_data'] or len(data['frames_data']) == 0:
            return False
        
        return True
