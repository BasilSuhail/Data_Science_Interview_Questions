"""
AI Interview Coach - Main Integration Module

Combines:
1. Your Supabase database (552 questions + 3,983 textbook pages)
2. Gemini evaluation (answer scoring + feedback)
3. Optional: RAG for textbook-based explanations

Complete interview coaching workflow:
- Select question from database
- User answers
- AI evaluates answer
- Provide feedback + explanations
"""

import os
import random
from typing import Dict, List, Optional
from supabase import create_client, Client

from gemini_evaluator import GeminiEvaluator


class InterviewCoach:
    """Complete AI Interview Coach using Supabase + Gemini."""

    def __init__(
        self,
        supabase_url: Optional[str] = None,
        supabase_key: Optional[str] = None,
        gemini_api_key: Optional[str] = None
    ):
        """
        Initialize Interview Coach.

        Args:
            supabase_url: Supabase project URL (or from env SUPABASE_URL)
            supabase_key: Supabase anon key (or from env SUPABASE_KEY)
            gemini_api_key: Gemini API key (or from env GEMINI_API_KEY)
        """
        # Initialize Supabase
        self.supabase_url = supabase_url or os.getenv("SUPABASE_URL")
        self.supabase_key = supabase_key or os.getenv("SUPABASE_KEY")

        if not self.supabase_url or not self.supabase_key:
            print("⚠️  Supabase credentials not found. Question database unavailable.")
            print("   Set SUPABASE_URL and SUPABASE_KEY environment variables.")
            self.supabase = None
        else:
            self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
            print("✅ Connected to Supabase database")

        # Initialize Gemini evaluator
        self.evaluator = GeminiEvaluator(api_key=gemini_api_key)
        print("✅ Gemini evaluator ready")

    def get_question(
        self,
        question_type: Optional[str] = None,
        difficulty: Optional[str] = None,
        company: Optional[str] = None,
        topics: Optional[str] = None,
        random_selection: bool = True
    ) -> Optional[Dict]:
        """
        Fetch a question from your Supabase database.

        Args:
            question_type: Filter by type (ml, stats, sql, coding, case, behavioral)
            difficulty: Filter by difficulty (easy, medium, hard)
            company: Filter by company
            topics: Filter by topics
            random_selection: If True, randomly select from matching questions

        Returns:
            Question dictionary or None
        """
        if not self.supabase:
            print("❌ Supabase not connected. Cannot fetch questions.")
            return None

        # Build query
        query = self.supabase.table("interview_questions").select("*")

        # Apply filters
        if question_type:
            query = query.eq("question_type", question_type)
        if difficulty:
            query = query.eq("difficulty", difficulty)
        if company:
            query = query.eq("company", company)
        if topics:
            query = query.eq("topics", topics)

        # Execute query
        try:
            response = query.execute()
            questions = response.data

            if not questions:
                print("❌ No questions found matching criteria.")
                return None

            # Select question
            if random_selection:
                question = random.choice(questions)
            else:
                question = questions[0]

            return question

        except Exception as e:
            print(f"❌ Error fetching question: {str(e)}")
            return None

    def conduct_interview(
        self,
        question_type: str = "ml",
        difficulty: str = "medium",
        role: str = "Data Scientist"
    ) -> Dict:
        """
        Complete interview session workflow.

        Args:
            question_type: Type of questions to ask
            difficulty: Question difficulty
            role: Job role for evaluation context

        Returns:
            Interview session results
        """
        print("\n" + "="*80)
        print(f"🎯 AI INTERVIEW COACH - {role}")
        print("="*80 + "\n")

        # Step 1: Get question from database
        print(f"📋 Fetching {difficulty} {question_type} question from database...")
        question_data = self.get_question(
            question_type=question_type,
            difficulty=difficulty
        )

        if not question_data:
            return {"error": "Could not fetch question"}

        question = question_data.get("question_text", "")
        print(f"\n❓ QUESTION:\n{question}\n")

        # Step 2: Get user's answer
        print("💭 Your answer:")
        print("   (Type your answer, then press Enter twice to submit)\n")

        lines = []
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)

        user_answer = "\n".join(lines).strip()

        if not user_answer:
            print("\n❌ No answer provided. Exiting.")
            return {"error": "No answer provided"}

        # Step 3: Evaluate answer with Gemini
        print("\n🤖 Evaluating your answer with Gemini AI...\n")

        evaluation = self.evaluator.evaluate_answer(
            question=question,
            answer=user_answer,
            role=role,
            question_type=question_type
        )

        # Step 4: Display results
        self._display_evaluation(evaluation)

        # Step 5: Show model answer if available
        if question_data.get("answer_text"):
            print("\n" + "="*80)
            print("📚 MODEL ANSWER (from database):")
            print("="*80)
            print(f"\n{question_data['answer_text']}\n")

        # Return session data
        return {
            "question": question,
            "user_answer": user_answer,
            "evaluation": evaluation,
            "question_data": question_data
        }

    def _display_evaluation(self, evaluation: Dict):
        """Display evaluation results in a nice format."""
        print("="*80)
        print("📊 EVALUATION RESULTS")
        print("="*80 + "\n")

        score = evaluation.get("score", 0)
        interpretation = self.evaluator.get_score_interpretation(score)

        print(f"🎯 Score: {score}/10")
        print(f"   {interpretation}\n")

        print("✅ STRENGTHS:")
        for i, strength in enumerate(evaluation.get("strengths", []), 1):
            print(f"   {i}. {strength}")

        print("\n💡 AREAS FOR IMPROVEMENT:")
        for i, improvement in enumerate(evaluation.get("improvements", []), 1):
            print(f"   {i}. {improvement}")

        print(f"\n💬 FINAL COMMENT:")
        print(f"   {evaluation.get('final_comment', 'N/A')}\n")

        print("="*80)

    def practice_session(
        self,
        num_questions: int = 5,
        question_type: str = "ml",
        difficulty: str = "medium",
        role: str = "Data Scientist"
    ) -> List[Dict]:
        """
        Practice session with multiple questions.

        Args:
            num_questions: Number of questions to practice
            question_type: Type of questions
            difficulty: Question difficulty
            role: Job role

        Returns:
            List of session results
        """
        print("\n" + "="*80)
        print(f"🚀 PRACTICE SESSION - {num_questions} Questions")
        print("="*80 + "\n")

        results = []

        for i in range(num_questions):
            print(f"\n{'='*80}")
            print(f"QUESTION {i+1}/{num_questions}")
            print(f"{'='*80}\n")

            session = self.conduct_interview(
                question_type=question_type,
                difficulty=difficulty,
                role=role
            )

            results.append(session)

            if i < num_questions - 1:
                input("\nPress Enter for next question...")

        # Show summary
        self._show_session_summary(results)

        return results

    def _show_session_summary(self, results: List[Dict]):
        """Display summary of practice session."""
        print("\n" + "="*80)
        print("📈 SESSION SUMMARY")
        print("="*80 + "\n")

        scores = [r.get("evaluation", {}).get("score", 0) for r in results]
        avg_score = sum(scores) / len(scores) if scores else 0

        print(f"Total Questions: {len(results)}")
        print(f"Average Score: {avg_score:.1f}/10")
        print(f"Interpretation: {self.evaluator.get_score_interpretation(int(avg_score))}\n")

        print("Individual Scores:")
        for i, score in enumerate(scores, 1):
            print(f"  Question {i}: {score}/10")

        print("\n" + "="*80)


def main():
    """Example usage of Interview Coach."""
    # Initialize coach
    coach = InterviewCoach()

    # Example 1: Single question interview
    print("\n🎯 Example 1: Single Question Interview\n")

    result = coach.conduct_interview(
        question_type="ml",
        difficulty="medium",
        role="Machine Learning Engineer"
    )

    # Example 2: Practice session (commented out - uncomment to use)
    # print("\n🎯 Example 2: Practice Session (5 questions)\n")
    # coach.practice_session(
    #     num_questions=5,
    #     question_type="stats",
    #     difficulty="medium",
    #     role="Data Scientist"
    # )


if __name__ == "__main__":
    main()
