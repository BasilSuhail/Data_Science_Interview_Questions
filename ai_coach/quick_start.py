#!/usr/bin/env python3
"""
AI Interview Coach - Quick Start Script

This is the fastest way to get started!
Just run: python quick_start.py

It will:
1. Check if you have API keys set
2. Guide you through setup if needed
3. Start an interview session
"""

import os
import sys


def check_environment():
    """Check if environment variables are set."""
    print("\n" + "="*80)
    print("🔍 Checking Environment Setup")
    print("="*80 + "\n")

    missing = []

    # Check Supabase
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")

    if not supabase_url:
        missing.append("SUPABASE_URL")
        print("❌ SUPABASE_URL not set")
    else:
        print(f"✅ SUPABASE_URL: {supabase_url[:30]}...")

    if not supabase_key:
        missing.append("SUPABASE_KEY")
        print("❌ SUPABASE_KEY not set")
    else:
        print(f"✅ SUPABASE_KEY: {supabase_key[:20]}...")

    if not gemini_key:
        missing.append("GEMINI_API_KEY")
        print("❌ GEMINI_API_KEY not set")
    else:
        print(f"✅ GEMINI_API_KEY: {gemini_key[:20]}...")

    return missing


def show_setup_instructions(missing):
    """Show setup instructions for missing variables."""
    print("\n" + "="*80)
    print("⚠️  Missing Environment Variables")
    print("="*80 + "\n")

    print("You need to set these environment variables:\n")

    for var in missing:
        print(f"  - {var}")

    print("\n" + "="*80)
    print("📝 Setup Instructions")
    print("="*80 + "\n")

    print("Option 1: Create .env file (Recommended)")
    print("-" * 80)
    print("1. Copy .env.example to .env:")
    print("   cp .env.example .env\n")
    print("2. Edit .env and add your credentials\n")
    print("3. Run this script again\n")

    print("Option 2: Export variables")
    print("-" * 80)
    print('export SUPABASE_URL="https://iteavenjozhzxupbxosu.supabase.co"')
    print('export SUPABASE_KEY="your-supabase-key"')
    print('export GEMINI_API_KEY="your-gemini-key"\n')

    print("=" * 80)
    print("📚 Where to get API keys:")
    print("=" * 80)
    print("Gemini API (free): https://aistudio.google.com/app/apikey")
    print("Supabase: You already have this from your project setup\n")

    print("For detailed instructions, see: SETUP.md\n")


def run_interview():
    """Run a sample interview."""
    print("\n" + "="*80)
    print("🚀 Starting AI Interview Coach")
    print("="*80 + "\n")

    try:
        from interview_coach import InterviewCoach

        # Initialize
        coach = InterviewCoach()

        print("\n" + "="*80)
        print("🎯 Choose Interview Type")
        print("="*80 + "\n")

        print("Question Types:")
        print("  1. ML (Machine Learning) - 264 questions")
        print("  2. Stats (Statistics) - 61 questions")
        print("  3. SQL (Databases) - 22 questions")
        print("  4. Coding (Algorithms) - 28 questions")
        print("  5. Case (Case Studies) - 61 questions")
        print("  6. Mixed (Various) - 109 questions\n")

        type_map = {
            "1": "ml", "2": "stats", "3": "sql",
            "4": "coding", "5": "case", "6": "mixed"
        }

        choice = input("Enter number (1-6) or press Enter for ML: ").strip()
        question_type = type_map.get(choice, "ml")

        print("\nDifficulty:")
        print("  1. Easy")
        print("  2. Medium")
        print("  3. Hard\n")

        diff_map = {"1": "easy", "2": "medium", "3": "hard"}
        diff_choice = input("Enter number (1-3) or press Enter for Medium: ").strip()
        difficulty = diff_map.get(diff_choice, "medium")

        # Conduct interview
        result = coach.conduct_interview(
            question_type=question_type,
            difficulty=difficulty,
            role="Data Scientist"
        )

        # Show completion message
        if "error" not in result:
            print("\n" + "="*80)
            print("✅ Interview Complete!")
            print("="*80 + "\n")
            print("💡 Tips for next time:")
            print("   - Try different question types")
            print("   - Practice with harder questions")
            print("   - Review the improvement suggestions\n")
            print("Run 'python examples/practice_session.py' for multiple questions!\n")
        else:
            print(f"\n❌ Error: {result['error']}\n")

    except ImportError as e:
        print(f"❌ Import Error: {str(e)}\n")
        print("Make sure you've installed dependencies:")
        print("  pip install -r requirements.txt\n")
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
        print("See SETUP.md for troubleshooting help.\n")


def main():
    """Main entry point."""
    print("\n" + "="*80)
    print("🤖 AI INTERVIEW COACH - Quick Start")
    print("="*80)

    # Load .env if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    # Check environment
    missing = check_environment()

    if missing:
        show_setup_instructions(missing)
        sys.exit(1)

    # Run interview
    run_interview()


if __name__ == "__main__":
    main()
