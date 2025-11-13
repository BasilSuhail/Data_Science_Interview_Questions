import sqlite3

# List of questions to be inserted
questions = [
    # Statistics
    ('Statistics', 'Explain the difference between descriptive and inferential statistics.', 'Easy'),
    ('Statistics', 'What is a p-value and how do you interpret it?', 'Medium'),
    ('Statistics', 'Explain the Central Limit Theorem and its significance.', 'Hard'),
    ('Statistics', 'What are Type I and Type II errors?', 'Medium'),
    ('Statistics', 'How do you handle outliers in a dataset?', 'Medium'),
    ('Statistics', 'What is the difference between correlation and causation?', 'Easy'),
    ('Statistics', 'Explain bias-variance tradeoff.', 'Hard'),
    ('Statistics', 'What is a normal distribution?', 'Easy'),

    # Machine Learning
    ('Machine Learning', 'What is the difference between supervised, unsupervised, and reinforcement learning?', 'Easy'),
    ('Machine Learning', 'Explain overfitting and underfitting, and how to avoid them.', 'Medium'),
    ('Machine Learning', 'How do you choose which algorithm to use for a dataset?', 'Medium'),
    ('Machine Learning', 'What is cross-validation and why is it important?', 'Medium'),
    ('Machine Learning', 'Explain how a random forest works.', 'Hard'),
    ('Machine Learning', 'What is regularization (L1 and L2) and why is it used?', 'Hard'),
    ('Machine Learning', 'What is a confusion matrix and why is it useful?', 'Medium'),
    ('Machine Learning', 'How do you handle imbalanced datasets?', 'Hard'),
    ('Machine Learning', 'What are the differences between bagging and boosting?', 'Hard'),
    ('Machine Learning', 'Explain logistic regression and its applications.', 'Medium'),
    ('Machine Learning', 'What is dimensionality reduction and what techniques are commonly used?', 'Hard'),

    # Python
    ('Python', 'Write a program that prints numbers ranging from one to 50.', 'Easy'),
    ('Python', 'Write a Python function to find unique elements in a list while preserving order.', 'Medium'),
    ('Python', 'What are the differences between a list and a tuple in Python?', 'Easy'),
    ('Python', 'Explain the difference between `==` and `is` in Python.', 'Medium'),
    ('Python', 'What are decorators in Python and how are they used?', 'Hard')
]

# Connect to the database
conn = sqlite3.connect('interview_questions.db')
c = conn.cursor()

# Insert the questions into the table
c.executemany('INSERT INTO questions (category, question, difficulty) VALUES (?,?,?)', questions)

# Commit the changes and close the connection
conn.commit()
conn.close()

print(f"{len(questions)} questions inserted successfully.")
