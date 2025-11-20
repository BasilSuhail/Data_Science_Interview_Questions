"""
Upload coding questions to Supabase
"""

import csv
import os
from supabase import create_client, Client

# Supabase credentials (from config.js)
SUPABASE_URL = "https://iteavenjozhzxupbxosu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml0ZWF2ZW5qb3poenh1cGJ4b3N1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMwMjk4NTgsImV4cCI6MjA3ODYwNTg1OH0.AfBGdanvvHUoFOWYF94PN0ccLlWPVJFHN1At-kjzpkE"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_coding_questions():
    """Upload coding questions from CSV to Supabase"""

    csv_file = 'collected_questions/source_files/coding_questions.csv'

    if not os.path.exists(csv_file):
        print(f"❌ Error: {csv_file} not found!")
        return

    print(f"📂 Reading coding questions from {csv_file}...")

    coding_questions = []

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            coding_questions.append({
                'question': row['question'].strip(),
                'difficulty': row['difficulty'].strip(),
                'category': row['category'].strip(),
                'tags': row['tags'].strip(),
                'constraints': row['constraints'].strip() if row['constraints'] else None,
                'examples': row['examples'].strip() if row['examples'] else None,
                'hints': row['hints'].strip() if row['hints'] else None,
                'source': row['source'].strip()
            })

    print(f"✅ Parsed {len(coding_questions)} coding questions")

    # Upload to Supabase
    print(f"\n🚀 Uploading to Supabase...")

    try:
        # Insert questions
        response = supabase.table('interview_questions').insert(coding_questions).execute()

        print(f"✅ Successfully uploaded {len(coding_questions)} coding questions!")
        print(f"   - Easy: {sum(1 for q in coding_questions if q['difficulty'] == 'Easy')}")
        print(f"   - Medium: {sum(1 for q in coding_questions if q['difficulty'] == 'Medium')}")
        print(f"   - Advanced: {sum(1 for q in coding_questions if q['difficulty'] == 'Advanced')}")

    except Exception as e:
        print(f"❌ Error uploading to Supabase: {str(e)}")
        print(f"   This might be because:")
        print(f"   1. Questions already exist (duplicate constraint)")
        print(f"   2. Table schema doesn't support new fields (constraints, examples, hints)")
        print(f"   3. Network issue")
        print(f"\n💡 Suggested action:")
        print(f"   - Check Supabase table schema")
        print(f"   - Add columns: constraints (text), examples (text), hints (text)")

if __name__ == "__main__":
    upload_coding_questions()
