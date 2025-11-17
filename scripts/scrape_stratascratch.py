"""
SCRIPT 3: StrataScratch Automated Collector

What it does:
- Uses Playwright to automate browser
- You log in once to StrataScratch
- Script collects questions automatically
- Outputs: stratascratch_questions.csv

REQUIRES: You to sign up at https://www.stratascratch.com first!
"""

import csv
import time
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

def scrape_stratascratch():
    """Scrape StrataScratch questions using Playwright."""

    if not PLAYWRIGHT_AVAILABLE:
        print("\n❌ Playwright not installed!")
        print("\nTo install:")
        print("  pip install playwright")
        print("  playwright install chromium")
        print("\nOr use manual collection template instead.")
        create_manual_stratascratch_template()
        return []

    print("\n" + "="*80)
    print("  🎯 StrataScratch Automated Question Collector")
    print("="*80 + "\n")

    print("📋 Instructions:")
    print("   1. Browser will open")
    print("   2. Log in to StrataScratch manually")
    print("   3. Script will collect questions automatically")
    print("   4. Don't close the browser during collection\n")

    questions = []

    with sync_playwright() as p:
        # Launch browser (non-headless so you can log in)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            # Go to StrataScratch
            print("Opening StrataScratch...")
            page.goto('https://www.stratascratch.com/coding', wait_until='networkidle')

            print("\n⏸  PLEASE LOG IN NOW")
            print("   (You have 60 seconds)")
            time.sleep(60)  # Give user time to log in

            # Navigate to questions page
            print("\nNavigating to questions...")
            page.goto('https://www.stratascratch.com/coding?filters=%7B%7D', wait_until='networkidle')

            time.sleep(3)

            # Try to extract questions
            print("\nExtracting questions...\n")

            # This is a simplified example - actual selectors may differ
            # You'll need to inspect StrataScratch's HTML to find correct selectors

            question_cards = page.query_selector_all('.question-card')  # Example selector

            if not question_cards:
                print("⚠️  Could not find question cards")
                print("   StrataScratch HTML structure may have changed")
                print("   Using manual template instead...")
                create_manual_stratascratch_template()
            else:
                for i, card in enumerate(question_cards[:50], 1):  # Limit to first 50
                    try:
                        title = card.query_selector('.question-title').inner_text()
                        difficulty = card.query_selector('.difficulty').inner_text()
                        company = card.query_selector('.company-tag').inner_text() if card.query_selector('.company-tag') else ''

                        questions.append({
                            'question_text': title,
                            'company': company,
                            'difficulty': difficulty.lower(),
                            'question_type': 'coding',  # StrataScratch is primarily SQL/Python
                            'topics': 'sql',
                            'source': 'StrataScratch',
                            'answer_text': '',
                            'created_at': datetime.now().isoformat()
                        })

                        print(f"  {i}. {title[:50]}...")

                    except Exception as e:
                        print(f"  ⚠️  Skipped card {i}: {str(e)}")

                print(f"\n✅ Collected {len(questions)} questions")

        except Exception as e:
            print(f"\n❌ Error during scraping: {str(e)}")
            print("   Falling back to manual template...")
            create_manual_stratascratch_template()

        finally:
            print("\nClosing browser...")
            browser.close()

    return questions

def create_manual_stratascratch_template():
    """Create template for manual StrataScratch collection."""
    template_content = """# StrataScratch - Manual Collection Template

## How to Use:

1. Go to: https://www.stratascratch.com
2. Sign up for free account
3. Browse coding questions
4. Copy questions and paste below in this format:

---

**Company**: [Company Name or "General"]
**Difficulty**: easy/medium/hard
**Type**: sql/python

**Question Title:**
[Question title/description]

**Question Details:**
[Full question text if available]

---

Example:

**Company**: Netflix
**Difficulty**: medium
**Type**: sql

**Question Title:**
Count the number of movies per genre

**Question Details:**
Write a query to find the number of movies in each genre. Return the genre name and count, ordered by count descending.

---

After filling this template, save and run: python parse_manual_questions.py
"""

    with open('stratascratch_manual_template.txt', 'w', encoding='utf-8') as f:
        f.write(template_content)

    print(f"\n✅ Created: stratascratch_manual_template.txt")
    print(f"   Fill this template with StrataScratch questions")

def save_to_csv(questions, filename='stratascratch_questions.csv'):
    """Save questions to CSV."""
    if not questions:
        print("\n⚠️  No questions collected automatically")
        print("   Use the manual template!")
        return

    fieldnames = ['question_text', 'company', 'difficulty', 'question_type',
                  'topics', 'source', 'answer_text', 'created_at']

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(questions)

    print(f"\n✅ Saved {len(questions)} questions to '{filename}'")

if __name__ == "__main__":
    questions = scrape_stratascratch()
    save_to_csv(questions)

    print("\n" + "="*80)
    print("✅ StrataScratch collection complete!")
    print("="*80 + "\n")
