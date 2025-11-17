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

            # Extract metadata fields (company, difficulty, type) - these apply to ALL questions in the section
            company_match = re.search(r'\*\*Company\*\*:\s*(.+)', section)
            difficulty_match = re.search(r'\*\*Difficulty\*\*:\s*(.+)', section)
            type_match = re.search(r'\*\*Type\*\*:\s*(.+)', section)

            # Extract company from header if not in field format (e.g., "## Amazon - Data Scientist")
            if not company_match:
                header_match = re.search(r'^##\s*([^-\n]+)', section)
                if header_match:
                    company_match = header_match

            # Method 1: Check for **Question Title:** format (StrataScratch style)
            title_match = re.search(r'\*\*Question Title:\*\*\s*(.+?)(?=\*\*|$)', section, re.DOTALL)
            details_match = re.search(r'\*\*Question Details:\*\*\s*(.+)', section, re.DOTALL)

            if title_match:
                # StrataScratch format - one question per section
                question_text = title_match.group(1).strip()
                if details_match:
                    details = details_match.group(1).strip()
                    if details and details not in question_text:
                        question_text += "\n" + details

                # Clean up question text
                question_text = re.sub(r'\n+', ' ', question_text)
                question_text = re.sub(r'\s+', ' ', question_text).strip()

                if len(question_text) >= 20:
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
            else:
                # Method 2: Find ALL **Question N:** in this section (LeetCode/Scenario style)
                question_matches = re.finditer(r'\*\*Question \d+:\*\*\s*(.+?)(?=\n\*\*Question \d+:|\n---|\Z)', section, re.DOTALL)

                for match in question_matches:
                    question_text = match.group(1).strip()

                    # Clean up question text
                    question_text = re.sub(r'\n+', ' ', question_text)
                    question_text = re.sub(r'\s+', ' ', question_text).strip()

                    if len(question_text) >= 20:
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
        'templates/leetcode_manual_template.txt',
        'templates/stratascratch_manual_template.txt',
        'templates/manual_scenario_questions.txt'
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

def save_to_csv(questions, filename='collected_questions/manual_questions.csv'):
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
