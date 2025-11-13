# Visual Workflow Guide

## Your Current Folder Structure

```
Data_Science_Interview_Questions/
│
├── Books used/                          [Your 5 PDF books are here]
│   ├── Introduction to Data Science.pdf
│   ├── Python for Data Science.pdf
│   ├── A Mathematical Introduction to Data Science.pdf
│   ├── An Introduction to Statistics and Machine Learning.pdf
│   └── Data Science- Foundations and Hands-on Experience.pdf
│
├── QUICK_START.md                       [Start here! 5-min guide]
├── README.md                            [Full documentation]
├── WORKFLOW.md                          [This file!]
│
├── create_database.py                   [Script 1: Creates database]
├── extract_pdf_content.py               [Script 2: Extracts PDFs]
├── curate_questions.py                  [Script 3: Add questions]
└── manage_questions.py                  [Script 4: View/search]
```

---

## Complete Workflow (Step-by-Step)

### Before Starting

```bash
# Install required library
pip install pdfplumber
```

---

### STEP 1: Create Database

**Command:**
```bash
python create_database.py
```

**What happens:**
```
Your Folder
│
├── Books used/
├── Scripts...
│
└── interview_questions.db ← NEW! Empty database created
```

**Output:**
```
✓ Database created successfully!
✓ Tables created: 'questions', 'books'
```

---

### STEP 2: Extract PDF Content

**Command:**
```bash
python extract_pdf_content.py
```

**What happens:**
```
Your Folder
│
├── Books used/
│   └── [PDFs are read]
│
├── extracted_text/ ← NEW FOLDER!
│   ├── Introduction_to_Data_Science/
│   │   └── full_text.txt (all text from book)
│   │
│   ├── Python_for_Data_Science/
│   │   └── full_text.txt
│   │
│   └── ... (one folder per book)
│
└── interview_questions.db (books registered here)
```

**Output:**
```
[1/5] Processing: Introduction to Data Science.pdf
  Extracting 250 pages...
  Progress: 10/250 pages
  Progress: 20/250 pages
  ...
  ✓ Saved full text to: extracted_text/Introduction_to_Data_Science/full_text.txt
  ✓ Registered book in database
```

**Time:** 2-5 minutes (depends on PDF size)

---

### STEP 3: Curate Questions

**Command:**
```bash
python curate_questions.py
```

**What happens:**

```
QUESTION CURATION MENU
1. Interactive curation from extracted text
2. Manually add a question
3. View database statistics
4. Exit

Select an option: 1

Available books:
  1. Introduction_to_Data_Science
  2. Python_for_Data_Science
  3. ... (all books)

Select a book: 1

Found 25 potential questions!

--- Question 1/25 ---
Question: What is the difference between supervised and unsupervised learning?

Context:
What is the difference between supervised and unsupervised learning?
In supervised learning, the algorithm learns from labeled data...

Action (a=add, s=skip, e=edit, q=quit): a
Category: Machine Learning
Difficulty: Easy
Answer: Supervised learning uses labeled data with known outcomes...
Tags: ML, basics

✓ Question added!
```

**What goes into database:**
```
questions table
├── ID: 1
├── Category: Machine Learning
├── Question: What is the difference between...
├── Answer: Supervised learning uses...
├── Difficulty: Easy
├── Source Book: Introduction_to_Data_Science
├── Tags: ML, basics
└── Date Added: 2025-11-13
```

---

### STEP 4: View/Search Questions

**Command:**
```bash
python manage_questions.py
```

**Menu Options:**
```
1. View all questions          → See everything
2. View question details       → See full info for one question
3. Filter by category          → Only ML questions, only Python, etc.
4. Filter by difficulty        → Only Easy/Medium/Hard
5. Search questions            → Search by keyword
6. Show statistics             → How many questions per category?
7. Export to CSV               → Save questions to CSV file
8. Exit
```

**Example - View Statistics:**
```
DATABASE STATISTICS

Total Questions: 127
Questions with Answers: 98 (77%)

By Category:
  Machine Learning: 45
  Python: 32
  Statistics: 28
  SQL: 15
  Data Visualization: 7

By Difficulty:
  Easy: 42
  Medium: 63
  Hard: 22

By Source:
  Introduction_to_Data_Science: 35
  Python_for_Data_Science: 28
  ...
```

---

## The Complete Cycle

```
┌─────────────────────────────────────────────────────────┐
│  START: You have PDF books                              │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 1: python create_database.py                      │
│  → Creates empty database                               │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 2: python extract_pdf_content.py                  │
│  → Reads PDFs, extracts text to extracted_text/         │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 3: python curate_questions.py                     │
│  → You review extracted text and add questions          │
│  → Questions saved to database with answers             │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 4: python manage_questions.py                     │
│  → Browse, search, filter your questions                │
│  → Export to CSV if needed                              │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  GOAL ACHIEVED: Study for interviews! 🎯                │
└─────────────────────────────────────────────────────────┘
```

---

## Your Next Actions

1. **Right now:** Open terminal in this folder
2. **Run:** `pip install pdfplumber`
3. **Run:** `python create_database.py`
4. **Run:** `python extract_pdf_content.py`
5. **Wait:** 2-5 minutes for extraction
6. **Run:** `python curate_questions.py`
7. **Start:** Adding questions to your database!

---

## Tips for Success

**For Extraction (Step 2):**
- Let it run completely, don't interrupt
- Check `extracted_text/` folder to verify it worked
- Each book gets its own folder with `full_text.txt`

**For Curation (Step 3):**
- Start with one book, don't rush
- Quality over quantity!
- Add answers when you find them
- Use consistent category names
- Tag questions for easy searching later

**For Daily Use:**
- Use `manage_questions.py` to review questions
- Filter by category to focus on weak areas
- Export to CSV for flashcard apps
- Keep adding questions as you study

---

## Database Schema Quick Reference

**What gets stored for each question:**
- ✓ The question text
- ✓ The answer (if you add it)
- ✓ Category (Python, ML, Stats, etc.)
- ✓ Difficulty (Easy/Medium/Hard)
- ✓ Source book name
- ✓ Page number (if available)
- ✓ Tags for searching
- ✓ When it was added
- ✓ Your personal notes

---

## Troubleshooting Quick Reference

| Problem | Solution |
|---------|----------|
| "No module named 'pdfplumber'" | `pip install pdfplumber` |
| "No PDF files found" | Check PDFs are in "Books used/" folder |
| Extracted text is gibberish | Try different PDF or use OCR |
| No questions found | Use manual entry (option 2) |

---

Good luck building your interview question database! 🚀