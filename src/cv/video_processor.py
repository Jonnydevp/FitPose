import cv2
import mediapipe as mp
import numpy as np
import json
from typing import Dict, List, Optional, Tuple
import asyncio

class VideoProcessor:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    
    def calculate_angle(self, a, b, c) -> float:
        """Calculates angle between three points"""
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
            
            # Shoulder angles
            'left_shoulder_angle': self.calculate_angle(left_elbow, left_shoulder, left_hip),
            'right_shoulder_angle': self.calculate_angle(right_elbow, right_shoulder, right_hip),
            
            # Key point coordinates
            'left_wrist_y': left_wrist.y,
            'right_wrist_y': right_wrist.y,
            'left_knee_y': left_knee.y,
            'right_knee_y': right_knee.y,
            
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
    
    async def process_video(self, video_path: str) -> Optional[Dict]:
        """
        Main video processing function
        Returns movement vectors for GPT analysis (since we don't have our own model)
        """
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
            analysis_result = self.analyze_movement_patterns(all_frames_data)
            
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
    
    def analyze_movement_patterns(self, frames_data: List[Dict]) -> Dict:
        """Analyzes movement patterns to determine exercise type and rep count"""
        if not frames_data:
            return {}
        
        # Extract time series of angles
        left_elbow_angles = [frame.get('left_elbow_angle', 0) for frame in frames_data]
        right_elbow_angles = [frame.get('right_elbow_angle', 0) for frame in frames_data]
        left_knee_angles = [frame.get('left_knee_angle', 0) for frame in frames_data]
        right_knee_angles = [frame.get('right_knee_angle', 0) for frame in frames_data]
        
        # Simple analysis for exercise type detection
        elbow_range = max(left_elbow_angles + right_elbow_angles) - min(left_elbow_angles + right_elbow_angles)
        knee_range = max(left_knee_angles + right_knee_angles) - min(left_knee_angles + right_knee_angles)
        
        # Determine exercise type
        exercise_type = "unknown"
        if elbow_range > 60 and knee_range < 30:
            exercise_type = "upper_body"  # push-ups, pull-ups
        elif knee_range > 30 and elbow_range < 60:
            exercise_type = "lower_body"  # squats, lunges
        elif elbow_range > 30 and knee_range > 30:
            exercise_type = "full_body"   # burpees
        
        # Simple rep counting (movement peaks)
        estimated_reps = max(1, int(elbow_range / 20) if exercise_type == "upper_body" else int(knee_range / 20))
        
        return {
            'exercise_type': exercise_type,
            'elbow_range': elbow_range,
            'knee_range': knee_range,
            'estimated_reps': min(estimated_reps, 50),  # maximum 50 reps
            'avg_left_elbow_angle': np.mean(left_elbow_angles),
            'avg_right_elbow_angle': np.mean(right_elbow_angles),
            'avg_left_knee_angle': np.mean(left_knee_angles),
            'avg_right_knee_angle': np.mean(right_knee_angles)
        }
