# 🚀 PHASE 2: Database Upload Instructions

## What You Have Now

✅ **1,726 interview questions** ready to upload (merged from your 900 + 1,174 new scraped questions)
✅ **Complete SQL schema** with performance tracking tables
✅ **CSV file ready**: `UPLOAD_TO_SUPABASE.csv`

---

## STEP 1: Create Database Tables (5 minutes)

### Go to Supabase SQL Editor

1. Open your browser and go to: https://supabase.com
2. Click on your project
3. Click **SQL Editor** in the left sidebar
4. Click **New Query**

### Run the SQL Schema

1. Open the file: `PHASE_2_SQL_SCHEMA.sql` (in this folder)
2. **Copy the ENTIRE contents** (all 400+ lines)
3. **Paste into the Supabase SQL Editor**
4. Click **RUN** (or press Cmd/Ctrl + Enter)
5. Wait ~10-20 seconds
6. You should see: ✅ **Success. No rows returned**

### Verify Tables Were Created

Run this query in SQL Editor:

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

You should see:
- ✅ `interview_questions`
- ✅ `user_profiles`
- ✅ `user_answers`
- ✅ `mock_interviews`

---

## STEP 2: Upload Questions CSV (5 minutes)

### Method 1: Supabase Dashboard Import (Easiest)

1. Go to **Table Editor** in left sidebar
2. Click on **interview_questions** table
3. Click **Insert** dropdown → **Import data from CSV**
4. Click **Select file** and choose: `UPLOAD_TO_SUPABASE.csv`
5. **Map columns** (should auto-map correctly):
   - question_text → question_text
   - company → company
   - difficulty → difficulty
   - question_type → question_type
   - topics → topics
   - source → source
   - answer_text → answer_text
   - created_at → created_at
6. Click **Import**
7. Wait 2-5 minutes (1,726 rows takes time)
8. ✅ Done!

### Method 2: Python Upload Script (If CSV Import Fails)

If the CSV import fails (file too large), run this:

```bash
cd "/Users/basilsuhail/folders/Data Sets/Data_Science_Interview_Questions"
source venv/bin/activate
python upload_to_supabase.py
```

I'll create that script if needed.

---

## STEP 3: Verify Upload Worked

### Run these queries in SQL Editor:

```sql
-- Check total questions
SELECT COUNT(*) as total_questions FROM interview_questions;
-- Should return: ~1726

-- Check by question type
SELECT question_type, COUNT(*)
FROM interview_questions
GROUP BY question_type
ORDER BY COUNT(*) DESC;

-- Check by difficulty
SELECT difficulty, COUNT(*)
FROM interview_questions
GROUP BY difficulty
ORDER BY COUNT(*) DESC;

-- Check by company (top 10)
SELECT company, COUNT(*)
FROM interview_questions
WHERE company IS NOT NULL AND company != ''
GROUP BY company
ORDER BY COUNT(*) DESC
LIMIT 10;

-- Check by source
SELECT source, COUNT(*)
FROM interview_questions
GROUP BY source
ORDER BY COUNT(*) DESC;
```

### Expected Results:

- **Total questions**: ~1,726
- **Question types**: mixed (936), ml (429), coding (129), stats (103), case (94), etc.
- **Difficulty**: medium (1,483), hard (189), easy (52)
- **Sources**: reddit, github, your original collections

---

## STEP 4: Test Helper Functions

### Test adaptive difficulty function:

```sql
-- This will return 'easy' since no user data yet
SELECT get_recommended_difficulty('00000000-0000-0000-0000-000000000000'::UUID);
```

### Test getting a random sample of questions:

```sql
-- Get 10 random medium coding questions
SELECT question_text, difficulty, question_type, company
FROM interview_questions
WHERE difficulty = 'medium'
  AND question_type = 'coding'
ORDER BY RANDOM()
LIMIT 10;
```

---

## STEP 5: What Happens Next?

After you upload the data, I will:

1. ✅ Update your app to fetch **real questions** from Supabase (instead of AI-generated)
2. ✅ Add **performance tracking** (save user answers to `user_answers` table)
3. ✅ Implement **adaptive difficulty** (questions get harder as user improves)
4. ✅ Add **progress analytics** (show user stats: accuracy, time spent, weak areas)

---

## 🐛 Troubleshooting

### Problem: CSV import fails (file too large)
**Solution:** Use Method 2 (Python upload script)

### Problem: "Column not found" error
**Solution:**
1. Check CSV headers match table column names exactly
2. Re-run the CREATE TABLE SQL to ensure all columns exist

### Problem: Questions don't show up in table
**Solution:**
1. Verify table exists: `SELECT * FROM interview_questions LIMIT 5;`
2. Check for errors in the import log
3. Try uploading a smaller sample first (first 100 rows)

### Problem: Permission denied / Row Level Security error
**Solution:**
```sql
-- Temporarily disable RLS for testing
ALTER TABLE interview_questions DISABLE ROW LEVEL SECURITY;

-- Re-enable after testing
ALTER TABLE interview_questions ENABLE ROW LEVEL SECURITY;
```

---

## 📊 What You Now Have

### Database Tables:
1. **interview_questions** (1,726 questions)
   - Real interview questions from multiple sources
   - Tagged by company, difficulty, type, topics

2. **user_profiles** (empty, will populate from localStorage)
   - User experience level, target companies, weak areas

3. **user_answers** (empty, will populate as users practice)
   - Every question answered, correctness, time spent

4. **mock_interviews** (empty, will populate in Phase 3)
   - Full mock interview sessions with analytics

### Helper Functions:
1. `get_recommended_difficulty(user_id)` - Returns adaptive difficulty
2. `get_weak_question_types(user_id)` - Returns user's weak areas
3. `user_performance_stats` - View with aggregate performance data

---

## 📁 Files Reference

- `PHASE_2_SQL_SCHEMA.sql` - Complete database schema (run this first)
- `UPLOAD_TO_SUPABASE.csv` - 1,726 questions to upload
- `scraped_questions.csv` - 1,332 newly scraped questions (backup)
- `collected_questions/final_interview_questions.csv` - Your original 900 questions (backup)

---

## ✅ Checklist

Before moving to the next step, verify:

- [ ] All 4 tables created in Supabase
- [ ] 1,726 questions uploaded to `interview_questions` table
- [ ] Can run SELECT queries successfully
- [ ] Helper functions return results (even if empty)
- [ ] Row Level Security policies are active

---

**Once you complete these steps, tell me and I'll update the app to use these real questions!** 🚀
