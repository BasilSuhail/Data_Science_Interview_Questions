"""
AI Interview Coach

Combines your curated question database with AI-powered evaluation.

Example:
    from ai_coach import InterviewCoach

    coach = InterviewCoach()
    coach.conduct_interview(question_type="ml", difficulty="medium")
"""

from .interview_coach import InterviewCoach
from .gemini_evaluator import GeminiEvaluator

__version__ = "1.0.0"
__all__ = ["InterviewCoach", "GeminiEvaluator"]
