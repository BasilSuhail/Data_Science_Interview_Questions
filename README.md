# Data Science Interview Questions - Semantic Search

Search through data science books using AI-powered semantic search.

## 🚀 Quick Start

### What You Need
1. `SIMPLE_SUPABASE.sql` - Database setup
2. `simple_upload.py` - Upload data
3. `simple_search.html` - Search interface

### Instructions
**Read:** [SIMPLE_INSTRUCTIONS.md](SIMPLE_INSTRUCTIONS.md)

**3 Steps:**
1. Setup Supabase (5 min)
2. Upload data (10 min)
3. Use search (1 min)

That's it!

---

## 📁 Files in This Project

```
.
├── Books used/              # Your 5 PDF books
├── extracted_text/          # Extracted text (auto-generated)
├── extract_pdf_content.py   # Run first to extract PDFs
│
├── SIMPLE_SUPABASE.sql      # ⭐ Supabase database setup
├── simple_upload.py         # ⭐ Upload to Supabase
├── simple_search.html       # ⭐ Search interface
│
├── SIMPLE_INSTRUCTIONS.md   # 📖 Read this!
└── README.md                # This file
```

---

## 💡 What This Does

1. **Extract** text from PDF books
2. **Convert** text into vector embeddings (AI)
3. **Store** in Supabase database
4. **Search** using semantic similarity (finds related content, not just keywords)

---

## 🎯 Example Searches

- "What is machine learning?"
- "Explain neural networks"
- "How to handle missing data?"
- "Python data structures"

Finds relevant content even if exact words don't match!

---

## 📚 Books Included

1. Introduction to Data Science
2. Python for Data Science
3. A Mathematical Introduction to Data Science
4. An Introduction to Statistics and Machine Learning
5. Data Science: Foundations and Hands-on Experience

---

## 🆘 Problems?

Check [SIMPLE_INSTRUCTIONS.md](SIMPLE_INSTRUCTIONS.md) → Troubleshooting section

---

Built with Supabase + pgvector 🚀
