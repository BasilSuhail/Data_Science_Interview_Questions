"""
Example 1: Basic Usage of AI Interview Coach

This script shows the simplest way to use the Interview Coach:
1. Initialize the coach
2. Conduct a single interview
3. Get evaluation feedback
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from interview_coach import InterviewCoach


def main():
    print("\n" + "="*80)
    print("🎯 AI INTERVIEW COACH - Basic Usage Example")
    print("="*80 + "\n")

    # Initialize the coach
    print("Initializing AI Interview Coach...\n")
    coach = InterviewCoach()

    # Conduct a single interview
    print("Starting interview session...\n")

    result = coach.conduct_interview(
        question_type="ml",           # Machine Learning question
        difficulty="medium",          # Medium difficulty
        role="Data Scientist"         # Role for evaluation context
    )

    # Check if interview completed successfully
    if "error" not in result:
        print("\n✅ Interview session completed successfully!")
        print(f"\nYour score: {result['evaluation']['score']}/10")
    else:
        print(f"\n❌ Interview session failed: {result['error']}")


if __name__ == "__main__":
    main()
