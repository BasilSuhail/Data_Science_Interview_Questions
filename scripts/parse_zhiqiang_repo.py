"""
SCRIPT: Parse zhiqiangzhongddu Repository

What it does:
- Parses the zhiqiangzhongddu/Data-Science-Interview-Questions repo
- Extracts Q&A from README
- Format: #### QN Question text
- Outputs: zhiqiang_questions.csv
"""

import csv
import re
from datetime import datetime

def parse_zhiqiang_readme():
    """Parse zhiqiangzhongddu README."""
    questions = []

    try:
        with open('temp_zhiqiang_readme.md', 'r', encoding='utf-8') as f:
            content = f.read()

        # Pattern: #### QN Question text
        # Answer follows on next lines
        pattern = r'#### Q(\d+)\s+(.+?)\n\n(.+?)(?=\n#### Q|\Z)'
        matches = re.finditer(pattern, content, re.DOTALL)

        for match in matches:
            num = match.group(1)
            question_text = match.group(2).strip()
            answer_block = match.group(3).strip()

            # Clean up question
            question_text = re.sub(r'\s+', ' ', question_text)

            # Clean up answer
            # Remove image markdown
            answer_text = re.sub(r'!\[.*?\]\(.*?\)', '', answer_block)
            # Remove excessive whitespace
            answer_text = re.sub(r'\s+', ' ', answer_text)
            # Take first 500 chars
            answer_text = answer_text[:500]

            if len(question_text) < 10:
                continue

            # Determine question type
            question_type = 'mixed'
            q_lower = question_text.lower()

            if any(kw in q_lower for kw in ['regression', 'classification', 'model', 'algorithm', 'clustering', 'machine learning']):
                question_type = 'ml'
            elif any(kw in q_lower for kw in ['statistics', 'probability', 'distribution', 'correlation', 'hypothesis']):
                question_type = 'stats'
            elif any(kw in q_lower for kw in ['python', 'r ', ' r,', 'code', 'programming']):
                question_type = 'coding'
            elif any(kw in q_lower for kw in ['data clean', 'analysis', 'analytics', 'trends', 'business']):
                question_type = 'case'
            elif any(kw in q_lower for kw in ['sql', 'database', 'query']):
                question_type = 'sql'

            # Determine difficulty
            difficulty = 'medium'
            if len(answer_text) > 350 or 'complex' in answer_text.lower():
                difficulty = 'hard'
            elif len(answer_text) < 200 or 'simple' in answer_text.lower() or num in ['1', '2', '3']:
                difficulty = 'easy'

            questions.append({
                'question_text': question_text,
                'company': '',
                'difficulty': difficulty,
                'question_type': question_type,
                'topics': 'data_science_general',
                'source': 'zhiqiangzhongddu/DS-QA-General',
                'answer_text': answer_text,
                'created_at': datetime.now().isoformat()
            })

        print(f"✅ Parsed {len(questions)} questions from zhiqiangzhongddu repo")
        return questions

    except Exception as e:
        print(f"⚠️  Error parsing zhiqiangzhongddu: {str(e)}")
        return []

def save_to_csv(questions, filename='collected_questions/zhiqiang_questions.csv'):
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

    print(f"✅ Saved {len(questions)} questions to '{filename}'")

if __name__ == "__main__":
    print("\n" + "="*80)
    print("  📚 zhiqiangzhongddu Repository Parser")
    print("="*80 + "\n")

    questions = parse_zhiqiang_readme()

    if questions:
        # Show breakdown by type
        type_counts = {}
        for q in questions:
            qtype = q['question_type']
            type_counts[qtype] = type_counts.get(qtype, 0) + 1

        print("\nBreakdown by type:")
        for qtype, count in sorted(type_counts.items()):
            print(f"  - {qtype}: {count}")

        # Save to CSV
        save_to_csv(questions)

    print("\n" + "="*80)
    print("✅ Parsing complete!")
    print("="*80 + "\n")
