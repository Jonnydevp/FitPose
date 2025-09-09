import json
from typing import Dict, List, Optional, Tuple
import asyncio
import os
import ctypes
import glob

# Force CPU path for MediaPipe in headless servers (Railway)
os.environ.setdefault("MEDIAPIPE_DISABLE_GPU", "1")
os.environ.setdefault("OPENCV_DISABLE_GPU", "1")
os.environ.setdefault("LIBGL_ALWAYS_SOFTWARE", "1")
os.environ.setdefault("MESA_LOADER_DRIVER_OVERRIDE", "llvmpipe")

# Ensure system GL libraries are discoverable at runtime (Railway Ubuntu 24.04)
# Some builds use Nix python which may not see apt-installed libs unless we extend LD_LIBRARY_PATH
_ld_paths = [
    "/usr/lib/x86_64-linux-gnu",
    "/usr/local/lib",
    "/lib/x86_64-linux-gnu",
]
_existing_ld = os.environ.get("LD_LIBRARY_PATH", "")
for p in _ld_paths:
    if p and p not in _existing_ld:
        _existing_ld = f"{p}:{_existing_ld}" if _existing_ld else p
os.environ["LD_LIBRARY_PATH"] = _existing_ld

# Try to preload libGL to avoid 'libGL.so.1: cannot open shared object file'
# 1) Absolute candidates in common locations
_gl_candidates = [
    "/usr/lib/x86_64-linux-gnu/libGL.so.1",
    "/lib/x86_64-linux-gnu/libGL.so.1",
]
for pattern in (
    "/usr/lib/x86_64-linux-gnu/libGL.so*",
    "/lib/x86_64-linux-gnu/libGL.so*",
):
    _gl_candidates.extend(glob.glob(pattern))

_loaded_gl = False
for path in _gl_candidates:
    try:
        if os.path.exists(path):
            # Preload and export LD_PRELOAD so subsequent imports inherit it
            existing_preload = os.environ.get('LD_PRELOAD', '')
            os.environ['LD_PRELOAD'] = f"{path}:{existing_preload}" if existing_preload else path
            ctypes.CDLL(path, mode=getattr(ctypes, "RTLD_GLOBAL", 0))
            _loaded_gl = True
            break
    except OSError:
        continue

# 2) Fallback to sonames if absolute paths failed
if not _loaded_gl:
    # Try preloading GL dispatch/GLX chain first
    for _dep in ("/usr/lib/x86_64-linux-gnu/libGLdispatch.so.0", "/usr/lib/x86_64-linux-gnu/libGLX.so.0"):
        try:
            if os.path.exists(_dep):
                ctypes.CDLL(_dep, mode=getattr(ctypes, "RTLD_GLOBAL", 0))
        except OSError:
            pass
    for _lib in ("libGL.so.1", "libGL.so"):
        try:
            ctypes.CDLL(_lib, mode=getattr(ctypes, "RTLD_GLOBAL", 0))
            _loaded_gl = True
            break
        except OSError:
            continue

# Try to import computer vision libraries
try:
    import cv2
    import mediapipe as mp
    import numpy as np
    CV_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Computer vision libraries not available: {e}")
    CV_AVAILABLE = False
    # Mock objects for deployment without CV
    cv2 = None
    mp = None
    np = None

class VideoProcessor:
    def __init__(self):
        if not CV_AVAILABLE:
            print("Warning: VideoProcessor initialized without computer vision support")
            self.mp_pose = None
            self.pose = None
            return
            
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    
    def calculate_angle(self, a, b, c) -> float:
        """Calculates angle between three points"""
        if not CV_AVAILABLE:
            return 180.0
            
        a = np.array([a.x, a.y])
        b = np.array([b.x, b.y])
        c = np.array([c.x, c.y])

        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
        return np.degrees(angle)
    
    def extract_landmarks_features(self, landmarks) -> Dict:
        """Extracts key angles and coordinates from landmarks"""
        if not landmarks:
            return {}
        
        # Key points
        left_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
        left_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ELBOW]
        left_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]
        left_hip = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP]
        left_knee = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_KNEE]
        left_ankle = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ANKLE]
        
        right_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ELBOW]
        right_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST]
        right_hip = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_HIP]
        right_knee = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_KNEE]
        right_ankle = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ANKLE]
        
        # Calculate angles
        features = {
            # Arm angles
            'left_elbow_angle': self.calculate_angle(left_shoulder, left_elbow, left_wrist),
            'right_elbow_angle': self.calculate_angle(right_shoulder, right_elbow, right_wrist),
            
            # Leg angles
            'left_knee_angle': self.calculate_angle(left_hip, left_knee, left_ankle),
            'right_knee_angle': self.calculate_angle(right_hip, right_knee, right_ankle),
            
            # Hip hinge angles (shoulder-hip-knee)
            'left_hip_angle': self.calculate_angle(left_shoulder, left_hip, left_knee),
            'right_hip_angle': self.calculate_angle(right_shoulder, right_hip, right_knee),
            
            # Shoulder angles
            'left_shoulder_angle': self.calculate_angle(left_elbow, left_shoulder, left_hip),
            'right_shoulder_angle': self.calculate_angle(right_elbow, right_shoulder, right_hip),
            
            # Key point coordinates
            'left_wrist_y': left_wrist.y,
            'right_wrist_y': right_wrist.y,
            'left_knee_y': left_knee.y,
            'right_knee_y': right_knee.y,
            'left_shoulder_y': left_shoulder.y,
            'right_shoulder_y': right_shoulder.y,
            'left_hip_y': left_hip.y,
            'right_hip_y': right_hip.y,
            
            # Point visibility
            'left_elbow_visibility': left_elbow.visibility,
            'right_elbow_visibility': right_elbow.visibility,
            'left_knee_visibility': left_knee.visibility,
            'right_knee_visibility': right_knee.visibility
        }
        
        return features
    
    def calculate_velocity(self, current_features: Dict, previous_features: Dict, fps: float) -> Dict:
        """Calculates velocity of angle changes"""
        velocities = {}
        
        for key in current_features:
            if key in previous_features and isinstance(current_features[key], (int, float)):
                velocity = (current_features[key] - previous_features[key]) * fps
                velocities[f"{key}_velocity"] = velocity
        
        return velocities
    
    async def process_video(self, video_path: str, expected_exercise: Optional[str] = None) -> Optional[Dict]:
        """
        Main video processing function
        Returns movement vectors for GPT analysis (since we don't have our own model)
        """
        if not CV_AVAILABLE:
            print("Warning: Computer vision processing not available")
            return {
                'total_frames': 100,
                'duration': 10.0,
                'fps': 30.0,
                'frames_data': [],
                'movement_analysis': {
                    'exercise_type': 'unknown',
                    'elbow_range': 0,
                    'knee_range': 0,
                    'estimated_reps': 1,
                    'avg_left_elbow_angle': 180,
                    'avg_right_elbow_angle': 180,
                    'avg_left_knee_angle': 180,
                    'avg_right_knee_angle': 180
                },
                'rep_count': 1
            }
            
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print(f"Error opening video: {video_path}")
                return None

            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps
            
            all_frames_data = []
            previous_features = None
            frame_id = 0
            
            print(f"Processing video: {frame_count} frames, {fps} FPS, {duration:.2f}s")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Convert to RGB for MediaPipe
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.pose.process(rgb_frame)
                
                if results.pose_landmarks:
                    # Extract features
                    features = self.extract_landmarks_features(results.pose_landmarks)
                    
                    # Add metadata
                    frame_data = {
                        'frame_id': frame_id,
                        'timestamp': frame_id / fps,
                        **features
                    }
                    
                    # Calculate velocities if previous frame exists
                    if previous_features:
                        velocities = self.calculate_velocity(features, previous_features, fps)
                        frame_data.update(velocities)
                    
                    all_frames_data.append(frame_data)
                    previous_features = features
                
                frame_id += 1
                
                # Allow other tasks to execute
                if frame_id % 30 == 0:
                    await asyncio.sleep(0.01)
            
            cap.release()
            
            if not all_frames_data:
                return None
            
            # Analyze data for rep counting
            analysis_result = self.analyze_movement_patterns(all_frames_data, expected_exercise=expected_exercise)
            
            result = {
                'total_frames': len(all_frames_data),
                'duration': duration,
                'fps': fps,
                'frames_data': all_frames_data,
                'movement_analysis': analysis_result,
                'rep_count': analysis_result.get('estimated_reps', 0)
            }
            
            return result
            
        except Exception as e:
            print(f"Error processing video: {str(e)}")
            return None
    
    def analyze_movement_patterns(self, frames_data: List[Dict], expected_exercise: Optional[str] = None) -> Dict:
        """Analyzes movement patterns to determine exercise type and rep count.
        Uses per-exercise state machines with smoothing and hysteresis.
        """
        if not frames_data:
            return {}

        # Extract time series of angles and coordinates
        left_elbow_angles = [frame.get('left_elbow_angle', 0.0) for frame in frames_data]
        right_elbow_angles = [frame.get('right_elbow_angle', 0.0) for frame in frames_data]
        left_knee_angles = [frame.get('left_knee_angle', 0.0) for frame in frames_data]
        right_knee_angles = [frame.get('right_knee_angle', 0.0) for frame in frames_data]
        left_hip_angles = [frame.get('left_hip_angle', 0.0) for frame in frames_data]
        right_hip_angles = [frame.get('right_hip_angle', 0.0) for frame in frames_data]
        left_wrist_y = [frame.get('left_wrist_y', 0.0) for frame in frames_data]
        right_wrist_y = [frame.get('right_wrist_y', 0.0) for frame in frames_data]
        left_shoulder_y = [frame.get('left_shoulder_y', 0.0) for frame in frames_data]
        right_shoulder_y = [frame.get('right_shoulder_y', 0.0) for frame in frames_data]

        wrist_y = [(l + r) / 2.0 for l, r in zip(left_wrist_y, right_wrist_y)]
        shoulder_y = [(l + r) / 2.0 for l, r in zip(left_shoulder_y, right_shoulder_y)]
        knee_angles = [(l + r) / 2.0 for l, r in zip(left_knee_angles, right_knee_angles)]
        hip_angles = [(l + r) / 2.0 for l, r in zip(left_hip_angles, right_hip_angles)]

        def smooth(series: List[float], window: int = 7) -> List[float]:
            if len(series) < 3:
                return series
            w = max(3, window if window % 2 == 1 else window + 1)
            pad = w // 2
            arr = np.array(series, dtype=float)
            arr = np.pad(arr, (pad, pad), mode='edge')
            kernel = np.ones(w) / w
            sm = np.convolve(arr, kernel, mode='same')[pad:-pad]
            return sm.tolist()

        wrist_y_s = smooth(wrist_y, 7)
        shoulder_y_s = smooth(shoulder_y, 7)
        knee_angles_s = smooth(knee_angles, 7)
        hip_angles_s = smooth(hip_angles, 7)

        # Ranges
        elbow_range = (max(left_elbow_angles + right_elbow_angles) - min(left_elbow_angles + right_elbow_angles))
        knee_range = max(knee_angles_s) - min(knee_angles_s)
        hip_range = max(hip_angles_s) - min(hip_angles_s)
        wrist_y_range = max(wrist_y_s) - min(wrist_y_s)
        shoulder_y_range = max(shoulder_y_s) - min(shoulder_y_s)

        # Determine exercise type (do not override with expected_exercise)
        exercise_type = "unknown"
        if (max(wrist_y_range, shoulder_y_range) > 0.06 and elbow_range > 35 and knee_range < 25):
            exercise_type = "pullup"
        elif knee_range > 55 and max(wrist_y_range, shoulder_y_range) > 0.04:
            exercise_type = "squat"
        elif 25 <= knee_range <= 55 and hip_range > 20 and max(wrist_y_range, shoulder_y_range) <= 0.05:
            exercise_type = "deadlift"
        elif elbow_range > 45 and max(wrist_y_range, shoulder_y_range) <= 0.03 and knee_range < 25:
            exercise_type = "pushup"
        else:
            if elbow_range > 60 and knee_range < 30:
                exercise_type = "upper_body"
            elif knee_range > 30 and elbow_range < 60:
                exercise_type = "lower_body"
            elif elbow_range > 30 and knee_range > 30:
                exercise_type = "full_body"

        # Rep counting with hysteresis
        def count_reps_pullup(y_series: List[float]) -> int:
            y_min, y_max = min(y_series), max(y_series)
            amp = y_max - y_min
            if amp < 0.03:
                return 0
            low = y_min + 0.25 * amp
            high = y_min + 0.75 * amp
            state = 'down'
            reps = 0
            for y in y_series:
                if state == 'down' and y <= low:
                    state = 'up'
                elif state == 'up' and y >= high:
                    reps += 1
                    state = 'down'
            return reps

        def count_reps_angle(angles: List[float], flex_thresh: float, extend_thresh: float, min_amp: float = 20.0) -> int:
            a_min, a_max = min(angles), max(angles)
            if a_max - a_min < min_amp:
                return 0
            state = 'extended'
            reps = 0
            for a in angles:
                if state == 'extended' and a <= flex_thresh:
                    state = 'flexed'
                elif state == 'flexed' and a >= extend_thresh:
                    reps += 1
                    state = 'extended'
            return reps

        estimated_reps = 0
        if exercise_type == 'pullup':
            estimated_reps = count_reps_pullup(shoulder_y_s)
        elif exercise_type == 'squat':
            p30, p70 = np.percentile(knee_angles_s, [30, 70])
            estimated_reps = count_reps_angle(knee_angles_s, p30, p70, min_amp=30.0)
        elif exercise_type == 'deadlift':
            p35, p75 = np.percentile(hip_angles_s, [35, 75])
            estimated_reps = count_reps_angle(hip_angles_s, p35, p75, min_amp=20.0)
        elif exercise_type == 'pushup':
            elbows = smooth([(l + r) / 2.0 for l, r in zip(left_elbow_angles, right_elbow_angles)], 7)
            p35, p75 = np.percentile(elbows, [35, 75])
            estimated_reps = count_reps_angle(elbows, p35, p75, min_amp=25.0)
        else:
            estimated_reps = max(0, int(max(elbow_range, knee_range, hip_range) / 25))

        return {
            'exercise_type': exercise_type,
            'elbow_range': elbow_range,
            'knee_range': knee_range,
            'wrist_y_range': wrist_y_range,
            'shoulder_y_range': shoulder_y_range,
            'estimated_reps': int(min(estimated_reps, 200)),
            'avg_left_elbow_angle': float(np.mean(left_elbow_angles)),
            'avg_right_elbow_angle': float(np.mean(right_elbow_angles)),
            'avg_left_knee_angle': float(np.mean(left_knee_angles)),
            'avg_right_knee_angle': float(np.mean(right_knee_angles))
        }
