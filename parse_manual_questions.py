"""
SCRIPT 4: Manual Question Parser

What it does:
- Parses the manual templates you filled out
- Converts to standardized CSV format
- Outputs: manual_questions.csv
"""

import csv
import re
from datetime import datetime

def parse_template_file(filename):
    """Parse a manual template file."""
    questions = []

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split by the separator (---)
        sections = re.split(r'\n---+\n', content)

        for section in sections:
            # Skip header sections and empty sections
            if len(section.strip()) < 50:
                continue

            # Extract fields using regex
            company_match = re.search(r'\*\*Company\*\*:\s*(.+)', section)
            difficulty_match = re.search(r'\*\*Difficulty\*\*:\s*(.+)', section)
            type_match = re.search(r'\*\*Type\*\*:\s*(.+)', section)
            title_match = re.search(r'\*\*Question Title:\*\*\s*(.+?)(?=\*\*|$)', section, re.DOTALL)
            details_match = re.search(r'\*\*Question Details:\*\*\s*(.+)', section, re.DOTALL)

            # For LeetCode template (slightly different format)
            if not title_match:
                question_match = re.search(r'\*\*Question \d+:\*\*\s*(.+?)(?=\*\*Question \d+:|$)', section, re.DOTALL)
                if question_match:
                    title_match = question_match

            if title_match:
                question_text = title_match.group(1).strip()

                # Add details if available
                if details_match:
                    details = details_match.group(1).strip()
                    if details and details not in question_text:
                        question_text += "\n" + details

                # Clean up question text
                question_text = re.sub(r'\n+', ' ', question_text)
                question_text = re.sub(r'\s+', ' ', question_text).strip()

                if len(question_text) < 20:
                    continue

                questions.append({
                    'question_text': question_text,
                    'company': company_match.group(1).strip() if company_match else '',
                    'difficulty': difficulty_match.group(1).strip().lower() if difficulty_match else 'medium',
                    'question_type': type_match.group(1).strip().lower() if type_match else 'mixed',
                    'topics': '',
                    'source': f'manual_{filename}',
                    'answer_text': '',
                    'created_at': datetime.now().isoformat()
                })

    except FileNotFoundError:
        print(f"⚠️  File not found: {filename}")
        return []
    except Exception as e:
        print(f"⚠️  Error parsing {filename}: {str(e)}")
        return []

    return questions

def parse_all_templates():
    """Parse all manual template files."""
    all_questions = []

    print("\n" + "="*80)
    print("  📝 Manual Question Template Parser")
    print("="*80 + "\n")

    template_files = [
        'leetcode_manual_template.txt',
        'stratascratch_manual_template.txt'
    ]

    for filename in template_files:
        print(f"Parsing: {filename}")
        questions = parse_template_file(filename)

        if questions:
            print(f"  ✅ Found {len(questions)} questions")
            all_questions.extend(questions)
        else:
            print(f"  ⚠️  No questions found (template may be empty or incorrectly formatted)")

    return all_questions

def save_to_csv(questions, filename='manual_questions.csv'):
    """Save parsed questions to CSV."""
    if not questions:
        print("\n❌ No questions to save!")
        print("   Make sure you filled out the templates correctly")
        return

    fieldnames = ['question_text', 'company', 'difficulty', 'question_type',
                  'topics', 'source', 'answer_text', 'created_at']

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(questions)

    print(f"\n✅ Saved {len(questions)} questions to '{filename}'")

if __name__ == "__main__":
    questions = parse_all_templates()
    save_to_csv(questions)

    print("\n" + "="*80)
    print("✅ Manual parsing complete!")
    print("="*80 + "\n")
