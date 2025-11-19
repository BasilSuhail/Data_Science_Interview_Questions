"""
Example 3: Batch Evaluation of Pre-written Answers

This script shows:
1. How to evaluate multiple answers at once
2. Useful for testing your prepared answers
3. Comparing answer quality across topics
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gemini_evaluator import GeminiEvaluator


def main():
    print("\n" + "="*80)
    print("📝 AI INTERVIEW COACH - Batch Evaluation Example")
    print("="*80 + "\n")

    # Initialize evaluator
    evaluator = GeminiEvaluator()

    # Prepare Q&A pairs (these are your prepared answers)
    qa_pairs = [
        {
            "question": "What is the bias-variance tradeoff?",
            "answer": """
                Bias is the error from overly simplistic assumptions, leading to
                underfitting. Variance is the error from too much complexity,
                causing overfitting. We need to balance both for optimal model
                performance.
            """,
            "question_type": "ml"
        },
        {
            "question": "Explain the Central Limit Theorem.",
            "answer": """
                The CLT states that when you take sufficiently large samples from
                any population, the distribution of sample means will approximate
                a normal distribution, regardless of the population's original
                distribution.
            """,
            "question_type": "stats"
        },
        {
            "question": "What is the difference between INNER JOIN and LEFT JOIN?",
            "answer": """
                INNER JOIN returns only matching rows from both tables.
                LEFT JOIN returns all rows from the left table and matching
                rows from the right table, with NULLs for non-matches.
            """,
            "question_type": "sql"
        }
    ]

    print(f"Evaluating {len(qa_pairs)} pre-written answers...\n")

    # Batch evaluate
    results = evaluator.batch_evaluate(qa_pairs, role="Data Scientist")

    # Display results
    print("\n" + "="*80)
    print("📊 BATCH EVALUATION RESULTS")
    print("="*80 + "\n")

    for i, result in enumerate(results, 1):
        eval_data = result["evaluation"]
        print(f"\nQuestion {i}: {result['question'][:50]}...")
        print(f"Score: {eval_data['score']}/10")
        print(f"Comment: {eval_data.get('final_comment', 'N/A')}")
        print("-" * 80)

    # Summary
    scores = [r["evaluation"]["score"] for r in results]
    avg_score = sum(scores) / len(scores)

    print(f"\n📈 SUMMARY:")
    print(f"   Total Answers: {len(results)}")
    print(f"   Average Score: {avg_score:.1f}/10")
    print(f"   Best Score: {max(scores)}/10")
    print(f"   Needs Work: {min(scores)}/10")

    print("\n✅ Batch evaluation complete!")


if __name__ == "__main__":
    main()
