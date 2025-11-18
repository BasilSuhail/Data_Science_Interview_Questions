"""
SCRIPT: 120 Data Science Interview Questions Parser

What it does:
- Parses the kojino/120-Data-Science-Interview-Questions repository
- Extracts questions from 7 markdown files
- Format: #### N. Question text
- Outputs: 120questions.csv

Categories:
1. communication.md
2. data-analysis.md
3. predictive-modeling.md
4. probability.md
5. product-metrics.md
6. programming.md
7. statistical-inference.md
"""

import csv
import re
import os
from datetime import datetime

def parse_markdown_file(filepath, category):
    """Parse a single markdown file and extract questions."""
    questions = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split by #### markers (question headers)
        # Pattern: #### N. Question text
        question_pattern = r'####\s+(\d+)\.\s+(.+?)(?=\n####|\Z)'
        matches = re.finditer(question_pattern, content, re.DOTALL)

        for match in matches:
            question_num = match.group(1)
            question_block = match.group(2).strip()

            # Split question from answer
            # The question is usually the first line, answer follows after newline or bullet
            lines = question_block.split('\n', 1)
            question_text = lines[0].strip()

            # Get answer if it exists (everything after first line)
            answer_text = ''
            if len(lines) > 1:
                answer_text = lines[1].strip()
                # Clean up answer - remove excessive whitespace
                answer_text = re.sub(r'\n\s*\n', '\n', answer_text)
                answer_text = answer_text[:500]  # First 500 chars

            # Clean up question text
            question_text = re.sub(r'\s+', ' ', question_text).strip()

            # Skip if question is too short
            if len(question_text) < 10:
                continue

            # Determine difficulty based on answer length and category
            difficulty = 'medium'
            if category in ['probability', 'statistical-inference']:
                difficulty = 'hard'
            elif category in ['communication', 'programming']:
                difficulty = 'medium'
            elif len(answer_text) > 300:
                difficulty = 'hard'

            # Determine question type
            question_type = 'mixed'
            if category == 'probability':
                question_type = 'stats'
            elif category == 'statistical-inference':
                question_type = 'stats'
            elif category == 'predictive-modeling':
                question_type = 'ml'
            elif category == 'programming':
                question_type = 'coding'
            elif category == 'data-analysis':
                question_type = 'case'
            elif category == 'product-metrics':
                question_type = 'case'
            elif category == 'communication':
                question_type = 'behavioral'

            questions.append({
                'question_text': question_text,
                'company': '',
                'difficulty': difficulty,
                'question_type': question_type,
                'topics': category.replace('-', '_'),
                'source': 'kojino/120-DS-Questions',
                'answer_text': answer_text,
                'created_at': datetime.now().isoformat()
            })

        return questions

    except FileNotFoundError:
        print(f"⚠️  File not found: {filepath}")
        return []
    except Exception as e:
        print(f"⚠️  Error parsing {filepath}: {str(e)}")
        return []

def parse_all_files():
    """Parse all markdown files from the 120 Questions repo."""
    all_questions = []

    files = [
        ('temp_120questions/communication.md', 'communication'),
        ('temp_120questions/data-analysis.md', 'data-analysis'),
        ('temp_120questions/predictive-modeling.md', 'predictive-modeling'),
        ('temp_120questions/probability.md', 'probability'),
        ('temp_120questions/product-metrics.md', 'product-metrics'),
        ('temp_120questions/programming.md', 'programming'),
        ('temp_120questions/statistical-inference.md', 'statistical-inference')
    ]

    print("\n" + "="*80)
    print("  📚 120 Data Science Interview Questions Parser")
    print("="*80 + "\n")

    for filepath, category in files:
        if not os.path.exists(filepath):
            print(f"⚠️  File not found: {filepath}")
            continue

        questions = parse_markdown_file(filepath, category)
        all_questions.extend(questions)
        print(f"✅ {category:25} {len(questions):3} questions")

    return all_questions

def save_to_csv(questions, filename='collected_questions/120questions.csv'):
    """Save questions to CSV."""
    if not questions:
        print("\n❌ No questions to save!")
        return

    fieldnames = ['question_text', 'company', 'difficulty', 'question_type',
                  'topics', 'source', 'answer_text', 'created_at']

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(questions)

    print(f"\n✅ Saved {len(questions)} questions to '{filename}'")

if __name__ == "__main__":
    # Parse all files
    questions = parse_all_files()

    if questions:
        print(f"\n📊 Total questions extracted: {len(questions)}")

        # Show breakdown by type
        type_counts = {}
        for q in questions:
            qtype = q['question_type']
            type_counts[qtype] = type_counts.get(qtype, 0) + 1

        print("\nBreakdown by type:")
        for qtype, count in sorted(type_counts.items()):
            print(f"  - {qtype}: {count}")

        # Show breakdown by category
        category_counts = {}
        for q in questions:
            cat = q['topics']
            category_counts[cat] = category_counts.get(cat, 0) + 1

        print("\nBreakdown by category:")
        for cat, count in sorted(category_counts.items()):
            print(f"  - {cat}: {count}")

        # Save to CSV
        save_to_csv(questions)

    print("\n" + "="*80)
    print("✅ Parsing complete!")
    print("="*80 + "\n")
