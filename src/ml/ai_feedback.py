import os
import json
import requests
import asyncio
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from src.backend.core.config import settings

load_dotenv()

class AIFeedbackService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.api_base = settings.openai_api_base
        self.api_url = f"{self.api_base}/chat/completions"
        self.model = settings.openai_model
        
        if not self.api_key:
            print("Warning: OPENAI_API_KEY not found in environment variables")
    
    async def analyze_exercise(self, vectors_data: Dict) -> Dict[str, Any]:
        """
        Sends motion vectors to OpenAI API for analysis
        """
        try:
            # Prepare data for analysis
            analysis_prompt = self.prepare_analysis_prompt(vectors_data)
            
            # Send request to OpenAI
            response = await self.call_openai_api(analysis_prompt)
            
            # Parse response
            feedback = self.parse_ai_response(response)
            
            return feedback
            
        except Exception as e:
            print(f"Error in AI analysis: {str(e)}")
            return self.get_fallback_response(vectors_data)
    
    def prepare_analysis_prompt(self, vectors_data: Dict) -> str:
        """Prepares prompt for movement analysis with quality context"""
        
        movement_analysis = vectors_data.get('movement_analysis', {})
        exercise_type = movement_analysis.get('exercise_type', 'unknown')
        rep_count = vectors_data.get('rep_count', 0)
        duration = vectors_data.get('duration', 0)
        
        # Average angles
        avg_elbow_left = movement_analysis.get('avg_left_elbow_angle', 0)
        avg_elbow_right = movement_analysis.get('avg_right_elbow_angle', 0)
        avg_knee_left = movement_analysis.get('avg_left_knee_angle', 0)
        avg_knee_right = movement_analysis.get('avg_right_knee_angle', 0)
        
        # Range of motion
        elbow_range = movement_analysis.get('elbow_range', 0)
        knee_range = movement_analysis.get('knee_range', 0)
        
        # Quality information
        validation = vectors_data.get('validation', {})
        quality_score = validation.get('quality_score', 1.0)
        quality_warnings = validation.get('quality_warnings', [])
        diagnostics = vectors_data.get('diagnostics', {})
        
        # Quality context for AI
        quality_context = ""
        if quality_score < 0.8 or quality_warnings:
            quality_context = f"""
VIDEO QUALITY CONTEXT:
- Quality score: {quality_score:.2f}/1.0 {'(Limited quality)' if quality_score < 0.8 else '(Good quality)'}
- Quality warnings: {', '.join(quality_warnings) if quality_warnings else 'None'}
- Pose detection: {diagnostics.get('avg_visibility', 0):.2f} average visibility
- Motion score: {diagnostics.get('motion_score', 0):.2f}

IMPORTANT: Due to video quality limitations, focus on general advice rather than detailed biomechanical analysis. 
Be more encouraging and provide foundational tips rather than precise technical corrections.
"""
        
        prompt = f"""
You are a professional fitness trainer and biomechanics expert. Analyze the user's movement data and provide detailed feedback.

EXERCISE DATA:
- Exercise type: {exercise_type}
- Repetition count: {rep_count}
- Duration: {duration:.1f} seconds
- Average left elbow angle: {avg_elbow_left:.1f}°
- Average right elbow angle: {avg_elbow_right:.1f}°
- Average left knee angle: {avg_knee_left:.1f}°
- Average right knee angle: {avg_knee_right:.1f}°
- Elbow range of motion: {elbow_range:.1f}°
- Knee range of motion: {knee_range:.1f}°
{quality_context}
TASK:
Analyze the exercise technique and provide feedback in JSON format:

{{
  "overall_score": number from 1 to 10,
  "exercise_detected": "exercise name",
  "technique_analysis": {{
    "form_quality": "excellent/good/fair/poor",
    "symmetry": "left and right sides are symmetrical/imbalance detected",
    "range_of_motion": "full/limited/excessive",
    "tempo": "appropriate/too fast/too slow"
  }},
  "feedback": {{
    "positive": ["what is being done well"],
    "improvements": ["what needs improvement"],
    "specific_tips": ["specific advice"]
  }},
  "rep_count_accuracy": "accurate/approximate/inaccurate",
  "safety_concerns": ["safety issues if any"]
}}

Respond only with JSON, no additional text.
"""
        
        return prompt
    
    async def call_openai_api(self, prompt: str) -> str:
        """Asynchronous OpenAI API call"""
        
        if not self.api_key:
            raise Exception("OpenAI API key not configured")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        # OpenRouter recommends these headers; harmless elsewhere
        if "openrouter.ai" in self.api_base:
            site = os.getenv("OPENROUTER_SITE_URL", "http://localhost")
            app_title = os.getenv("OPENROUTER_APP_NAME", settings.app_name)
            headers.update({
                "HTTP-Referer": site,
                "X-Title": app_title,
            })
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a professional fitness trainer and movement analysis expert. Respond only in JSON format."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.3
        }
        
        # Use asyncio for non-blocking request
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            lambda: requests.post(self.api_url, headers=headers, json=data, timeout=settings.ai_timeout_seconds)
        )
        
        if response.status_code != 200:
            raise Exception(f"OpenAI API error: {response.status_code} - {response.text}")
        
        result = response.json()
        return result['choices'][0]['message']['content']
    
    def parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """Parses AI response"""
        try:
            # Remove possible markdown blocks
            clean_response = response_text.strip()
            if clean_response.startswith('```json'):
                clean_response = clean_response[7:]
            if clean_response.endswith('```'):
                clean_response = clean_response[:-3]
            
            feedback = json.loads(clean_response.strip())
            
            # Validate response structure
            required_fields = ['overall_score', 'exercise_detected', 'technique_analysis', 'feedback']
            for field in required_fields:
                if field not in feedback:
                    feedback[field] = self.get_default_field_value(field)
            
            return feedback
            
        except json.JSONDecodeError as e:
            print(f"Error parsing AI response: {e}")
            return self.get_default_feedback()
    
    def get_default_field_value(self, field: str) -> Any:
        """Returns default values for fields"""
        defaults = {
            'overall_score': 5,
            'exercise_detected': 'Unrecognized exercise',
            'technique_analysis': {
                'form_quality': 'fair',
                'symmetry': 'requires analysis',
                'range_of_motion': 'requires analysis',
                'tempo': 'requires analysis'
            },
            'feedback': {
                'positive': ['Exercise completed'],
                'improvements': ['Additional analysis required'],
                'specific_tips': ['Keep training']
            }
        }
        return defaults.get(field, 'Not determined')
    
    def get_fallback_response(self, vectors_data: Dict) -> Dict[str, Any]:
        """Fallback response when AI is unavailable"""
        movement_analysis = vectors_data.get('movement_analysis', {})
        exercise_type = movement_analysis.get('exercise_type', 'unknown')
        rep_count = vectors_data.get('rep_count', 0)
        
        exercise_names = {
            'upper_body': 'Upper body exercise',
            'lower_body': 'Lower body exercise', 
            'full_body': 'Functional exercise',
            'unknown': 'Unrecognized exercise'
        }
        
        return {
            'overall_score': 6,
            'exercise_detected': exercise_names.get(exercise_type, 'Unrecognized exercise'),
            'technique_analysis': {
                'form_quality': 'fair',
                'symmetry': 'analysis unavailable',
                'range_of_motion': 'analysis unavailable', 
                'tempo': 'analysis unavailable'
            },
            'feedback': {
                'positive': [f'Completed {rep_count} repetitions', 'Movement detected'],
                'improvements': ['Detailed analysis requires AI connection'],
                'specific_tips': ['Monitor your form', 'Maintain steady pace']
            },
            'rep_count_accuracy': 'approximate',
            'safety_concerns': [],
            'note': 'Analysis performed in basic mode. Full analysis requires AI.'
        }
    
    def get_default_feedback(self) -> Dict[str, Any]:
        """Returns standard feedback"""
        return {
            'overall_score': 5,
            'exercise_detected': 'Exercise detected',
            'technique_analysis': {
                'form_quality': 'requires analysis',
                'symmetry': 'requires analysis',
                'range_of_motion': 'requires analysis',
                'tempo': 'requires analysis'
            },
            'feedback': {
                'positive': ['Exercise completed'],
                'improvements': ['Analysis temporarily unavailable'],
                'specific_tips': ['Keep training']
            },
            'rep_count_accuracy': 'inaccurate',
            'safety_concerns': [],
            'note': 'Standard response - analysis service temporarily unavailable'
        }
