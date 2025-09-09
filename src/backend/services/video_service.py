"""
Service for video file processing
"""
import os
import tempfile
from typing import Optional, Dict, Any
from fastapi import UploadFile, HTTPException

from src.cv.video_processor import VideoProcessor
from src.backend.core.config import settings


class VideoService:
    def __init__(self):
        self.video_processor = VideoProcessor()
        self.max_file_size = settings.max_file_size_mb * 1024 * 1024  # MB to bytes
        self.supported_formats = settings.supported_video_formats
    
    async def validate_video_file(self, file: UploadFile) -> None:
        """Validates video file"""
        # Check file type
        if not file.content_type or not file.content_type.startswith('video/'):
            raise HTTPException(
                status_code=400, 
                detail="File must be a video"
            )
        
        # Check extension
        if file.filename:
            extension = file.filename.split('.')[-1].lower()
            if extension not in self.supported_formats:
                raise HTTPException(
                    status_code=400,
                    detail=f"Supported formats: {', '.join(self.supported_formats)}"
                )
        
        # Check file size
        file.file.seek(0, 2)  # Move to end of file
        file_size = file.file.tell()
        file.file.seek(0)  # Return to beginning
        
        if file_size > self.max_file_size:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.max_file_size_mb}MB"
            )
    
    async def save_temp_video(self, file: UploadFile) -> str:
        """Saves video to temporary file"""
        # Create temporary file
        suffix = '.mp4'
        if file.filename:
            extension = file.filename.split('.')[-1].lower()
            suffix = f'.{extension}'
        
        # Ensure temp_dir exists
        temp_dir = settings.temp_dir
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir, exist_ok=True)
        
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, 
            suffix=suffix,
            dir=temp_dir
        )
        temp_path = temp_file.name
        
        # Write file synchronously (simpler for Railway)
        content = await file.read()
        temp_file.write(content)
        temp_file.close()
        
        return temp_path
    
    def _normalize_exercise(self, name: Optional[str]) -> Optional[str]:
        if not name:
            return None
        key = name.strip().lower().replace(" ", "").replace("-", "")
        aliases = {
            "pullups": "pullup",
            "pullup": "pullup",
            "chinups": "pullup",
            "deadlift": "deadlift",
            "deadlifts": "deadlift",
            "squat": "squat",
            "squats": "squat",
            "pushup": "pushup",
            "pushups": "pushup",
            "burpee": "burpee",
            "burpees": "burpee",
            "lunge": "lunge",
            "lunges": "lunge",
            "plank": "plank",
        }
        return aliases.get(key, key)

    async def process_video(self, file: UploadFile, expected_exercise: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Complete video file processing"""
        temp_path = None
        expected_norm = self._normalize_exercise(expected_exercise)
        
        try:
            # Validate file
            await self.validate_video_file(file)
            
            # Save to temporary file
            temp_path = await self.save_temp_video(file)
            
            # Process video
            result = await self.video_processor.process_video(temp_path, expected_exercise=expected_norm)
            
            if not result:
                raise HTTPException(
                    status_code=422,
                    detail="Failed to process video. Please check video quality and content."
                )
            
            # If client provided expected exercise, validate mismatch
            detected = result.get('movement_analysis', {}).get('exercise_type')
            if expected_norm and detected and expected_norm != detected:
                raise HTTPException(
                    status_code=400,
                    detail=f"Exercise mismatch: expected '{expected_norm}', detected '{detected}'"
                )
            
            return result
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Video processing error: {str(e)}"
            )
        finally:
            # Remove temporary file
            if temp_path and os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except Exception as e:
                    print(f"Warning: Could not delete temp file {temp_path}: {e}")
    
    def cleanup_temp_files(self):
        """Cleanup old temporary files"""
        # Can add logic for cleaning old files
        pass
