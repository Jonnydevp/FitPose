"""
Data schemas for API
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class TechniqueAnalysis:
    """Exercise technique analysis"""
    form_quality: str
    symmetry: str
    range_of_motion: str
    tempo: str


@dataclass
class Feedback:
    """Feedback"""
    positive: List[str]
    improvements: List[str]
    specific_tips: List[str]


@dataclass
class AIAnalysisResult:
    """AI analysis result"""
    overall_score: int
    exercise_detected: str
    technique_analysis: TechniqueAnalysis
    feedback: Feedback
    rep_count_accuracy: str
    safety_concerns: List[str]
    note: Optional[str] = None


@dataclass
class ExerciseMetrics:
    """Exercise metrics"""
    rep_count: int
    total_frames: int
    duration: float
    fps: Optional[float] = None


@dataclass
class MovementAnalysis:
    """Movement analysis"""
    exercise_type: str
    elbow_range: float
    knee_range: float
    estimated_reps: int
    avg_left_elbow_angle: float
    avg_right_elbow_angle: float
    avg_left_knee_angle: float
    avg_right_knee_angle: float


@dataclass
class AnalysisResponse:
    """Exercise analysis response"""
    status: str
    analysis: Dict[str, Any]
    metrics: Dict[str, Any]


@dataclass
class ErrorResponse:
    """Error response"""
    detail: str
    error_code: Optional[str] = None


@dataclass
class HealthResponse:
    """Health check response"""
    status: str
    version: str
    timestamp: str
