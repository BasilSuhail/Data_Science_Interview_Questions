# Quick Start Guide - 5 Minutes to Get Started!

## What You Need to Do Right Now

### Step 1: Install Dependencies (1 minute)

Open your terminal and run:

```bash
pip install pdfplumber
```

### Step 2: Create the Database (5 seconds)

```bash
python create_database.py
```

You should see:
```
✓ Database created successfully!
✓ Tables created: 'questions', 'books'
✓ Indexes created for faster searching
```

### Step 3: Extract Text from Your PDFs (2-5 minutes)

```bash
python extract_pdf_content.py
```

This will read all your PDF books and extract their text. Grab a coffee - this takes a few minutes!

### Step 4: Start Adding Questions (ongoing)

```bash
python curate_questions.py
```

Choose option 1 (Interactive curation), select a book, and start adding questions!

---

## What Each File Does

| File | What It Does |
|------|--------------|
| **create_database.py** | Creates the SQLite database |
| **extract_pdf_content.py** | Reads PDFs and extracts text |
| **curate_questions.py** | Helps you add questions to database |
| **manage_questions.py** | Browse and search your questions |
| **README.md** | Full documentation (read this!) |

---

## Your PDF Books

You have **5 PDF books** with 1500+ pages:
1. A Mathematical Introduction to Data Science
2. An Introduction to Statistics and Machine Learning
3. Data Science- Foundations and Hands-on Experience
4. Introduction to Data Science
5. Python for Data Science

---

## Quick Commands Cheat Sheet

```bash
# Create database
python create_database.py

# Extract PDFs
python extract_pdf_content.py

# Add questions
python curate_questions.py

# View/search questions
python manage_questions.py
```

---

## Need More Help?

Read the full [README.md](README.md) for detailed instructions!

---

Start with Step 1 above and you'll be adding questions in 5 minutes!
