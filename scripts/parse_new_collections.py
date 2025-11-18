"""
SCRIPT: Parse New Collection Files

What it does:
- Parses 3 new question files from collected_questions folder
- Extracts and cleans questions from different formats
- Outputs: new_collections_questions.csv

Files to parse:
1. 165_Machine_Learning_Interview_QuestionsAnswers.txt (165 ML questions)
2. SQL_INTERVIEW_QUESTIONSANSWERS.txt (24 SQL questions)
3. data-science-interview-questions-answers.ipynb (102 questions)
"""

import csv
import re
import json
from datetime import datetime

def parse_ml_questions_txt():
    """Parse 165 ML questions from text file."""
    questions = []

    try:
        with open('collected_questions/165_Machine_Learning_Interview_QuestionsAnswers.txt', 'r', encoding='utf-8') as f:
            content = f.read()

        # Pattern: N) Question text
        # Answer starts with =>
        pattern = r'(\d+)\)\s+(.+?)\n=>\s*(.+?)(?=\n\d+\)|$)'
        matches = re.finditer(pattern, content, re.DOTALL)

        for match in matches:
            num = match.group(1)
            question_text = match.group(2).strip()
            answer_text = match.group(3).strip()

            # Clean up question
            question_text = re.sub(r'\s+', ' ', question_text)

            # Clean up answer (first 500 chars)
            answer_text = re.sub(r'\s+', ' ', answer_text)
            answer_text = answer_text[:500]

            if len(question_text) < 10:
                continue

            # Determine difficulty based on answer length
            difficulty = 'medium'
            if len(answer_text) > 300:
                difficulty = 'hard'
            elif len(answer_text) < 150:
                difficulty = 'easy'

            questions.append({
                'question_text': question_text,
                'company': '',
                'difficulty': difficulty,
                'question_type': 'ml',
                'topics': 'machine_learning',
                'source': '165_ML_Interview_QA',
                'answer_text': answer_text,
                'created_at': datetime.now().isoformat()
            })

        print(f"✅ Parsed {len(questions)} ML questions")
        return questions

    except Exception as e:
        print(f"⚠️  Error parsing ML questions: {str(e)}")
        return []

def parse_sql_questions_txt():
    """Parse SQL questions from text file."""
    questions = []

    try:
        with open('collected_questions/SQL_INTERVIEW_QUESTIONSANSWERS.txt', 'r', encoding='utf-8') as f:
            content = f.read()

        # Pattern: N. Question text
        # Answer follows on next lines
        pattern = r'(\d+)\.\s+(.+?)(?=\n\d+\.|\Z)'
        matches = re.finditer(pattern, content, re.DOTALL)

        for match in matches:
            num = match.group(1)
            block = match.group(2).strip()

            # Split into question and answer
            lines = block.split('\n', 1)
            question_text = lines[0].strip()
            answer_text = lines[1].strip() if len(lines) > 1 else ''

            # Clean up
            question_text = re.sub(r'\s+', ' ', question_text)
            answer_text = re.sub(r'\s+', ' ', answer_text)
            answer_text = answer_text[:500]

            if len(question_text) < 10:
                continue

            # Determine difficulty
            difficulty = 'medium'
            if 'ACID' in question_text or 'transaction' in question_text.lower():
                difficulty = 'hard'
            elif 'What is' in question_text and len(answer_text) < 200:
                difficulty = 'easy'

            questions.append({
                'question_text': question_text,
                'company': '',
                'difficulty': difficulty,
                'question_type': 'sql',
                'topics': 'sql_database',
                'source': 'SQL_Interview_QA',
                'answer_text': answer_text,
                'created_at': datetime.now().isoformat()
            })

        print(f"✅ Parsed {len(questions)} SQL questions")
        return questions

    except Exception as e:
        print(f"⚠️  Error parsing SQL questions: {str(e)}")
        return []

def parse_jupyter_notebook():
    """Parse questions from Jupyter notebook."""
    questions = []

    try:
        with open('collected_questions/data-science-interview-questions-answers.ipynb', 'r', encoding='utf-8') as f:
            nb = json.load(f)

        for cell in nb['cells']:
            if cell['cell_type'] != 'markdown':
                continue

            content = ''.join(cell['source']).strip()

            # Skip if doesn't start with # (header)
            if not content.startswith('#'):
                continue

            # Skip the title cell
            if 'Important Tips' in content:
                continue

            # Extract question (first line after #)
            lines = content.split('\n')
            question_line = lines[0].replace('#', '').strip()

            # Extract answer (rest of the content)
            answer_lines = lines[1:] if len(lines) > 1 else []
            answer_text = '\n'.join(answer_lines).strip()

            # Clean up
            question_text = re.sub(r'\s+', ' ', question_line)
            answer_text = re.sub(r'\s+', ' ', answer_text)

            # Remove URLs from answer
            answer_text = re.sub(r'http[s]?://\S+', '', answer_text)
            answer_text = answer_text[:500]

            if len(question_text) < 10:
                continue

            # Determine question type
            question_type = 'mixed'
            q_lower = question_text.lower()
            if any(kw in q_lower for kw in ['regression', 'classification', 'model', 'algorithm', 'neural', 'learning']):
                question_type = 'ml'
            elif any(kw in q_lower for kw in ['probability', 'statistics', 'hypothesis', 'test', 'distribution']):
                question_type = 'stats'
            elif any(kw in q_lower for kw in ['code', 'implement', 'function', 'program']):
                question_type = 'coding'
            elif any(kw in q_lower for kw in ['analyze', 'data', 'dataset', 'business']):
                question_type = 'case'

            # Determine difficulty
            difficulty = 'medium'
            if len(answer_text) > 300 or 'complex' in answer_text.lower():
                difficulty = 'hard'
            elif len(answer_text) < 150:
                difficulty = 'easy'

            questions.append({
                'question_text': question_text,
                'company': '',
                'difficulty': difficulty,
                'question_type': question_type,
                'topics': 'data_science',
                'source': 'DS_Interview_Notebook',
                'answer_text': answer_text,
                'created_at': datetime.now().isoformat()
            })

        print(f"✅ Parsed {len(questions)} questions from notebook")
        return questions

    except Exception as e:
        print(f"⚠️  Error parsing notebook: {str(e)}")
        return []

def save_to_csv(questions, filename='collected_questions/new_collections_questions.csv'):
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
    print("\n" + "="*80)
    print("  📚 New Collections Parser")
    print("="*80 + "\n")

    all_questions = []

    # Parse each file
    print("Parsing files...\n")

    ml_questions = parse_ml_questions_txt()
    all_questions.extend(ml_questions)

    sql_questions = parse_sql_questions_txt()
    all_questions.extend(sql_questions)

    notebook_questions = parse_jupyter_notebook()
    all_questions.extend(notebook_questions)

    if all_questions:
        print(f"\n📊 Total questions extracted: {len(all_questions)}")

        # Show breakdown by type
        type_counts = {}
        for q in all_questions:
            qtype = q['question_type']
            type_counts[qtype] = type_counts.get(qtype, 0) + 1

        print("\nBreakdown by type:")
        for qtype, count in sorted(type_counts.items()):
            print(f"  - {qtype}: {count}")

        # Show breakdown by source
        source_counts = {}
        for q in all_questions:
            source = q['source']
            source_counts[source] = source_counts.get(source, 0) + 1

        print("\nBreakdown by source:")
        for source, count in sorted(source_counts.items()):
            print(f"  - {source}: {count}")

        # Save to CSV
        save_to_csv(all_questions)

    print("\n" + "="*80)
    print("✅ Parsing complete!")
    print("="*80 + "\n")
