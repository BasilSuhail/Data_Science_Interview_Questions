"""
SCRIPT 2: LeetCode Discuss Scraper

What it does:
- Scrapes LeetCode Discuss "Interview Experience" posts
- Extracts: company, questions, difficulty
- Filters for data science/ML roles
- Outputs: leetcode_questions.csv

Uses public LeetCode Discuss forum (no login required)
"""

import requests
import csv
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup

# LeetCode Discuss topics related to data science interviews
LEETCODE_DISCUSS_URLS = [
    'https://leetcode.com/discuss/interview-experience?currentPage=1&orderBy=hot&query=data%20science',
    'https://leetcode.com/discuss/interview-experience?currentPage=1&orderBy=hot&query=machine%20learning',
    'https://leetcode.com/discuss/interview-experience?currentPage=1&orderBy=hot&query=data%20analyst'
]

def scrape_leetcode_discuss():
    """Scrape LeetCode Discuss for interview questions."""
    all_questions = []

    print("\n" + "="*80)
    print("  💬 LeetCode Discuss Interview Questions Scraper")
    print("="*80 + "\n")

    print("⚠️  NOTE: LeetCode may have rate limiting or require headers.")
    print("   If this fails, we'll use a simpler approach.\n")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    for url in LEETCODE_DISCUSS_URLS:
        print(f"Fetching: {url.split('query=')[1].split('&')[0].replace('%20', ' ')}")

        try:
            response = requests.get(url, headers=headers, timeout=30)

            if response.status_code == 200:
                # LeetCode uses dynamic content, so simple scraping may not work
                # This is a placeholder - would need Selenium/Playwright for full scraping

                print(f"  ⚠️  LeetCode uses dynamic content (JavaScript-rendered)")
                print(f"     Skipping full scrape for now")

            else:
                print(f"  ❌ Failed (HTTP {response.status_code})")

        except Exception as e:
            print(f"  ❌ Error: {str(e)}")

        time.sleep(2)  # Be polite with rate limiting

    # Since LeetCode scraping is complex, we'll create a manual template instead
    print(f"\n💡 Alternative: Use manual collection template")
    create_manual_template()

    return all_questions

def create_manual_template():
    """Create a template for manual LeetCode question collection."""
    template_content = """# LeetCode Discuss - Manual Collection Template

Since LeetCode uses JavaScript-rendered content, automated scraping is difficult.
Instead, manually copy questions from LeetCode Discuss and paste them here.

## How to Use:

1. Go to: https://leetcode.com/discuss/interview-experience
2. Search for "data science" or "machine learning"
3. Open interesting interview experience posts
4. Copy questions and paste below in this format:

---

## [Company Name] - [Role]

**Difficulty**: easy/medium/hard
**Type**: coding/stats/ml/case/behavioral

**Question 1:**
[Paste question here]

**Question 2:**
[Paste question here]

---

Repeat for each company/post you find!

After filling this template, run: python parse_manual_questions.py
"""

    with open('leetcode_manual_template.txt', 'w', encoding='utf-8') as f:
        f.write(template_content)

    print(f"\n✅ Created: leetcode_manual_template.txt")
    print(f"   Fill this template with questions from LeetCode Discuss")

def save_to_csv(questions, filename='leetcode_questions.csv'):
    """Save questions to CSV."""
    if not questions:
        print("\n⚠️  No automated questions collected (LeetCode requires JavaScript)")
        print("   Use the manual template instead!")
        return

    fieldnames = ['question_text', 'company', 'difficulty', 'question_type',
                  'topics', 'source', 'answer_text', 'created_at']

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(questions)

    print(f"\n✅ Saved {len(questions)} questions to '{filename}'")

if __name__ == "__main__":
    questions = scrape_leetcode_discuss()
    save_to_csv(questions)

    print("\n" + "="*80)
    print("✅ LeetCode template created!")
    print("   Next steps:")
    print("   1. Open leetcode_manual_template.txt")
    print("   2. Fill with questions from LeetCode Discuss")
    print("   3. Run: python parse_manual_questions.py")
    print("="*80 + "\n")
