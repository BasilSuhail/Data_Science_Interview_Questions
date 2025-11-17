"""
SCRIPT 1: GitHub Interview Questions Collector

What it does:
- Fetches curated data science interview question repos from GitHub
- Parses markdown/JSON files
- Tags by company, difficulty, topic, type
- Outputs: github_questions.csv

No authentication needed - uses public GitHub repos!
"""

import requests
import csv
import json
import re
from datetime import datetime

# Popular GitHub repos with curated data science interview questions (2025)
GITHUB_REPOS = [
    {
        'url': 'https://raw.githubusercontent.com/Devinterview-io/data-scientist-interview-questions/main/README.md',
        'name': 'Devinterview-io/data-scientist-interview-questions',
        'type': 'markdown'
    },
    {
        'url': 'https://raw.githubusercontent.com/ajitsingh98/Data-Science-Interview-Questions-Answers/main/README.md',
        'name': 'ajitsingh98/Data-Science-Interview-Questions-Answers',
        'type': 'markdown'
    },
    {
        'url': 'https://raw.githubusercontent.com/youssefHosni/Data-Science-Interview-Questions-Answers/main/README.md',
        'name': 'youssefHosni/Data-Science-Interview-Questions-Answers',
        'type': 'markdown'
    },
    {
        'url': 'https://raw.githubusercontent.com/iamtodor/data-science-interview-questions-and-answers/master/README.md',
        'name': 'iamtodor/data-science-interview-questions-and-answers',
        'type': 'markdown'
    }
]

def extract_questions_from_markdown(content, source_name):
    """Extract questions from markdown format."""
    questions = []

    # Pattern 1: Numbered questions (1. Question?)
    numbered_pattern = r'^\s*\d+\.\s+(.+?)(?=\n\s*\d+\.|\Z)'
    matches = re.findall(numbered_pattern, content, re.MULTILINE | re.DOTALL)

    for match in matches:
        question_text = match.strip()

        # Skip if too short or doesn't look like a question
        if len(question_text) < 20:
            continue

        # Detect question type based on keywords
        question_type = detect_question_type(question_text)

        # Detect difficulty (if mentioned)
        difficulty = detect_difficulty(question_text)

        # Detect company (if mentioned)
        company = detect_company(question_text)

        # Detect topics
        topics = detect_topics(question_text)

        questions.append({
            'question_text': clean_question_text(question_text),
            'company': company,
            'difficulty': difficulty,
            'question_type': question_type,
            'topics': '|'.join(topics) if topics else '',
            'source': source_name,
            'answer_text': '',  # GitHub repos usually don't have answers
            'created_at': datetime.now().isoformat()
        })

    # Pattern 2: Questions starting with "Q:" or "Question:"
    q_pattern = r'(?:^|\n)(?:Q:|Question:)\s*(.+?)(?=\n(?:Q:|Question:|\d+\.)|\Z)'
    matches = re.findall(q_pattern, content, re.DOTALL)

    for match in matches:
        question_text = match.strip()

        if len(question_text) < 20:
            continue

        questions.append({
            'question_text': clean_question_text(question_text),
            'company': detect_company(question_text),
            'difficulty': detect_difficulty(question_text),
            'question_type': detect_question_type(question_text),
            'topics': '|'.join(detect_topics(question_text)),
            'source': source_name,
            'answer_text': '',
            'created_at': datetime.now().isoformat()
        })

    return questions

def clean_question_text(text):
    """Clean up question text."""
    # Remove markdown formatting
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.+?)\*', r'\1', text)  # Italic
    text = re.sub(r'`(.+?)`', r'\1', text)  # Code
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)  # Links

    # Remove multiple newlines
    text = re.sub(r'\n+', ' ', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

def detect_question_type(text):
    """Detect question type based on keywords."""
    text_lower = text.lower()

    # Coding keywords
    if any(keyword in text_lower for keyword in ['sql', 'query', 'select', 'join', 'python code', 'write a function', 'algorithm', 'data structure']):
        return 'coding'

    # Statistics keywords
    if any(keyword in text_lower for keyword in ['p-value', 'hypothesis test', 'confidence interval', 'distribution', 'probability', 'statistical', 'variance', 'mean', 'median']):
        return 'stats'

    # ML keywords
    if any(keyword in text_lower for keyword in ['machine learning', 'model', 'training', 'overfitting', 'regularization', 'neural network', 'random forest', 'gradient']):
        return 'ml'

    # Case study keywords
    if any(keyword in text_lower for keyword in ['design', 'metrics', 'a/b test', 'experiment', 'product', 'how would you', 'business problem']):
        return 'case'

    # Behavioral keywords
    if any(keyword in text_lower for keyword in ['tell me about', 'describe a time', 'how do you handle', 'conflict', 'team', 'challenge']):
        return 'behavioral'

    return 'mixed'

def detect_difficulty(text):
    """Detect difficulty level if mentioned."""
    text_lower = text.lower()

    if 'easy' in text_lower:
        return 'easy'
    if 'hard' in text_lower or 'difficult' in text_lower or 'advanced' in text_lower:
        return 'hard'
    if 'medium' in text_lower or 'intermediate' in text_lower:
        return 'medium'

    return 'medium'  # Default

def detect_company(text):
    """Detect company name if mentioned."""
    companies = ['Google', 'Meta', 'Facebook', 'Amazon', 'Microsoft', 'Apple',
                 'Netflix', 'Tesla', 'Uber', 'Airbnb', 'LinkedIn', 'Twitter']

    for company in companies:
        if company.lower() in text.lower():
            return company

    return ''

def detect_topics(text):
    """Detect relevant topics."""
    topics = []
    text_lower = text.lower()

    topic_keywords = {
        'regression': ['regression', 'linear model', 'logistic'],
        'classification': ['classification', 'classifier', 'predict class'],
        'clustering': ['clustering', 'k-means', 'unsupervised'],
        'hypothesis_testing': ['hypothesis test', 'p-value', 'significance'],
        'probability': ['probability', 'distribution', 'bayes'],
        'sql': ['sql', 'query', 'database', 'join'],
        'python': ['python', 'pandas', 'numpy'],
        'deep_learning': ['neural network', 'deep learning', 'cnn', 'rnn'],
        'ensemble': ['random forest', 'boosting', 'ensemble', 'xgboost'],
        'metrics': ['precision', 'recall', 'f1', 'auc', 'roc'],
        'feature_engineering': ['feature', 'preprocessing', 'normalization'],
        'ab_testing': ['a/b test', 'experiment design', 'control group']
    }

    for topic, keywords in topic_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            topics.append(topic)

    return topics

def fetch_github_questions():
    """Main function to fetch questions from all GitHub repos."""
    all_questions = []

    print("\n" + "="*80)
    print("  📚 GitHub Data Science Interview Questions Collector")
    print("="*80 + "\n")

    for repo in GITHUB_REPOS:
        print(f"Fetching from: {repo['name']}")

        try:
            response = requests.get(repo['url'], timeout=30)

            if response.status_code == 200:
                content = response.text
                questions = extract_questions_from_markdown(content, repo['name'])

                print(f"  ✅ Found {len(questions)} questions")
                all_questions.extend(questions)
            else:
                print(f"  ❌ Failed to fetch (HTTP {response.status_code})")

        except Exception as e:
            print(f"  ❌ Error: {str(e)}")

    return all_questions

def save_to_csv(questions, filename='github_questions.csv'):
    """Save questions to CSV file."""
    if not questions:
        print("\n❌ No questions collected!")
        return

    fieldnames = ['question_text', 'company', 'difficulty', 'question_type',
                  'topics', 'source', 'answer_text', 'created_at']

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(questions)

    print(f"\n✅ Saved {len(questions)} questions to '{filename}'")

    # Print statistics
    print(f"\n📊 Statistics:")
    print(f"   - Total questions: {len(questions)}")

    # Count by type
    type_counts = {}
    for q in questions:
        qtype = q['question_type']
        type_counts[qtype] = type_counts.get(qtype, 0) + 1

    print(f"\n   By type:")
    for qtype, count in sorted(type_counts.items()):
        print(f"     - {qtype}: {count}")

    # Count with company tags
    with_company = sum(1 for q in questions if q['company'])
    print(f"\n   - With company tags: {with_company}")

if __name__ == "__main__":
    questions = fetch_github_questions()
    save_to_csv(questions)

    print("\n" + "="*80)
    print("✅ GitHub collection complete!")
    print("="*80 + "\n")
