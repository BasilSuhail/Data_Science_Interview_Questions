# 🗄️ Supabase Database Setup

**Everything you need to set up your AI Interview Coach database.**

---

## 📁 Files in This Folder

| File | Purpose |
|------|---------|
| `01_create_documents_table.sql` | Creates table for textbooks |
| `02_create_questions_table.sql` | Creates table for interview questions |
| `03_verify_upload.sql` | Verification queries after upload |
| `documents_data.csv` | Textbook content (7.6 MB, 3,983 pages) |
| `interview_questions_data.csv` | Interview questions (266 KB, 552 questions) |

---

## 🚀 Quick Setup (3 Steps)

### STEP 1: Create Tables

1. Go to your Supabase Dashboard: https://iteavenjozhzxupbxosu.supabase.co
2. Click **SQL Editor** in the sidebar
3. Run these SQL files **in order:**
   - First: `01_create_documents_table.sql`
   - Then: `02_create_questions_table.sql`

**How to run:**
- Click **New Query**
- Copy the entire contents of the SQL file
- Paste into the query editor
- Click **Run** (or press F5)
- You should see: "Success. No rows returned"

---

### STEP 2: Upload Data

#### Upload Documents (Textbooks):

1. Go to **Table Editor** in sidebar
2. Click on the **`documents`** table
3. Click **Insert** dropdown → **Import data from CSV**
4. Upload file: `documents_data.csv`
5. In the column mapping:
   - ❌ Uncheck `id` (auto-generated)
   - ❌ Uncheck `created_at` (auto-generated)
   - ✅ Check: `book_name`, `page_number`, `content`
6. Click **Import Data**
7. Wait 1-2 minutes for upload

#### Upload Questions:

1. Still in **Table Editor**
2. Click on the **`interview_questions`** table
3. Click **Insert** → **Import data from CSV**
4. Upload file: `interview_questions_data.csv`
5. In the column mapping:
   - ❌ Uncheck `id` (auto-generated)
   - ✅ Check all other columns:
     - `question_text`
     - `company`
     - `difficulty`
     - `question_type`
     - `topics`
     - `source`
     - `answer_text`
     - `created_at`
6. Click **Import Data**
7. Wait ~10 seconds

---

### STEP 3: Verify Upload

1. Go to **SQL Editor**
2. Open `03_verify_upload.sql`
3. Run the queries to verify:
   - Documents: ~3,983 rows
   - Questions: 552 rows
   - Indexes are working
   - Text search works

---

## ✅ Expected Results

### Documents Table:
- **Total Pages:** ~3,983
- **Books:** 10 textbooks
- **Size:** ~7.6 MB

**Books included:**
1. Introduction to Statistical Learning
2. OpenIntro Statistics
3. Think Stats
4. And 7 more data science books

---

### Interview Questions Table:
- **Total Questions:** 552
- **Sources:** 11 different repositories
- **Size:** 266 KB
- **Duplicates Removed:** 130 (from 682 total)

**Breakdown:**
- **By Type:**
  - ML: 264 (48%)
  - Mixed: 109 (20%)
  - Stats: 61 (11%)
  - Case Studies: 61 (11%)
  - Coding: 28 (5%)
  - SQL: 22 (4%)
  - Behavioral: 5 (1%)
  - Other: 2 (<1%)

- **By Difficulty:**
  - Medium: 309 (56%)
  - Hard: 189 (34%)
  - Easy: 52 (9%)
  - Multi-level: 2 (<1%)

- **By Source:**
  - Sandy1811/DS-Interview-FAANG: 156 (28%)
  - kojino/120-DS-Questions: 115 (21%)
  - DS_Interview_Notebook: 96 (17%)
  - 165_ML_Interview_QA: 46 (8%)
  - And 7 more sources

---

## 🔐 Security Settings

**IMPORTANT:** Disable Row Level Security (RLS) for public read access

1. Go to **Table Editor**
2. Click on **`documents`** table
3. Look for "RLS" toggle in top right
4. Make sure it's **OFF** (grayed out)
5. Repeat for **`interview_questions`** table

**Why?** Your app uses the anon key for read-only public access to educational content.

---

## 🔍 Test Queries

After uploading, test in SQL Editor:

### Test 1: Count Rows
```sql
SELECT COUNT(*) FROM documents;        -- Should be ~3,983
SELECT COUNT(*) FROM interview_questions;  -- Should be 552
```

### Test 2: Search Textbooks
```sql
-- Find pages about "gradient descent"
SELECT book_name, page_number, LEFT(content, 100) as preview
FROM documents
WHERE content ILIKE '%gradient descent%'
LIMIT 5;
```

### Test 3: Filter Questions
```sql
-- Get hard ML questions
SELECT question_text, source
FROM interview_questions
WHERE difficulty = 'hard' AND question_type = 'ml'
LIMIT 5;
```

---

## 🐛 Troubleshooting

### Error: "relation already exists"
**Solution:** Table was already created. Skip that SQL file.

### Error: "syntax error near ```"
**Solution:** Don't copy the markdown code blocks (```). Only copy the SQL commands between them.

### Error: CSV import fails
**Solutions:**
1. Make sure you selected the correct file
2. Check column mappings match the table
3. Refresh page and try again

### Error: "permission denied"
**Solution:** Disable RLS (see Security Settings above)

### Queries are slow
**Solution:** Make sure indexes were created (run the CREATE INDEX commands)

---

## 📊 Database Schema

### `documents` Table:
```
documents
├── id              BIGSERIAL PRIMARY KEY
├── book_name       TEXT NOT NULL
├── page_number     INTEGER
├── content         TEXT NOT NULL
└── created_at      TIMESTAMPTZ DEFAULT NOW()
```

**Indexes:**
- `idx_documents_content` (GIN text search)
- `idx_documents_book` (book filtering)
- `idx_documents_page` (page lookup)

---

### `interview_questions` Table:
```
interview_questions
├── id              BIGSERIAL PRIMARY KEY
├── question_text   TEXT NOT NULL
├── company         TEXT
├── difficulty      TEXT
├── question_type   TEXT
├── topics          TEXT
├── source          TEXT
├── answer_text     TEXT
└── created_at      TIMESTAMPTZ DEFAULT NOW()
```

**Indexes:**
- `idx_questions_difficulty` (filter by difficulty)
- `idx_questions_type` (filter by type)
- `idx_questions_company` (filter by company)
- `idx_questions_topics` (filter by topics)
- `idx_questions_search` (GIN text search)

---

## 💡 Pro Tips

1. **Run SQL files in order** (01, 02, 03)
2. **Test each step** before moving to next
3. **Use SQL Editor** for quick verification
4. **Monitor upload progress** in Supabase UI
5. **Keep these files** for future reference or re-setup

---

## 📱 After Setup

Once both tables are uploaded, your app can:

1. **Fetch interview questions:**
   - Filter by difficulty, type, company
   - Personalize based on user profile
   - Generate practice sets

2. **Generate AI answers:**
   - Search textbook content
   - Use RAG with Groq API
   - Cite sources from books

3. **Combine both:**
   - Ask question → Get textbook-based answer
   - Complete interview coaching experience

---

## 🔗 Quick Links

- **Supabase Dashboard:** https://iteavenjozhzxupbxosu.supabase.co
- **Table Editor:** Dashboard → Table Editor
- **SQL Editor:** Dashboard → SQL Editor
- **Database Settings:** Dashboard → Database

---

## ✨ Summary

**Total Setup Time:** ~10 minutes
**Total Storage Used:** ~7.8 MB
**Free Tier Limit:** 500 MB (you're using 1.5%)

**You'll have:**
- ✅ 3,983 textbook pages for AI answers
- ✅ 552 interview questions (130 duplicates removed!)
- ✅ Fast indexed searches
- ✅ Public read access for your app

**Your AI Interview Coach is ready to launch!** 🚀
