# Data Science Search - Intelligent Q&A System

Search through data science books with natural language questions and get smart, composed answers.

---

## 🚀 How to Run the App

### Step 1: Open the Search Page

1. Open `simple_search.html` in any web browser
2. That's it! The app will load and connect to the database

**Note:** Make sure you have internet connection (the app connects to Supabase)

---

## 📚 How to Add More Books

Want to add more PDF books to your search database? Follow these simple steps:

### Step 1: Install Required Package

```bash
pip install PyPDF2
```

### Step 2: Add Your PDF Books

Put your new PDF files in the `Books used/` folder

### Step 3: Generate CSV File

Run the extraction script:

```bash
python add_more_books.py
```

This will:
- Read all PDFs from "Books used" folder
- Extract text from each page
- Create a file called `new_books_data.csv`

### Step 4: Upload to Supabase

1. Go to your Supabase dashboard (https://supabase.com)
2. Click **Table Editor** → **documents** table
3. Click **Insert** → **Import data from CSV**
4. Select the `new_books_data.csv` file
5. Click **Import**

**Done!** Your new books are now searchable in the app!

---

## 💡 Features

- **Natural Language Search**: Ask questions like "what is python" or "explain machine learning"
- **Smart Answer Composition**: Gets coherent, readable answers instead of raw text chunks
- **Source Citations**: Shows which books the answer came from
- **Clean PDF Text Processing**: Automatically removes artifacts and formatting issues

---

## 📁 Files in This Project

```
.
├── simple_search.html       # Main search interface (open this!)
├── add_more_books.py        # Script to add new books
├── supabase_data.csv        # Current data (already uploaded)
├── Books used/              # Put your PDF books here
└── README.md                # This file
```

---

## 🔍 Example Searches

Try asking:
- "what is machine learning"
- "explain neural networks"
- "how does regression work"
- "what is Python used for"
- "define overfitting"

The app will extract keywords, search the database, and compose a clear answer with sources!

---

## 📊 Current Database

- **Books**: 6 data science books
- **Total chunks**: 2,343 searchable pieces
- **Topics**: Machine Learning, Statistics, Python, Math, Data Science

---

Built with Supabase & Intelligence 🚀
