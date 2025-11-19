"""
SCRIPT: Parse Sandy1811 Archive Files

What it does:
- Parses 3 files from archive/ folder (Sandy1811 repo)
- Extracts interview questions from different formats
- Outputs: sandy1811_questions.csv

Files to parse:
1. deeplearning_questions.csv (111 DL questions)
2. 1. Machine Learning Interview Questions (50 ML questions)
3. 2. Deep Learning Interview Questions (110 DL questions)
"""

import csv
import re
from datetime import datetime

def parse_dl_csv():
    """Parse deeplearning_questions.csv."""
    questions = []

    try:
        with open('archive/deeplearning_questions.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                question_text = row.get('DESCRIPTION', '').strip()

                if len(question_text) < 10:
                    continue

                # Clean up question
                question_text = re.sub(r'\s+', ' ', question_text)

                questions.append({
                    'question_text': question_text,
                    'company': '',
                    'difficulty': 'medium',
                    'question_type': 'ml',  # Deep learning is subset of ML
                    'topics': 'deep_learning',
                    'source': 'Sandy1811/DS-Interview-FAANG',
                    'answer_text': '',
                    'created_at': datetime.now().isoformat()
                })

        print(f"✅ Parsed {len(questions)} questions from deeplearning_questions.csv")
        return questions

    except Exception as e:
        print(f"⚠️  Error parsing DL CSV: {str(e)}")
        return []

def parse_ml_questions_txt():
    """Parse ML questions text file."""
    questions = []

    try:
        with open('archive/1. Machine Learning Interview Questions', 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines[1:]:  # Skip header
            line = line.strip()
            if not line or line.startswith('S.No'):
                continue

            # Format: Number\tQuestion
            parts = line.split('\t', 1)
            if len(parts) < 2:
                continue

            question_text = parts[1].strip()

            if len(question_text) < 10:
                continue

            # Clean up
            question_text = re.sub(r'\s+', ' ', question_text)

            # Determine difficulty
            difficulty = 'medium'
            q_lower = question_text.lower()
            if any(kw in q_lower for kw in ['what is', 'define', 'name']):
                difficulty = 'easy'
            elif any(kw in q_lower for kw in ['how', 'why', 'explain', 'difference']):
                difficulty = 'medium'
            elif len(question_text) > 80:
                difficulty = 'hard'

            questions.append({
                'question_text': question_text,
                'company': '',
                'difficulty': difficulty,
                'question_type': 'ml',
                'topics': 'machine_learning',
                'source': 'Sandy1811/DS-Interview-FAANG',
                'answer_text': '',
                'created_at': datetime.now().isoformat()
            })

        print(f"✅ Parsed {len(questions)} questions from ML text file")
        return questions

    except Exception as e:
        print(f"⚠️  Error parsing ML text: {str(e)}")
        return []

def parse_dl_questions_txt():
    """Parse DL questions text file."""
    questions = []

    try:
        with open('archive/2. Deep Learning Interview Questions', 'r', encoding='utf-8') as f:
            content = f.read()

        # Pattern: Number. Question?
        # or Number) Question?
        pattern = r'^\s*(\d+)[.)]\s+(.+?)(?=\n\s*\d+[.)]|\Z)'
        matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)

        for match in matches:
            num = match.group(1)
            question_text = match.group(2).strip()

            # Clean up
            question_text = re.sub(r'\s+', ' ', question_text)
            question_text = re.sub(r'\n', ' ', question_text)

            if len(question_text) < 10:
                continue

            # Determine difficulty
            difficulty = 'medium'
            q_lower = question_text.lower()
            if any(kw in q_lower for kw in ['what is', 'define', 'explain briefly']):
                difficulty = 'easy'
            elif any(kw in q_lower for kw in ['how', 'why', 'difference between', 'compare']):
                difficulty = 'medium'
            elif len(question_text) > 100:
                difficulty = 'hard'

            # Determine specific topic
            topics = 'deep_learning'
            if any(kw in q_lower for kw in ['nlp', 'bert', 'word', 'text', 'language']):
                topics = 'nlp'
            elif any(kw in q_lower for kw in ['cnn', 'convolutional', 'image', 'vision']):
                topics = 'computer_vision'
            elif any(kw in q_lower for kw in ['rnn', 'lstm', 'recurrent', 'sequence']):
                topics = 'sequence_models'

            questions.append({
                'question_text': question_text,
                'company': '',
                'difficulty': difficulty,
                'question_type': 'ml',
                'topics': topics,
                'source': 'Sandy1811/DS-Interview-FAANG',
                'answer_text': '',
                'created_at': datetime.now().isoformat()
            })

        print(f"✅ Parsed {len(questions)} questions from DL text file")
        return questions

    except Exception as e:
        print(f"⚠️  Error parsing DL text: {str(e)}")
        return []

def save_to_csv(questions, filename='collected_questions/sandy1811_questions.csv'):
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
    print("  📚 Sandy1811 Archive Parser (FAANG Interview Questions)")
    print("="*80 + "\n")

    all_questions = []

    # Parse each file
    print("Parsing files...\n")

    dl_csv_questions = parse_dl_csv()
    all_questions.extend(dl_csv_questions)

    ml_questions = parse_ml_questions_txt()
    all_questions.extend(ml_questions)

    dl_text_questions = parse_dl_questions_txt()
    all_questions.extend(dl_text_questions)

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

        # Show breakdown by topic
        topic_counts = {}
        for q in all_questions:
            topic = q['topics']
            topic_counts[topic] = topic_counts.get(topic, 0) + 1

        print("\nBreakdown by topic:")
        for topic, count in sorted(topic_counts.items()):
            print(f"  - {topic}: {count}")

        # Save to CSV
        save_to_csv(all_questions)

    print("\n" + "="*80)
    print("✅ Parsing complete!")
    print("="*80 + "\n")
