import sqlite3
import os


def view_all_questions():
    """View all questions in the database"""
    conn = sqlite3.connect('interview_questions.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM questions')
    total = cursor.fetchone()[0]

    if total == 0:
        print("\n⚠️  No questions in database yet!")
        print("Run 'python curate_questions.py' to add questions.\n")
        conn.close()
        return

    cursor.execute('''
        SELECT id, category, question, difficulty, source_book
        FROM questions
        ORDER BY category, difficulty
    ''')
    rows = cursor.fetchall()
    conn.close()

    print(f"\n{'='*100}")
    print(f"ALL QUESTIONS ({total} total)")
    print(f"{'='*100}\n")

    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Category: {row[1]}")
        print(f"Question: {row[2]}")
        print(f"Difficulty: {row[3]}")
        print(f"Source: {row[4] if row[4] else 'N/A'}")
        print("-" * 100)


def view_question_detail(question_id):
    """View detailed information about a specific question"""
    conn = sqlite3.connect('interview_questions.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM questions WHERE id = ?', (question_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        print(f"\n⚠️  Question ID {question_id} not found!")
        return

    print(f"\n{'='*100}")
    print(f"QUESTION DETAILS")
    print(f"{'='*100}\n")

    print(f"ID: {row[0]}")
    print(f"Category: {row[1]}")
    print(f"Subcategory: {row[2] if row[2] else 'N/A'}")
    print(f"Question: {row[3]}")
    print(f"\nAnswer: {row[4] if row[4] else 'No answer provided'}")
    print(f"\nDifficulty: {row[5]}")
    print(f"Source: {row[6] if row[6] else 'N/A'}")
    print(f"Page: {row[7] if row[7] else 'N/A'}")
    print(f"Tags: {row[8] if row[8] else 'None'}")
    print(f"Date Added: {row[9]}")
    print(f"Notes: {row[11] if row[11] else 'None'}")
    print(f"\n{'='*100}\n")


def filter_by_category():
    """Filter questions by category"""
    conn = sqlite3.connect('interview_questions.db')
    cursor = conn.cursor()

    # Show available categories
    cursor.execute('SELECT DISTINCT category FROM questions ORDER BY category')
    categories = cursor.fetchall()

    if not categories:
        print("\n⚠️  No questions in database yet!")
        conn.close()
        return

    print("\nAvailable categories:")
    for i, (cat,) in enumerate(categories, 1):
        print(f"  {i}. {cat}")

    category = input("\nEnter category name: ").strip()

    cursor.execute('''
        SELECT id, question, difficulty, source_book
        FROM questions
        WHERE category = ?
        ORDER BY difficulty
    ''', (category,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print(f"\n⚠️  No questions found in category '{category}'")
        return

    print(f"\n{'='*100}")
    print(f"QUESTIONS IN CATEGORY: {category} ({len(rows)} found)")
    print(f"{'='*100}\n")

    for row in rows:
        print(f"ID: {row[0]} | Difficulty: {row[2]} | Source: {row[3] if row[3] else 'N/A'}")
        print(f"Q: {row[1]}")
        print("-" * 100)


def filter_by_difficulty():
    """Filter questions by difficulty"""
    difficulty = input("Enter difficulty (Easy/Medium/Hard): ").strip()

    conn = sqlite3.connect('interview_questions.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, category, question, source_book
        FROM questions
        WHERE difficulty = ?
        ORDER BY category
    ''', (difficulty,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print(f"\n⚠️  No {difficulty} questions found")
        return

    print(f"\n{'='*100}")
    print(f"{difficulty.upper()} QUESTIONS ({len(rows)} found)")
    print(f"{'='*100}\n")

    for row in rows:
        print(f"ID: {row[0]} | Category: {row[1]} | Source: {row[3] if row[3] else 'N/A'}")
        print(f"Q: {row[2]}")
        print("-" * 100)


def search_questions():
    """Search questions by keyword"""
    keyword = input("Enter search term: ").strip()

    conn = sqlite3.connect('interview_questions.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, category, question, difficulty
        FROM questions
        WHERE question LIKE ? OR answer LIKE ? OR tags LIKE ?
        ORDER BY category
    ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print(f"\n⚠️  No questions found matching '{keyword}'")
        return

    print(f"\n{'='*100}")
    print(f"SEARCH RESULTS for '{keyword}' ({len(rows)} found)")
    print(f"{'='*100}\n")

    for row in rows:
        print(f"ID: {row[0]} | Category: {row[1]} | Difficulty: {row[3]}")
        print(f"Q: {row[2]}")
        print("-" * 100)


def show_statistics():
    """Show database statistics"""
    conn = sqlite3.connect('interview_questions.db')
    cursor = conn.cursor()

    print(f"\n{'='*100}")
    print("DATABASE STATISTICS")
    print(f"{'='*100}\n")

    # Total questions
    cursor.execute('SELECT COUNT(*) FROM questions')
    total = cursor.fetchone()[0]
    print(f"Total Questions: {total}")

    # Questions with answers
    cursor.execute('SELECT COUNT(*) FROM questions WHERE answer IS NOT NULL AND answer != ""')
    with_answers = cursor.fetchone()[0]
    print(f"Questions with Answers: {with_answers} ({with_answers*100//total if total > 0 else 0}%)")

    # By category
    cursor.execute('SELECT category, COUNT(*) FROM questions GROUP BY category ORDER BY COUNT(*) DESC')
    categories = cursor.fetchall()
    print("\nBy Category:")
    for cat, count in categories:
        print(f"  {cat}: {count}")

    # By difficulty
    cursor.execute('SELECT difficulty, COUNT(*) FROM questions GROUP BY difficulty')
    difficulties = cursor.fetchall()
    print("\nBy Difficulty:")
    for diff, count in difficulties:
        print(f"  {diff}: {count}")

    # By source
    cursor.execute('SELECT source_book, COUNT(*) FROM questions WHERE source_book IS NOT NULL GROUP BY source_book')
    sources = cursor.fetchall()
    print("\nBy Source:")
    for source, count in sources:
        print(f"  {source}: {count}")

    conn.close()
    print(f"\n{'='*100}\n")


def export_to_csv():
    """Export all questions to a CSV file"""
    import csv

    conn = sqlite3.connect('interview_questions.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM questions')
    rows = cursor.fetchall()

    if not rows:
        print("\n⚠️  No questions to export!")
        conn.close()
        return

    filename = 'interview_questions_export.csv'

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Write header
        writer.writerow([
            'ID', 'Category', 'Subcategory', 'Question', 'Answer',
            'Difficulty', 'Source Book', 'Page Number', 'Tags',
            'Date Added', 'Last Modified', 'Notes'
        ])

        # Write data
        writer.writerows(rows)

    conn.close()

    print(f"\n✓ Exported {len(rows)} questions to '{filename}'")


def main():
    """Main menu"""

    if not os.path.exists('interview_questions.db'):
        print("\n⚠️  Database not found!")
        print("Please run 'python create_database.py' first.\n")
        return

    while True:
        print(f"\n{'='*100}")
        print("INTERVIEW QUESTIONS DATABASE MANAGER")
        print(f"{'='*100}")
        print("\n1. View all questions")
        print("2. View question details (by ID)")
        print("3. Filter by category")
        print("4. Filter by difficulty")
        print("5. Search questions")
        print("6. Show statistics")
        print("7. Export to CSV")
        print("8. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == '1':
            view_all_questions()
        elif choice == '2':
            try:
                q_id = int(input("Enter question ID: ").strip())
                view_question_detail(q_id)
            except ValueError:
                print("Invalid ID!")
        elif choice == '3':
            filter_by_category()
        elif choice == '4':
            filter_by_difficulty()
        elif choice == '5':
            search_questions()
        elif choice == '6':
            show_statistics()
        elif choice == '7':
            export_to_csv()
        elif choice == '8':
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice!")


if __name__ == '__main__':
    main()
