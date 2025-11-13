import sqlite3
import os
import re
from pathlib import Path


def find_potential_questions(text):
    """
    Identify potential questions in text using common patterns.
    Returns a list of potential questions with their context.
    """
    questions = []

    # Split text into lines
    lines = text.split('\n')

    # Patterns that might indicate questions
    question_patterns = [
        r'^\d+\.\s+(.+\?)',  # Numbered questions ending with ?
        r'^Q\d*[\.:]\s*(.+)',  # Q1: or Q. patterns
        r'^Question\s*\d*[\.:]\s*(.+)',  # Question 1: patterns
        r'^\*\s+(.+\?)',  # Bullet points ending with ?
        r'^[A-Z][^.!?]*\?$',  # Lines starting with capital and ending with ?
    ]

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        # Check for explicit question patterns
        for pattern in question_patterns:
            match = re.match(pattern, line)
            if match:
                # Get some context (next few lines might be the answer)
                context_lines = lines[i:min(i+5, len(lines))]
                questions.append({
                    'question': line,
                    'context': '\n'.join(context_lines),
                    'line_number': i + 1
                })
                break

    return questions


def interactive_curation():
    """
    Interactive tool to help you curate questions from extracted text.
    """
    print("\n" + "="*80)
    print("INTERACTIVE QUESTION CURATION TOOL")
    print("="*80 + "\n")

    # Check if we have extracted text
    extracted_dir = Path('extracted_text')
    if not extracted_dir.exists():
        print("⚠️  No extracted text found!")
        print("Please run 'python extract_pdf_content.py' first.")
        return

    # Get all book directories
    book_dirs = [d for d in extracted_dir.iterdir() if d.is_dir()]

    if not book_dirs:
        print("⚠️  No extracted books found!")
        return

    print("Available books:")
    for i, book_dir in enumerate(book_dirs, 1):
        print(f"  {i}. {book_dir.name}")

    print(f"  {len(book_dirs) + 1}. Process all books")
    print(f"  0. Exit")

    choice = input("\nSelect a book (0 to exit): ").strip()

    if choice == '0':
        return

    if choice == str(len(book_dirs) + 1):
        selected_books = book_dirs
    else:
        try:
            idx = int(choice) - 1
            selected_books = [book_dirs[idx]]
        except (ValueError, IndexError):
            print("Invalid choice!")
            return

    # Process selected books
    conn = sqlite3.connect('interview_questions.db')
    cursor = conn.cursor()

    for book_dir in selected_books:
        print(f"\n{'='*80}")
        print(f"Processing: {book_dir.name}")
        print(f"{'='*80}\n")

        # Read the full text
        full_text_path = book_dir / 'full_text.txt'
        if not full_text_path.exists():
            print(f"⚠️  No full_text.txt found in {book_dir.name}")
            continue

        with open(full_text_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Find potential questions
        potential_questions = find_potential_questions(text)

        if not potential_questions:
            print("No obvious questions found using automatic detection.")
            print("You may need to manually review the extracted text.")
            continue

        print(f"Found {len(potential_questions)} potential questions!\n")

        # Ask user if they want to review them
        review = input("Review and add questions? (y/n): ").strip().lower()

        if review != 'y':
            continue

        added_count = 0

        for i, q_data in enumerate(potential_questions, 1):
            print(f"\n--- Question {i}/{len(potential_questions)} ---")
            print(f"Question: {q_data['question']}")
            print(f"\nContext:")
            print(q_data['context'][:300] + "..." if len(q_data['context']) > 300 else q_data['context'])

            action = input("\nAction (a=add, s=skip, e=edit, q=quit): ").strip().lower()

            if action == 'q':
                break
            elif action == 's':
                continue
            elif action in ['a', 'e']:
                # Prepare question data
                question_text = q_data['question']

                if action == 'e':
                    print("\nEnter question (or press Enter to keep current):")
                    new_q = input().strip()
                    if new_q:
                        question_text = new_q

                # Get additional information
                category = input("Category (e.g., Statistics, ML, Python): ").strip() or "General"
                difficulty = input("Difficulty (Easy/Medium/Hard): ").strip() or "Medium"
                answer = input("Answer (optional, press Enter to skip): ").strip() or None
                tags = input("Tags (comma-separated, optional): ").strip() or None

                # Insert into database
                cursor.execute('''
                    INSERT INTO questions
                    (category, question, answer, difficulty, source_book, tags)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (category, question_text, answer, difficulty, book_dir.name, tags))

                added_count += 1
                print("✓ Question added!")

        conn.commit()
        print(f"\n✓ Added {added_count} questions from {book_dir.name}")

    conn.close()
    print("\n" + "="*80)
    print("CURATION COMPLETE!")
    print("="*80)


def manual_add_question():
    """
    Manually add a question to the database without extraction.
    """
    print("\n" + "="*80)
    print("MANUAL QUESTION ENTRY")
    print("="*80 + "\n")

    conn = sqlite3.connect('interview_questions.db')
    cursor = conn.cursor()

    while True:
        print("\nEnter question details (or type 'done' to finish):")

        question = input("Question: ").strip()
        if question.lower() == 'done':
            break

        answer = input("Answer: ").strip()
        category = input("Category: ").strip() or "General"
        difficulty = input("Difficulty (Easy/Medium/Hard): ").strip() or "Medium"
        tags = input("Tags (comma-separated): ").strip() or None
        source = input("Source (book/website): ").strip() or None

        cursor.execute('''
            INSERT INTO questions
            (category, question, answer, difficulty, source_book, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (category, question, answer, difficulty, source, tags))

        conn.commit()
        print("✓ Question added!\n")

    conn.close()
    print("\nAll questions saved!")


def view_statistics():
    """Display statistics about the database"""
    conn = sqlite3.connect('interview_questions.db')
    cursor = conn.cursor()

    print("\n" + "="*80)
    print("DATABASE STATISTICS")
    print("="*80 + "\n")

    # Total questions
    cursor.execute('SELECT COUNT(*) FROM questions')
    total = cursor.fetchone()[0]
    print(f"Total Questions: {total}")

    # By category
    cursor.execute('SELECT category, COUNT(*) FROM questions GROUP BY category')
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

    # Books registered
    cursor.execute('SELECT COUNT(*) FROM books')
    total_books = cursor.fetchone()[0]
    print(f"\nBooks Registered: {total_books}")

    conn.close()
    print("\n" + "="*80 + "\n")


def main_menu():
    """Main menu for the curation tool"""

    while True:
        print("\n" + "="*80)
        print("QUESTION CURATION MENU")
        print("="*80)
        print("\n1. Interactive curation from extracted text")
        print("2. Manually add a question")
        print("3. View database statistics")
        print("4. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == '1':
            interactive_curation()
        elif choice == '2':
            manual_add_question()
        elif choice == '3':
            view_statistics()
        elif choice == '4':
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice!")


if __name__ == '__main__':
    # Check if database exists
    if not os.path.exists('interview_questions.db'):
        print("⚠️  Database not found!")
        print("Please run 'python create_database.py' first.")
        exit(1)

    main_menu()
