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
            movement = result.get('movement_analysis', {})
            detected = movement.get('exercise_type')
            conf = float(movement.get('confidence', 0.0))
            if expected_norm and detected and expected_norm != detected:
                # If detection failed ('unknown'), do not hard-fail even in strict mode
                if strict and detected != 'unknown' and conf >= settings.exercise_confidence_min:
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
        """Многоуровневая валидация: критичные проверки + качественные предупреждения"""
        frames = result.get('frames_data', [])
        movement = result.get('movement_analysis', {})
        fps = result.get('fps') or 30.0
        source_total = int(result.get('source_total_frames') or len(frames))

        frames_with_pose = len(frames)
        ratio = (frames_with_pose / source_total) if source_total else 0.0
        
        # Статистика видимости
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

        # Диагностика
        diagnostics = result.setdefault('diagnostics', {})
        diagnostics.update({
            'frames_with_pose_ratio': round(ratio,3),
            'avg_visibility': round(avg_vis,3),
            'min_keypoints_per_frame': int(min_kp),
            'source_total_frames': source_total,
            'sample_fps': fps,
        })

        # 🚫 УРОВЕНЬ 1: КРИТИЧНЫЕ ПРОВЕРКИ (блокирующие)
        # Только для явно неподходящих видео
        if ratio < settings.person_frames_ratio_min or avg_vis < settings.person_avg_visibility_min or min_kp < settings.person_min_keypoints:
            raise HTTPException(
                status_code=422,
                detail={
                    'status':'error',
                    'code':'NO_PERSON',
                    'message':'No person detected in the video',
                    'tips':[ 
                        'Ensure full body is visible in frame', 
                        'Improve lighting and camera angle', 
                        'Keep camera steady and avoid motion blur',
                        'Stand closer to camera or zoom in'
                    ],
                    'diagnostics': diagnostics
                }
            )

        # Анализ движения
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
        
        # Адаптивный порог для низкого FPS
        motion_threshold = settings.motion_score_min - (0.15 if fps and fps < 20 else 0.0)
        rep_count = int(movement.get('estimated_reps', 0))
        
        # Блокируем только если совсем нет движения И нет повторений
        if motion_score < motion_threshold and rep_count < 1:
            raise HTTPException(
                status_code=422,
                detail={
                    'status':'error',
                    'code':'INSUFFICIENT_MOTION',
                    'message':'Insufficient motion for exercise analysis',
                    'tips':[ 
                        'Perform at least one complete repetition', 
                        'Make movements more pronounced',
                        'Ensure you\'re doing the exercise throughout the video',
                        'Check that your full body is visible'
                    ],
                    'diagnostics': diagnostics
                }
            )

        # 🟡 УРОВЕНЬ 2: КАЧЕСТВЕННЫЕ ПРЕДУПРЕЖДЕНИЯ (не блокирующие)
        quality_warnings = []
        quality_score = 1.0
        
        if ratio < settings.person_frames_ratio_good:
            quality_warnings.append("Person visibility could be improved")
            quality_score *= 0.8
            
        if avg_vis < settings.person_avg_visibility_good:
            quality_warnings.append("Pose detection quality is low")
            quality_score *= 0.8
            
        if motion_score < settings.motion_score_good:
            quality_warnings.append("Movement amplitude is limited")
            quality_score *= 0.9

        # Информация о качестве для AI
        result.setdefault('validation', {})
        result['validation'].update({
            'quality_score': round(quality_score, 2),
            'quality_warnings': quality_warnings,
            'confidence': round(float(movement.get('confidence',0.0)), 2)
        })
        
        return result
