"""
SCRIPT: jayinai Repository Parser

What it does:
- Parses the jayinai data-science-question-answer README
- Extracts Q&A sections structured as ### Topic headings
- Converts to standardized CSV format
- Outputs: jayinai_questions.csv

The README structure is:
### Topic Name (this becomes the question)
Content explaining the topic (this becomes partial answer/context)
"""

import csv
import re
from datetime import datetime

def parse_jayinai_readme(filename='temp_jayinai_readme.md'):
    """Parse jayinai README into questions."""
    questions = []

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split into sections by ### headers (topic headings)
        # These headings are essentially interview questions
        sections = re.split(r'\n### ', content)

        # Track current category for context
        current_category = ''

        for section in sections:
            # Skip empty sections
            if len(section.strip()) < 20:
                continue

            # Check if this is a category header (## Category)
            category_match = re.match(r'^##\s+(.+?)\n', section)
            if category_match:
                current_category = category_match.group(1).strip()
                # Remove common suffixes
                current_category = current_category.replace(' and ML In General', '')
                current_category = current_category.replace(' Learning', '')
                continue

            # Extract topic heading (the question)
            lines = section.split('\n')
            if not lines:
                continue

            topic = lines[0].strip()

            # Skip navigation links and non-question topics
            skip_keywords = ['back to top', 'top](#', '[', '(#', 'http']
            if any(keyword in topic.lower() for keyword in skip_keywords):
                continue

            # Skip very short topics
            if len(topic) < 5:
                continue

            # Get the content (explanation)
            content_text = '\n'.join(lines[1:]).strip()

            # Clean up content - remove markdown image links
            content_text = re.sub(r'!\[.*?\]\(.*?\)', '', content_text)
            content_text = re.sub(r'\[back to top.*?\]', '', content_text, flags=re.IGNORECASE)
            content_text = content_text.strip()

            # Skip if no meaningful content
            if len(content_text) < 30:
                continue

            # Determine question type based on category
            question_type = 'mixed'
            if current_category in ['SQL', 'Tools and Framework']:
                question_type = 'sql' if 'SQL' in current_category else 'coding'
            elif current_category in ['Statistics', 'ML']:
                question_type = 'stats'
            elif current_category in ['Supervised', 'Unsupervised']:
                question_type = 'ml'
            elif current_category in ['Natural Language Processing', 'NLP']:
                question_type = 'ml'
            elif current_category in ['System']:
                question_type = 'system_design'

            # Determine difficulty based on content length and complexity
            difficulty = 'medium'
            if len(content_text) > 500:
                difficulty = 'hard'
            elif len(content_text) < 200:
                difficulty = 'easy'

            # Format the question text
            # Convert topic heading to question format if it's not already
            question_text = topic
            if not topic.endswith('?'):
                # Add question words if missing
                if topic.lower().startswith(('what', 'how', 'why', 'when', 'which', 'explain')):
                    question_text = topic
                else:
                    # Convert topic to question format
                    question_text = f"Explain {topic}"

            # Clean up question text
            question_text = re.sub(r'\s+', ' ', question_text).strip()

            questions.append({
                'question_text': question_text,
                'company': '',
                'difficulty': difficulty,
                'question_type': question_type,
                'topics': current_category.lower() if current_category else '',
                'source': 'jayinai/data-science-question-answer',
                'answer_text': content_text[:500],  # First 500 chars as preview
                'created_at': datetime.now().isoformat()
            })

        return questions

    except FileNotFoundError:
        print(f"⚠️  File not found: {filename}")
        print("   Run this command first:")
        print('   curl -s "https://raw.githubusercontent.com/jayinai/data-science-question-answer/master/README.md" > temp_jayinai_readme.md')
        return []
    except Exception as e:
        print(f"⚠️  Error parsing {filename}: {str(e)}")
        return []

def save_to_csv(questions, filename='collected_questions/jayinai_questions.csv'):
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
    print("  📚 jayinai Repository Parser")
    print("="*80 + "\n")

    # Parse the README
    questions = parse_jayinai_readme()

    if questions:
        print(f"✅ Extracted {len(questions)} questions from README")

        # Show breakdown
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
