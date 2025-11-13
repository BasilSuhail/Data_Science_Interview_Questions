import sqlite3

def add_question():
    category = input("Enter category: ")
    question = input("Enter question: ")
    difficulty = input("Enter difficulty: ")

    conn = sqlite3.connect('interview_questions.db')
    c = conn.cursor()
    c.execute("INSERT INTO questions (category, question, difficulty) VALUES (?, ?, ?)", (category, question, difficulty))
    conn.commit()
    conn.close()
    print("Question added successfully.")

def view_all_questions():
    conn = sqlite3.connect('interview_questions.db')
    c = conn.cursor()
    c.execute("SELECT * FROM questions")
    rows = c.fetchall()
    conn.close()

    for row in rows:
        print(f"ID: {row[0]}, Category: {row[1]}, Question: {row[2]}, Difficulty: {row[3]}")

def filter_by_category():
    category = input("Enter category to filter by: ")
    conn = sqlite3.connect('interview_questions.db')
    c = conn.cursor()
    c.execute("SELECT * FROM questions WHERE category=?", (category,))
    rows = c.fetchall()
    conn.close()

    for row in rows:
        print(f"ID: {row[0]}, Category: {row[1]}, Question: {row[2]}, Difficulty: {row[3]}")

def filter_by_difficulty():
    difficulty = input("Enter difficulty to filter by: ")
    conn = sqlite3.connect('interview_questions.db')
    c = conn.cursor()
    c.execute("SELECT * FROM questions WHERE difficulty=?", (difficulty,))
    rows = c.fetchall()
    conn.close()

    for row in rows:
        print(f"ID: {row[0]}, Category: {row[1]}, Question: {row[2]}, Difficulty: {row[3]}")

def main():
    while True:
        print("\n--- Interview Questions Database ---")
        print("1. Add a new question")
        print("2. View all questions")
        print("3. Filter by category")
        print("4. Filter by difficulty")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_question()
        elif choice == '2':
            view_all_questions()
        elif choice == '3':
            filter_by_category()
        elif choice == '4':
            filter_by_difficulty()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
