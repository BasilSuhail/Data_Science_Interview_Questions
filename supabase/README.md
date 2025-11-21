# Supabase Database Setup

This folder contains everything you need to upload to Supabase.

---

## 📂 Files in This Folder

1. **README.md** ← You are here
2. **documents_data.csv** (7.6 MB) ← 10 textbooks, 3,983 pages
3. **interview_questions.csv** (536 KB) ← 1,726 interview questions
4. **setup.sql** (10 KB) ← SQL schema for all tables

---

## 🚀 Quick Setup (10 minutes)

### Step 1: Create Tables (2 minutes)

1. Go to https://supabase.com → Open your project
2. Click **SQL Editor** in left sidebar
3. Click **New Query**
4. Open `setup.sql` in this folder
5. **Copy the entire file** (all 400+ lines)
6. **Paste into Supabase SQL Editor**
7. Click **RUN** (or press Cmd/Ctrl + Enter)
8. Wait ~10 seconds
9. You should see: ✅ **Success. No rows returned**

**This creates 5 tables:**
- `documents` (textbooks)
- `interview_questions` (questions)
- `user_profiles` (user data)
- `user_answers` (performance tracking)
- `mock_interviews` (Phase 3)

---

### Step 2: Upload Documents (3 minutes)

1. Go to **Table Editor** → Click **documents** table
2. Click **Insert** dropdown → **Import data from CSV**
3. Select: `documents_data.csv`
4. Map columns (should auto-map)
5. Click **Import**
6. Wait ~2 minutes (7.6 MB file)
7. ✅ Verify: ~3,983 rows

---

### Step 3: Upload Questions (3 minutes)

1. Go to **Table Editor** → Click **interview_questions** table
2. Click **Insert** → **Import data from CSV**
3. Select: `interview_questions.csv`
4. Map columns:
   - question_text → question_text
   - company → company
   - difficulty → difficulty
   - question_type → question_type
   - topics → topics
   - source → source
   - answer_text → answer_text
   - created_at → created_at
5. Click **Import**
6. Wait ~2 minutes
7. ✅ Verify: ~1,726 rows

---

### Step 4: Verify (2 minutes)

Run in **SQL Editor**:

```sql
-- Check documents
SELECT COUNT(*) FROM documents;
-- Should return: ~3983

-- Check questions
SELECT COUNT(*) FROM interview_questions;
-- Should return: ~1726

-- Check breakdown
SELECT question_type, COUNT(*)
FROM interview_questions
GROUP BY question_type
ORDER BY COUNT(*) DESC;
```

---

## 📊 What You're Uploading

### Documents (7.6 MB)
- 10 data science textbooks
- 3,983 pages
- For AI-powered answers (RAG)

### Questions (536 KB)
- 1,726 interview questions
- Sources: GitHub (446), Reddit (728), Your collections (552)
- Tagged by company, difficulty, type

**Breakdown:**
- **By Type:** mixed (936), ml (429), coding (129), stats (103), case (94)
- **By Difficulty:** medium (1,483), hard (189), easy (52)

---

## ✅ Done!

Open `interview-coach-app.html` → Start practicing!

---

## 🐛 Troubleshooting

**CSV import fails:** File too large → Split CSV in half, upload separately

**Table not found:** Run `setup.sql` first

**Permission denied:** Disable RLS temporarily:
```sql
ALTER TABLE interview_questions DISABLE ROW LEVEL SECURITY;
```

---

**Need detailed instructions?** See `docs/PHASE_2_UPLOAD_INSTRUCTIONS.md`
