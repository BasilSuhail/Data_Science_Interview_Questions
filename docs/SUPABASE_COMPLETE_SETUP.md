# 📤 Complete Supabase Setup Guide

**Everything you need to set up both databases for your AI Interview Coach.**

---

## 🎯 Quick Overview

Your app needs **2 Supabase tables:**

| Table | Purpose | File to Upload | Size |
|-------|---------|----------------|------|
| `documents` | Textbook content for AI answers | `supabase_dataset.csv` | 7.6 MB |
| `interview_questions` | Interview questions | `final_interview_questions.csv` | 161 KB |

**Total time:** ~10 minutes
**Total storage:** ~7.8 MB (free tier: 500 MB)

---

## 📋 PART 1: Upload Textbooks (`documents` table)

### Step 1: Create the Documents Table

1. Go to your Supabase Dashboard: https://iteavenjozhzxupbxosu.supabase.co
2. Click **SQL Editor** in sidebar
3. Click **New Query**
4. Paste this SQL:

```sql
-- Create documents table for textbook content
CREATE TABLE IF NOT EXISTS documents (
    id BIGSERIAL PRIMARY KEY,
    book_name TEXT NOT NULL,
    page_number INTEGER,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for faster text searches
CREATE INDEX IF NOT EXISTS idx_documents_content
ON documents USING gin(to_tsvector('english', content));

-- Create index for book filtering
CREATE INDEX IF NOT EXISTS idx_documents_book ON documents(book_name);
```

5. Click **Run** (or press F5)
6. You should see: "Success. No rows returned"

### Step 2: Upload Textbook Data

1. Go to **Table Editor** in sidebar
2. Find the **`documents`** table
3. Click the table to open it
4. Click **Insert** dropdown → **Import data from CSV**
5. Click **Browse** and select: `supabase_dataset.csv`
6. In the mapping screen:
   - Uncheck `id` (auto-generated)
   - Uncheck `created_at` (auto-generated)
   - Make sure these are checked:
     - ✅ `book_name`
     - ✅ `page_number`
     - ✅ `content`
7. Click **Import Data**
8. **Wait 1-2 minutes** for upload to complete

### Step 3: Verify Textbook Upload

Go to **SQL Editor** and run:

```sql
SELECT
    book_name,
    COUNT(*) as page_count
FROM documents
GROUP BY book_name
ORDER BY page_count DESC;
```

**Expected:** 10 books with ~3,983 total pages

---

## 📋 PART 2: Upload Questions (`interview_questions` table)

### Step 1: Create the Interview Questions Table

1. Go to **SQL Editor**
2. Click **New Query**
3. Paste this SQL:

```sql
-- Create interview_questions table
CREATE TABLE IF NOT EXISTS interview_questions (
    id BIGSERIAL PRIMARY KEY,
    question_text TEXT NOT NULL,
    company TEXT,
    difficulty TEXT,
    question_type TEXT,
    topics TEXT,
    source TEXT,
    answer_text TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for faster filtering
CREATE INDEX IF NOT EXISTS idx_questions_difficulty ON interview_questions(difficulty);
CREATE INDEX IF NOT EXISTS idx_questions_type ON interview_questions(question_type);
CREATE INDEX IF NOT EXISTS idx_questions_company ON interview_questions(company);
CREATE INDEX IF NOT EXISTS idx_questions_search
ON interview_questions USING gin(to_tsvector('english', question_text));
```

4. Click **Run**
5. You should see: "Success. No rows returned"

### Step 2: Upload Interview Questions

1. Go to **Table Editor**
2. Find the **`interview_questions`** table
3. Click the table to open it
4. Click **Insert** → **Import data from CSV**
5. Click **Browse** and select: `collected_questions/final_interview_questions.csv`
6. In the mapping screen:
   - Uncheck `id` (auto-generated)
   - Make sure these are checked:
     - ✅ `question_text`
     - ✅ `company`
     - ✅ `difficulty`
     - ✅ `question_type`
     - ✅ `topics`
     - ✅ `source`
     - ✅ `answer_text`
     - ✅ `created_at`
7. Click **Import Data**
8. **Wait ~10 seconds** for upload

### Step 3: Verify Questions Upload

Go to **SQL Editor** and run:

```sql
SELECT
    question_type,
    difficulty,
    COUNT(*) as count
FROM interview_questions
GROUP BY question_type, difficulty
ORDER BY count DESC;
```

**Expected:** 234 total questions across different types and difficulties

---

## 🔍 Testing Your Setup

### Test 1: Check Total Counts

```sql
-- Should return ~3,983
SELECT COUNT(*) as textbook_pages FROM documents;

-- Should return 234
SELECT COUNT(*) as total_questions FROM interview_questions;
```

### Test 2: Search Textbooks

```sql
-- Find pages about "regression"
SELECT book_name, page_number, LEFT(content, 100) as preview
FROM documents
WHERE content ILIKE '%regression%'
LIMIT 5;
```

### Test 3: Filter Questions

```sql
-- Get medium difficulty ML questions
SELECT question_text, source
FROM interview_questions
WHERE difficulty = 'medium'
  AND question_type = 'ml'
LIMIT 5;
```

### Test 4: Get Questions by Category

```sql
-- Count questions by type
SELECT
    question_type,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) as percentage
FROM interview_questions
GROUP BY question_type
ORDER BY count DESC;
```

---

## 🔐 Security Settings (Important!)

### Disable RLS for Public Read Access

Your app uses the anon key for read-only access, so RLS should be **disabled**:

1. Go to **Table Editor**
2. Click on **`documents`** table
3. Look for "RLS" toggle in top right
4. Make sure it's **OFF** (gray)
5. Repeat for **`interview_questions`** table

**Why?** With RLS enabled, the anon key can't read data. Since this is public educational content, we keep it open.

---

## 📊 Data Overview

### Documents Table Structure:
```
documents
├── id (auto)
├── book_name (e.g., "Introduction to Statistical Learning")
├── page_number (e.g., 42)
├── content (page text with tables as markdown)
└── created_at (auto)
```

**Contains:**
- 10 textbooks
- ~3,983 pages
- Tables formatted as markdown
- Enhanced with pdfplumber extraction

### Interview Questions Table Structure:
```
interview_questions
├── id (auto)
├── question_text (e.g., "What is gradient descent?")
├── company (e.g., "Meta", or empty)
├── difficulty (easy/medium/hard)
├── question_type (coding/stats/ml/case/behavioral/mixed)
├── topics (e.g., "probability")
├── source (e.g., "kojino/120-DS-Questions")
├── answer_text (brief answer if available)
└── created_at (auto)
```

**Contains:**
- 234 unique questions
- 6 different sources
- 7 question types
- 3 difficulty levels

---

## 🐛 Troubleshooting

### Issue: "Relation already exists"
**Cause:** Table was already created
**Solution:** Skip the CREATE TABLE step, or add `IF NOT EXISTS` to the query

### Issue: CSV Import Fails
**Solutions:**
- Make sure you're selecting the correct file
- Check that column names in CSV match table columns
- Try refreshing the page and importing again
- If file is too large, contact Supabase support

### Issue: "permission denied for table"
**Cause:** RLS is enabled
**Solution:** Disable RLS in Table Editor (see Security Settings above)

### Issue: Queries are Slow
**Solutions:**
- Make sure indexes are created (run the CREATE INDEX commands)
- Use `LIMIT` in queries
- Check that you're not accidentally doing full table scans

### Issue: Special Characters Look Weird
**Cause:** Encoding issue
**Solution:** CSVs are UTF-8 encoded - make sure your editor uses UTF-8

---

## ✅ Final Checklist

After completing setup, verify:

- [ ] `documents` table exists with ~3,983 rows
- [ ] `interview_questions` table exists with 234 rows
- [ ] Both tables have RLS **disabled**
- [ ] Indexes are created on both tables
- [ ] Can query both tables successfully
- [ ] Text search works on `documents` (test with regression query)
- [ ] Filtering works on `interview_questions` (test by difficulty)

---

## 📱 What's Next?

After uploading both databases:

1. ✅ Your app can now:
   - Fetch interview questions from `interview_questions`
   - Generate AI answers from `documents`
   - Combine both for complete coaching experience

2. 🎯 Test in your app:
   - Generate interview questions
   - Ask for answers and verify they use textbook content
   - Filter questions by difficulty/type

3. 🚀 Optional enhancements:
   - Add more SQL questions via StrataScratch
   - Add company-specific filters
   - Implement progress tracking

---

## 📁 Files Location

Make sure you're uploading the correct files:

| File | Location | Description |
|------|----------|-------------|
| `supabase_dataset.csv` | Root folder | 10 textbooks, 3,983 pages |
| `final_interview_questions.csv` | `collected_questions/` | 234 interview questions |

---

## 💡 Pro Tips

1. **Backup before uploading:** Supabase auto-backs up, but keep local copies
2. **Test queries first:** Use SQL Editor before connecting app
3. **Monitor usage:** Check Supabase dashboard → Database → Usage
4. **Free tier limits:** 500 MB storage, 50 MB max file upload
5. **Optimize queries:** Always use indexes and LIMIT clauses

---

## 🔗 Quick Links

- **Supabase Dashboard:** https://iteavenjozhzxupbxosu.supabase.co
- **Table Editor:** Dashboard → Table Editor
- **SQL Editor:** Dashboard → SQL Editor
- **Database Settings:** Dashboard → Database → Tables

---

## 📞 Need Help?

**Common resources:**
- Supabase Docs: https://supabase.com/docs
- SQL Tutorial: https://www.postgresql.org/docs/current/tutorial.html
- Your project docs: Check `/docs` folder

---

## ✨ Summary

**What you just set up:**
1. ✅ `documents` table with 10 textbooks (7.6 MB)
2. ✅ `interview_questions` table with 234 questions (161 KB)
3. ✅ Indexes for fast querying
4. ✅ Public read access for your app

**Your AI Interview Coach is now fully powered!** 🚀
