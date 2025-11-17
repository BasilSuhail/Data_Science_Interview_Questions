"""
SCRIPT 5: Question Merger & Deduplicator

What it does:
- Combines all question sources (GitHub, LeetCode, StrataScratch, manual)
- Removes duplicates (fuzzy matching)
- Standardizes format
- Outputs: final_interview_questions.csv

Run this AFTER you've collected from all sources!
"""

import csv
import os
from datetime import datetime
from difflib import SequenceMatcher

def load_csv_questions(filename):
    """Load questions from a CSV file."""
    questions = []

    if not os.path.exists(filename):
        print(f"  ⚠️  File not found: {filename}")
        return questions

    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                questions.append(row)

        print(f"  ✅ Loaded {len(questions)} questions from {filename}")
    except Exception as e:
        print(f"  ❌ Error loading {filename}: {str(e)}")

    return questions

def similarity_ratio(str1, str2):
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def remove_duplicates(questions, similarity_threshold=0.85):
    """Remove duplicate questions using fuzzy matching."""
    unique_questions = []
    duplicates_count = 0

    print(f"\n🔍 Checking for duplicates (threshold: {similarity_threshold})...")

    for i, question in enumerate(questions):
        is_duplicate = False

        # Check against all unique questions so far
        for unique_q in unique_questions:
            similarity = similarity_ratio(
                question['question_text'],
                unique_q['question_text']
            )

            if similarity >= similarity_threshold:
                is_duplicate = True
                duplicates_count += 1
                break

        if not is_duplicate:
            unique_questions.append(question)

        if (i + 1) % 100 == 0:
            print(f"  Processed {i + 1}/{len(questions)} questions...")

    print(f"\n  ✅ Removed {duplicates_count} duplicates")
    print(f"  ✅ {len(unique_questions)} unique questions remaining")

    return unique_questions

def merge_all_questions():
    """Main function to merge all question sources."""
    all_questions = []

    print("\n" + "="*80)
    print("  🔗 Interview Questions Merger & Deduplicator")
    print("="*80 + "\n")

    # Load from all sources
    print("📂 Loading questions from all sources:\n")

    sources = [
        'github_questions.csv',
        'leetcode_questions.csv',
        'stratascratch_questions.csv',
        'manual_questions.csv'
    ]

    for source in sources:
        questions = load_csv_questions(source)
        all_questions.extend(questions)

    if not all_questions:
        print("\n❌ No questions found!")
        print("   Make sure you've run the collection scripts first:")
        print("   1. python collect_github_questions.py")
        print("   2. python scrape_leetcode_discuss.py")
        print("   3. python scrape_stratascratch.py")
        print("   4. python parse_manual_questions.py")
        return []

    print(f"\n📊 Total questions before deduplication: {len(all_questions)}")

    # Remove duplicates
    unique_questions = remove_duplicates(all_questions)

    # Add statistics
    print(f"\n📊 Final Statistics:")
    print(f"   - Total unique questions: {len(unique_questions)}")

    # Count by source
    source_counts = {}
    for q in unique_questions:
        source = q.get('source', 'unknown')
        source_counts[source] = source_counts.get(source, 0) + 1

    print(f"\n   By source:")
    for source, count in sorted(source_counts.items()):
        print(f"     - {source}: {count}")

    # Count by type
    type_counts = {}
    for q in unique_questions:
        qtype = q.get('question_type', 'unknown')
        type_counts[qtype] = type_counts.get(qtype, 0) + 1

    print(f"\n   By type:")
    for qtype, count in sorted(type_counts.items()):
        print(f"     - {qtype}: {count}")

    # Count by difficulty
    difficulty_counts = {}
    for q in unique_questions:
        difficulty = q.get('difficulty', 'medium')
        difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1

    print(f"\n   By difficulty:")
    for difficulty, count in sorted(difficulty_counts.items()):
        print(f"     - {difficulty}: {count}")

    # Count with company tags
    with_company = sum(1 for q in unique_questions if q.get('company'))
    print(f"\n   - With company tags: {with_company}")

    return unique_questions

def save_to_csv(questions, filename='final_interview_questions.csv'):
    """Save merged questions to CSV."""
    if not questions:
        print("\n❌ No questions to save!")
        return

    fieldnames = ['question_text', 'company', 'difficulty', 'question_type',
                  'topics', 'source', 'answer_text', 'created_at']

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(questions)

    print(f"\n✅ Saved {len(questions)} unique questions to '{filename}'")
    print(f"\n📤 Next step: Upload '{filename}' to Supabase!")

if __name__ == "__main__":
    questions = merge_all_questions()
    save_to_csv(questions)

    print("\n" + "="*80)
    print("✅ Merge complete!")
    print("="*80 + "\n")
