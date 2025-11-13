# Data Science Interview Questions Database

A comprehensive system to extract interview questions from PDF books and organize them in a searchable SQLite database.

---

## 📁 Project Structure

```
Data_Science_Interview_Questions/
│
├── Books used/                      # Your PDF books go here
│   ├── Introduction to Data Science.pdf
│   ├── Python for Data Science.pdf
│   └── ... (more PDFs)
│
├── extracted_text/                  # Auto-generated text from PDFs
│   ├── Book_Name_1/
│   │   └── full_text.txt
│   └── Book_Name_2/
│       └── full_text.txt
│
├── interview_questions.db           # SQLite database (created by scripts)
│
├── create_database.py               # Step 1: Creates database schema
├── extract_pdf_content.py           # Step 2: Extracts text from PDFs
├── curate_questions.py              # Step 3: Add questions to database
├── manage_questions.py              # Step 4: View/search questions
│
└── README.md                        # This file!
```

---

## 🚀 Quick Start Guide

### Prerequisites

First, install the required Python libraries:

```bash
# Install PDF extraction library (choose one)
pip install PyPDF2
# OR (pdfplumber is usually better quality)
pip install pdfplumber
```

### Step-by-Step Tutorial

#### **STEP 1: Create the Database**

This creates an empty SQLite database with the proper structure.

```bash
python create_database.py
```

**What this does:**
- Creates `interview_questions.db`
- Sets up two tables: `questions` and `books`
- Creates indexes for fast searching

**You should see:**
```
✓ Database created successfully!
✓ Tables created: 'questions', 'books'
✓ Indexes created for faster searching
```

---

#### **STEP 2: Extract Text from PDFs**

This reads all PDF files in the "Books used" folder and extracts their text.

```bash
python extract_pdf_content.py
```

**What this does:**
- Scans the "Books used" folder for PDFs
- Extracts text from each page
- Saves extracted text to `extracted_text/` folder
- Registers books in the database

**You should see:**
```
[1/5] Processing: Introduction to Data Science.pdf
  Extracting 250 pages...
  Progress: 10/250 pages
  Progress: 20/250 pages
  ...
  ✓ Saved full text to: extracted_text/Introduction_to_Data_Science/full_text.txt
  ✓ Registered book in database
  ✓ Successfully processed 'Introduction to Data Science.pdf'
```

**⏱️ Time estimate:** This can take 1-5 minutes per book depending on size.

---

#### **STEP 3: Curate Questions**

This is where you identify questions from the extracted text and add them to your database.

```bash
python curate_questions.py
```

**What this does:**
- Scans extracted text for potential questions
- Shows you questions interactively
- You decide which ones to add
- Stores questions in the database

**Interactive Menu:**
```
QUESTION CURATION MENU
1. Interactive curation from extracted text
2. Manually add a question
3. View database statistics
4. Exit
```

**Workflow:**

1. **Choose Option 1** (Interactive curation)
2. Select a book to process
3. The tool will find potential questions automatically
4. For each question found, you can:
   - **a** = Add it to database
   - **s** = Skip it
   - **e** = Edit the question before adding
   - **q** = Quit and save progress

**Example interaction:**
```
--- Question 1/25 ---
Question: What is the difference between supervised and unsupervised learning?

Context:
What is the difference between supervised and unsupervised learning?
In supervised learning, the algorithm learns from labeled data...

Action (a=add, s=skip, e=edit, q=quit): a
Category (e.g., Statistics, ML, Python): Machine Learning
Difficulty (Easy/Medium/Hard): Easy
Answer (optional, press Enter to skip): Supervised learning uses labeled data...
Tags (comma-separated, optional): ML, basics
✓ Question added!
```

---

#### **STEP 4: View and Search Questions**

Use the original manage_questions.py script to browse your database.

```bash
python manage_questions.py
```

**Features:**
- View all questions
- Filter by category
- Filter by difficulty
- Add new questions manually

---

## 📊 Database Schema

### Questions Table

| Column         | Type    | Description                              |
|----------------|---------|------------------------------------------|
| id             | INTEGER | Unique identifier (auto-generated)       |
| category       | TEXT    | Category (e.g., "Machine Learning")      |
| subcategory    | TEXT    | Subcategory (optional)                   |
| question       | TEXT    | The interview question                   |
| answer         | TEXT    | The answer (optional)                    |
| difficulty     | TEXT    | Easy, Medium, or Hard                    |
| source_book    | TEXT    | Which book it came from                  |
| page_number    | INTEGER | Page number in the source                |
| tags           | TEXT    | Comma-separated tags                     |
| date_added     | TEXT    | When it was added                        |
| last_modified  | TEXT    | Last update time                         |
| notes          | TEXT    | Additional notes                         |

### Books Table

| Column             | Type    | Description                          |
|--------------------|---------|--------------------------------------|
| id                 | INTEGER | Unique identifier                    |
| title              | TEXT    | Book title                           |
| filename           | TEXT    | PDF filename                         |
| total_pages        | INTEGER | Number of pages                      |
| date_added         | TEXT    | When it was registered               |
| extraction_status  | TEXT    | Status (pending/extracted)           |

---

## 💡 Tips and Best Practices

### 1. **Organizing Your PDFs**
- Keep all PDF books in the "Books used" folder
- Use descriptive filenames
- Remove any corrupted or incomplete PDFs

### 2. **Extraction Tips**
- First extraction may take a while (be patient!)
- Check the `extracted_text/` folder to verify extraction worked
- If extraction fails, try installing `pdfplumber` instead of `PyPDF2`

### 3. **Curation Best Practices**
- Don't rush - quality over quantity!
- Add detailed answers when you find them
- Use consistent category names
- Tag questions with relevant keywords
- Review questions from different books for variety

### 4. **Categories to Consider**
- Python
- Statistics
- Machine Learning
- Data Structures
- SQL/Databases
- Data Visualization
- Math/Linear Algebra
- Big Data/Spark
- Deep Learning
- Business/Domain Knowledge

### 5. **Difficulty Levels**
- **Easy**: Basic definitions, simple concepts
- **Medium**: Requires understanding and application
- **Hard**: Complex scenarios, deep technical knowledge

---

## 🔍 Searching Your Database

You can search your database using SQL queries. Here are some examples:

```python
import sqlite3

conn = sqlite3.connect('interview_questions.db')
cursor = conn.cursor()

# Get all Machine Learning questions
cursor.execute("SELECT * FROM questions WHERE category = 'Machine Learning'")

# Get hard questions only
cursor.execute("SELECT * FROM questions WHERE difficulty = 'Hard'")

# Search for specific topics
cursor.execute("SELECT * FROM questions WHERE question LIKE '%neural network%'")

# Get questions from a specific book
cursor.execute("SELECT * FROM questions WHERE source_book LIKE '%Python%'")

conn.close()
```

---

## 🛠️ Troubleshooting

### Problem: "No module named 'PyPDF2'"
**Solution:**
```bash
pip install PyPDF2
# OR
pip install pdfplumber
```

### Problem: "No PDF files found"
**Solution:**
- Make sure PDFs are in the "Books used" folder
- Check that files have `.pdf` extension (not `.PDF` or `.crdownload`)

### Problem: Extracted text is gibberish
**Solution:**
- Some PDFs have encrypted or image-based text
- Try using `pdfplumber` instead of `PyPDF2`
- For scanned books, you may need OCR (Optical Character Recognition)

### Problem: No questions found automatically
**Solution:**
- The auto-detection is pattern-based and may miss questions
- Use Option 2 in curate_questions.py to manually add questions
- Review the extracted text files manually

---

## 📈 Workflow Summary

```
1. Put PDFs in "Books used/" folder
        ↓
2. Run create_database.py
        ↓
3. Run extract_pdf_content.py
        ↓
4. Check extracted_text/ folder
        ↓
5. Run curate_questions.py
        ↓
6. Add questions interactively
        ↓
7. Use manage_questions.py to review
        ↓
8. Study for your interviews! 🎯
```

---

## 🎯 Your Project Goal

**Objective:** Build a comprehensive database of data science interview questions to help you prepare for interviews.

**Why this approach?**
- ✅ Questions are organized and searchable
- ✅ You can filter by topic and difficulty
- ✅ Answers are stored alongside questions
- ✅ You know the source of each question
- ✅ Easy to add more questions over time
- ✅ Can export to CSV or other formats later

---

## 📝 Next Steps

1. ✅ Create the database
2. ✅ Extract text from your PDFs
3. ✅ Start curating questions
4. Build a study plan based on categories
5. Export questions to flashcards or quizzes
6. Track which questions you've mastered

---

## 🤝 Need Help?

If something isn't working:
1. Read the error message carefully
2. Check the Troubleshooting section
3. Make sure all prerequisites are installed
4. Verify your PDF files are readable

---

## 📚 Books You Currently Have

```
1. A Mathematical Introduction to Data Science.pdf
2. An Introduction to Statistics and Machine Learning.pdf
3. Data Science- Foundations and Hands-on Experience Handling Economic, Spatial, and Multidimensional Data with R.pdf
4. Introduction to Data Science.pdf
5. Python for Data Science.pdf
```

**Total pages to extract:** ~1500+ pages of content!

---

Good luck with your interview preparation! 🚀
