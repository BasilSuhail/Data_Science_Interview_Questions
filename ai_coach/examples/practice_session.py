"""
Example 2: Practice Session with Multiple Questions

This script demonstrates:
1. Practice session with 3 questions
2. Different question types
3. Session summary with average score
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from interview_coach import InterviewCoach


def main():
    print("\n" + "="*80)
    print("🚀 AI INTERVIEW COACH - Practice Session Example")
    print("="*80 + "\n")

    # Initialize
    coach = InterviewCoach()

    # Run practice session
    print("Starting practice session with 3 ML questions...\n")

    results = coach.practice_session(
        num_questions=3,
        question_type="ml",
        difficulty="medium",
        role="Machine Learning Engineer"
    )

    # Additional analysis
    print("\n" + "="*80)
    print("📈 DETAILED ANALYSIS")
    print("="*80 + "\n")

    scores = [r["evaluation"]["score"] for r in results if "evaluation" in r]

    if scores:
        print(f"Highest Score: {max(scores)}/10")
        print(f"Lowest Score: {min(scores)}/10")
        print(f"Average Score: {sum(scores)/len(scores):.1f}/10")

        # Identify weak areas
        all_improvements = []
        for r in results:
            if "evaluation" in r:
                all_improvements.extend(r["evaluation"].get("improvements", []))

        print(f"\n🎯 Focus Areas ({len(all_improvements)} total suggestions):")
        for i, imp in enumerate(set(all_improvements[:5]), 1):
            print(f"   {i}. {imp}")
    else:
        print("❌ No results to analyze")


if __name__ == "__main__":
    main()
