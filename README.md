# AI Interview Coach for Data Science Jobs

Personalized interview practice with **396 real interview questions** and AI-powered answers from 10 textbooks.

---

## 🚀 Quick Start

1. **Upload Database to Supabase:**
   - See **[UPLOAD_READY.md](UPLOAD_READY.md)** for 3-step guide
   - Takes ~10 minutes

2. **Open the App:**
   - Open `index.html` in your browser
   - No server needed!

---

## 📊 What You Get

### 396 Interview Questions
- **ML:** 108 questions (27%)
- **Mixed/General:** 109 questions (28%)
- **Stats:** 61 questions (15%)
- **Case Studies:** 61 questions (15%)
- **Coding:** 28 questions (7%)
- **SQL:** 22 questions (6%)
- **Behavioral:** 5 questions (1%)

### 10 Data Science Textbooks
- 3,983 pages with tables extracted
- Statistics, ML, Probability coverage
- 7.6 MB database

---

## 🎯 Features

- ✅ **Personalized Questions** - Based on experience level & target company
- ✅ **Interview Types** - Coding, ML, Stats, Case Studies, Behavioral
- ✅ **AI Answers** - From textbooks using RAG
- ✅ **Dark/Light Mode** - Clean, modern UI
- ✅ **Profile System** - Track weak areas & interview countdown

---

## 📁 Project Structure

```
├── supabase/                      ← Everything to upload
│   ├── 01_create_documents_table.sql
│   ├── 02_create_questions_table.sql
│   ├── 03_verify_upload.sql
│   ├── documents_data.csv         (7.6 MB - textbooks)
│   ├── interview_questions_data.csv (238 KB - questions)
│   └── README.md                  (Upload guide)
│
├── index.html                     ← Open this in browser
├── config.js                      ← Add your Groq API key
│
├── UPLOAD_READY.md               ← Start here!
├── START_HERE.md                 ← Full project guide
└── THE ROADMAP.md                ← Development plan
```

---

## 🎨 UI Features

- Clean, modern design
- Responsive (works on mobile)
- Question accordion (expand/collapse)
- Profile setup wizard
- Interview countdown timer

---

## 🛠️ Tech Stack

- **Frontend:** Vanilla HTML/CSS/JavaScript
- **AI:** Groq API (llama-3.3-70b)
- **Database:** Supabase (PostgreSQL)
- **RAG:** Keyword extraction + relevance scoring

---

## 📚 Documentation

- **[UPLOAD_READY.md](UPLOAD_READY.md)** - How to upload database
- **[START_HERE.md](START_HERE.md)** - Complete project guide
- **[THE ROADMAP.md](THE ROADMAP.md)** - Development roadmap
- **[supabase/README.md](supabase/README.md)** - Detailed upload steps

---

## ✨ Quick Stats

- **Questions:** 396 (9 sources, deduplicated)
- **Textbooks:** 10 books, 3,983 pages
- **Coverage:** All major DS interview areas
- **Setup Time:** ~10 minutes
- **Storage:** ~7.8 MB

---

Built to help you ace data science interviews! 🚀
