#!/usr/bin/env python3
"""
Merge existing questions with scraped questions
Removes duplicates and creates final upload CSV
"""

import csv
from datetime import datetime

def load_csv(filepath):
    """Load CSV and return list of dicts"""
    questions = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            questions.append(row)
    return questions

def normalize_question(text):
    """Normalize question text for duplicate detection"""
    # Remove extra whitespace, lowercase, remove punctuation
    return ''.join(c.lower() for c in text if c.isalnum() or c.isspace()).strip()

def merge_questions(existing_file, scraped_file, output_file):
    """Merge two question CSVs, removing duplicates"""

    print("📂 Loading existing questions...")
    existing = load_csv(existing_file)
    print(f"  ✅ Loaded {len(existing)} existing questions")

    print("📂 Loading scraped questions...")
    scraped = load_csv(scraped_file)
    print(f"  ✅ Loaded {len(scraped)} scraped questions")

    # Track unique questions by normalized text
    seen_questions = set()
    merged = []

    # Add existing questions first (priority)
    for q in existing:
        normalized = normalize_question(q['question_text'])
        if normalized and normalized not in seen_questions:
            seen_questions.add(normalized)
            merged.append(q)

    print(f"  ✅ Added {len(merged)} existing questions")

    # Add scraped questions (skip duplicates)
    scraped_added = 0
    for q in scraped:
        normalized = normalize_question(q['question_text'])
        if normalized and normalized not in seen_questions and len(normalized) > 20:
            seen_questions.add(normalized)
            merged.append(q)
            scraped_added += 1

    print(f"  ✅ Added {scraped_added} new scraped questions")
    print(f"  ⚠️  Skipped {len(scraped) - scraped_added} duplicate questions")

    # Save merged questions
    print(f"\n💾 Saving {len(merged)} total questions to {output_file}...")

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['question_text', 'company', 'difficulty', 'question_type',
                     'topics', 'source', 'answer_text', 'created_at']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(merged)

    print(f"✅ Saved successfully!")

    # Print stats
    print(f"\n📊 Final Stats:")
    print(f"  Total questions: {len(merged)}")

    by_type = {}
    by_difficulty = {}
    by_company = {}

    for q in merged:
        # By type
        qtype = q.get('question_type', 'unknown')
        by_type[qtype] = by_type.get(qtype, 0) + 1

        # By difficulty
        diff = q.get('difficulty', 'unknown')
        by_difficulty[diff] = by_difficulty.get(diff, 0) + 1

        # By company (only if not empty)
        company = q.get('company', '').strip()
        if company:
            by_company[company] = by_company.get(company, 0) + 1

    print(f"\n  By Question Type:")
    for qtype, count in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"    {qtype}: {count}")

    print(f"\n  By Difficulty:")
    for diff, count in sorted(by_difficulty.items(), key=lambda x: -x[1]):
        print(f"    {diff}: {count}")

    print(f"\n  By Company (top 10):")
    for company, count in sorted(by_company.items(), key=lambda x: -x[1])[:10]:
        print(f"    {company}: {count}")

    print(f"\n✅ Ready to upload to Supabase!")
    print(f"📁 File: {output_file}")

if __name__ == "__main__":
    merge_questions(
        existing_file="collected_questions/final_interview_questions.csv",
        scraped_file="scraped_questions.csv",
        output_file="UPLOAD_TO_SUPABASE.csv"
    )
