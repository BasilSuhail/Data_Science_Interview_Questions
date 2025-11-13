import sqlite3
from datetime import datetime

def create_database():
    """
    Creates an improved SQLite database for storing interview questions.
    This version includes answers, sources, tags, and metadata.
    """

    # Connect to the database (creates file if it doesn't exist)
    conn = sqlite3.connect('interview_questions.db')
    cursor = conn.cursor()

    # Create the main questions table with enhanced schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            subcategory TEXT,
            question TEXT NOT NULL,
            answer TEXT,
            difficulty TEXT CHECK(difficulty IN ('Easy', 'Medium', 'Hard')),
            source_book TEXT,
            page_number INTEGER,
            tags TEXT,
            date_added TEXT DEFAULT CURRENT_TIMESTAMP,
            last_modified TEXT DEFAULT CURRENT_TIMESTAMP,
            notes TEXT
        )
    ''')

    # Create a books table to track source materials
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            filename TEXT NOT NULL,
            total_pages INTEGER,
            date_added TEXT DEFAULT CURRENT_TIMESTAMP,
            extraction_status TEXT DEFAULT 'pending'
        )
    ''')

    # Create an index for faster searches
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON questions(category)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_difficulty ON questions(difficulty)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_source ON questions(source_book)')

    conn.commit()
    conn.close()

    print("✓ Database created successfully!")
    print("✓ Tables created: 'questions', 'books'")
    print("✓ Indexes created for faster searching")

if __name__ == '__main__':
    create_database()
