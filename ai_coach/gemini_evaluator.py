"""
AI Interview Coach - Answer Evaluation Module

Uses Gemini 2.5 Flash to evaluate user answers and provide structured feedback.
Based on the Kaggle AI Interview Coach implementation.

Features:
- Score answers (0-10)
- Identify strengths
- Suggest improvements
- Provide actionable feedback
"""

import json
import re
import os
from typing import Dict, List, Optional

try:
    from google import genai
except ImportError:
    print("⚠️  google-genai not installed. Run: pip install google-genai")
    raise


class GeminiEvaluator:
    """Evaluates interview answers using Gemini 2.5 Flash."""

    EVALUATION_PROMPT = """
You are an expert interview evaluator for data science and software engineering roles.

Evaluate the candidate's answer in these categories:
- Clarity: Is the answer clear and well-structured?
- Relevance: Does it directly answer the question?
- Technical Depth: Shows understanding of concepts?
- Communication: Professional and articulate?
- Completeness: Covers key points?

Return ONLY this JSON format (no markdown, no code blocks):

{{
  "score": <0-10>,
  "strengths": ["point 1", "point 2", "point 3"],
  "improvements": ["point 1", "point 2"],
  "final_comment": "2-3 sentence summary with actionable advice"
}}

Question: {question}
Answer: {answer}
Role: {role}
Question Type: {question_type}
"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini evaluator.

        Args:
            api_key: Gemini API key. If None, reads from GEMINI_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "Gemini API key required. Set GEMINI_API_KEY environment variable "
                "or pass api_key parameter."
            )

        # Initialize Gemini client
        self.client = genai.Client(api_key=self.api_key)
        self.model = "models/gemini-2.5-flash"

    def evaluate_answer(
        self,
        question: str,
        answer: str,
        role: str = "Data Scientist",
        question_type: str = "general"
    ) -> Dict:
        """
        Evaluate a candidate's answer to an interview question.

        Args:
            question: The interview question
            answer: The candidate's answer
            role: Job role (e.g., "Data Scientist", "ML Engineer")
            question_type: Type of question (ml, stats, sql, coding, etc.)

        Returns:
            Dictionary with evaluation results:
            {
                "score": 0-10,
                "strengths": ["..."],
                "improvements": ["..."],
                "final_comment": "..."
            }
        """
        # Format prompt
        prompt = self.EVALUATION_PROMPT.format(
            question=question,
            answer=answer,
            role=role,
            question_type=question_type
        )

        # Call Gemini API
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            response_text = response.text

            # Parse JSON response
            return self._parse_response(response_text)

        except Exception as e:
            return {
                "error": f"Evaluation failed: {str(e)}",
                "score": 0,
                "strengths": [],
                "improvements": ["Error occurred during evaluation"],
                "final_comment": "Unable to evaluate answer due to technical error."
            }

    def _parse_response(self, response_text: str) -> Dict:
        """Parse Gemini response and extract JSON."""
        # Remove markdown code blocks
        cleaned = response_text.replace("```json", "").replace("```", "").strip()

        # Extract JSON object
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)

        if match:
            try:
                result = json.loads(match.group(0))

                # Validate required fields
                required_fields = ["score", "strengths", "improvements", "final_comment"]
                if all(field in result for field in required_fields):
                    return result

            except json.JSONDecodeError:
                pass

        # Fallback: return raw response
        return {
            "error": "Failed to parse response",
            "raw_response": response_text,
            "score": 0,
            "strengths": [],
            "improvements": ["Could not parse evaluation"],
            "final_comment": "Evaluation format error."
        }

    def batch_evaluate(
        self,
        qa_pairs: List[Dict],
        role: str = "Data Scientist"
    ) -> List[Dict]:
        """
        Evaluate multiple question-answer pairs.

        Args:
            qa_pairs: List of dicts with 'question', 'answer', 'question_type' keys
            role: Job role for context

        Returns:
            List of evaluation results
        """
        results = []

        for i, pair in enumerate(qa_pairs):
            print(f"Evaluating answer {i+1}/{len(qa_pairs)}...")

            evaluation = self.evaluate_answer(
                question=pair.get("question", ""),
                answer=pair.get("answer", ""),
                role=role,
                question_type=pair.get("question_type", "general")
            )

            results.append({
                **pair,
                "evaluation": evaluation
            })

        return results

    def get_score_interpretation(self, score: int) -> str:
        """Get human-readable interpretation of score."""
        if score >= 9:
            return "Excellent - Hire immediately!"
        elif score >= 7:
            return "Strong - Good candidate"
        elif score >= 5:
            return "Acceptable - Needs some improvement"
        elif score >= 3:
            return "Weak - Significant gaps"
        else:
            return "Poor - Not ready"


def test_evaluator():
    """Test the evaluator with sample question/answer."""
    evaluator = GeminiEvaluator()

    question = "What is the difference between bias and variance in machine learning?"
    answer = """
    Bias is the error from overly simplistic assumptions in the model,
    leading to underfitting. Variance is the error from too much complexity,
    causing the model to overfit training data. The bias-variance tradeoff
    is about finding the right model complexity.
    """

    result = evaluator.evaluate_answer(
        question=question,
        answer=answer,
        role="Machine Learning Engineer",
        question_type="ml"
    )

    print("\n" + "="*80)
    print("EVALUATION RESULT")
    print("="*80)
    print(f"\nScore: {result['score']}/10")
    print(f"Interpretation: {evaluator.get_score_interpretation(result['score'])}")
    print(f"\nStrengths:")
    for strength in result.get('strengths', []):
        print(f"  ✅ {strength}")
    print(f"\nImprovements:")
    for improvement in result.get('improvements', []):
        print(f"  💡 {improvement}")
    print(f"\nFinal Comment:")
    print(f"  {result.get('final_comment', 'N/A')}")
    print("\n" + "="*80)


if __name__ == "__main__":
    # Test the evaluator
    test_evaluator()
