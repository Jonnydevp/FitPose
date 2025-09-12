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

    async def process_video(
        self,
        file: UploadFile,
        expected_exercise: Optional[str] = None,
        strict: bool = False,
    ) -> Optional[Dict[str, Any]]:
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
            # Gates: person presence and motion sufficiency
            result = self._apply_gates(result)

            # If client provided expected exercise, validate mismatch
            detected = result.get('movement_analysis', {}).get('exercise_type')
            if expected_norm and detected and expected_norm != detected:
                # If detection failed ('unknown'), do not hard-fail even in strict mode
                if strict and detected != 'unknown':
                    raise HTTPException(
                        status_code=400,
                        detail=f"Exercise mismatch: expected '{expected_norm}', detected '{detected}'"
                    )
                # Attach validation info
                result.setdefault('validation', {})
                result['validation'].update({
                    'expected_exercise': expected_norm,
                    'detected_exercise': detected,
                    'match': detected == expected_norm
                })
            elif expected_norm and detected:
                result.setdefault('validation', {})
                result['validation'].update({
                    'expected_exercise': expected_norm,
                    'detected_exercise': detected,
                    'match': True
                })
            
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

    def _apply_gates(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Person/Motion gates with diagnostics. Raises HTTPException on failure."""
        frames = result.get('frames_data', [])
        movement = result.get('movement_analysis', {})
        fps = result.get('fps') or 30.0
        source_total = int(result.get('source_total_frames') or len(frames))

        frames_with_pose = len(frames)
        ratio = (frames_with_pose / source_total) if source_total else 0.0
        # visibility stats
        vis_keys = [
            'left_shoulder_visibility','right_shoulder_visibility',
            'left_hip_visibility','right_hip_visibility',
            'left_knee_visibility','right_knee_visibility',
            'left_elbow_visibility','right_elbow_visibility'
        ]
        vis_vals = []
        min_kp = 0
        if frames:
            counts = []
            for f in frames:
                cnt = 0
                for k in vis_keys:
                    v = f.get(k)
                    if isinstance(v,(int,float)):
                        vis_vals.append(v)
                        if v > 0.5:
                            cnt += 1
                counts.append(cnt)
            min_kp = min(counts) if counts else 0
        avg_vis = (sum(vis_vals)/len(vis_vals)) if vis_vals else 0.0

        diagnostics = result.setdefault('diagnostics', {})
        diagnostics.update({
            'frames_with_pose_ratio': round(ratio,3),
            'avg_visibility': round(avg_vis,3),
            'min_keypoints_per_frame': int(min_kp),
            'source_total_frames': source_total,
            'sample_fps': fps,
        })

        if ratio < 0.30 or avg_vis < 0.60 or min_kp < 10:
            raise HTTPException(
                status_code=422,
                detail={
                    'status':'error',
                    'code':'NO_PERSON',
                    'message':'No person detected in the video',
                    'tips':[ 'Ensure full body is in frame', 'Improve lighting', 'Keep camera steady' ],
                    'diagnostics': diagnostics
                }
            )

        # Motion Gate
        amp = {
            'elbow': float(movement.get('elbow_range',0.0)),
            'knee': float(movement.get('knee_range',0.0)),
            'shoulderY': float(movement.get('shoulder_y_range',0.0)),
            'wristY': float(movement.get('wrist_y_range',0.0)),
        }
        motion_score = max(
            amp['elbow']/25.0,
            amp['knee']/25.0,
            (amp['shoulderY']/0.05) if 0.05 else 0.0,
            (amp['wristY']/0.05) if 0.05 else 0.0,
        )
        diagnostics.update({'motion_amplitude': amp, 'motion_score': round(motion_score,2)})
        if motion_score < 1.0:
            raise HTTPException(
                status_code=422,
                detail={
                    'status':'error',
                    'code':'INSUFFICIENT_MOTION',
                    'message':'Insufficient motion for analysis',
                    'tips':[ 'Perform at least one full repetition', 'Increase movement amplitude' ],
                    'diagnostics': diagnostics
                }
            )

        # Attach confidence for downstream/front diagnostics
        conf = float(movement.get('confidence',0.0))
        result.setdefault('validation', {})
        result['validation'].update({'confidence': round(conf,2)})
        return result
