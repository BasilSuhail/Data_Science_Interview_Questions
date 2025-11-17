# 🗄️ Supabase Database Setup for Interview Questions

## 📋 Overview

This guide shows you how to:
1. Create the `interview_questions` table in Supabase
2. Upload your collected questions
3. Integrate with your app

---

## STEP 1: Create the Table

### Option A: Using Supabase Dashboard (Easiest)

1. Go to https://supabase.com and open your project

2. Click **SQL Editor** in the left sidebar

3. Click **New Query**

4. Paste this SQL:

```sql
-- Create interview_questions table
CREATE TABLE IF NOT EXISTS interview_questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_text TEXT NOT NULL,
    company TEXT,
    difficulty TEXT CHECK (difficulty IN ('easy', 'medium', 'hard')),
    question_type TEXT CHECK (question_type IN ('coding', 'stats', 'ml', 'case', 'behavioral', 'mixed')),
    topics TEXT,  -- Pipe-separated topics (e.g., "regression|hypothesis_testing")
    source TEXT,  -- Where the question came from
    answer_text TEXT,  -- Answer if available
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_company ON interview_questions(company);
CREATE INDEX IF NOT EXISTS idx_difficulty ON interview_questions(difficulty);
CREATE INDEX IF NOT EXISTS idx_question_type ON interview_questions(question_type);

-- Enable Row Level Security (optional but recommended)
ALTER TABLE interview_questions ENABLE ROW LEVEL SECURITY;

-- Create policy to allow public read access
CREATE POLICY "Allow public read access"
ON interview_questions
FOR SELECT
TO anon
USING (true);
```

5. Click **RUN** (or press Cmd/Ctrl + Enter)

6. You should see: ✅ Success. No rows returned

---

### Option B: Using SQL Command Line

If you have Supabase CLI installed:

```bash
supabase db reset
# Then run the SQL from Option A in the SQL Editor
```

---

## STEP 2: Upload Questions

### Method 1: CSV Import via Dashboard (Recommended)

1. Go to **Table Editor** → **interview_questions** table

2. Click **Insert** → **Import data from CSV**

3. Select: `final_interview_questions.csv`

4. **Map columns**:
   - question_text → question_text
   - company → company
   - difficulty → difficulty
   - question_type → question_type
   - topics → topics
   - source → source
   - answer_text → answer_text
   - created_at → created_at

5. Click **Import**

6. Wait for upload (may take 2-5 minutes for 300-700 rows)

7. **Verify**: Check row count matches your CSV

---

### Method 2: Python Upload Script

If CSV import fails (file too large), use this script:

```python
import csv
from supabase import create_client

# Your Supabase credentials (from config.js)
SUPABASE_URL = "your_supabase_url_here"
SUPABASE_KEY = "your_supabase_anon_key_here"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load CSV
with open('final_interview_questions.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    questions = list(reader)

# Upload in batches
batch_size = 100
for i in range(0, len(questions), batch_size):
    batch = questions[i:i+batch_size]
    supabase.table('interview_questions').insert(batch).execute()
    print(f"Uploaded batch {i//batch_size + 1}")

print(f"✅ Uploaded {len(questions)} questions!")
```

---

## STEP 3: Verify Upload

### Quick Check:

Go to **Table Editor** → **interview_questions**

You should see:
- ✅ Multiple rows (300-700+)
- ✅ question_text filled
- ✅ Some rows have company names
- ✅ difficulty: easy/medium/hard
- ✅ question_type: coding/stats/ml/case/behavioral

### SQL Check:

Run in SQL Editor:

```sql
-- Count total questions
SELECT COUNT(*) FROM interview_questions;

-- Count by type
SELECT question_type, COUNT(*)
FROM interview_questions
GROUP BY question_type
ORDER BY COUNT(*) DESC;

-- Count by company
SELECT company, COUNT(*)
FROM interview_questions
WHERE company IS NOT NULL AND company != ''
GROUP BY company
ORDER BY COUNT(*) DESC
LIMIT 10;

-- Count by difficulty
SELECT difficulty, COUNT(*)
FROM interview_questions
GROUP BY difficulty;
```

---

## STEP 4: Integrate with Your App

Now you need to update your app to use real questions instead of AI-generated ones.

### Current Flow (AI-Generated):
1. User clicks "Generate Questions"
2. App sends prompt to Groq API
3. AI generates random questions
4. Questions displayed

### New Flow (Real Questions):
1. User clicks "Generate Questions"
2. App queries Supabase `interview_questions` table
3. Filter by: user's profile (company, difficulty, type)
4. Return random sample of matching questions
5. Questions displayed

---

## STEP 5: Update index.html (Integration Code)

I'll create a separate script to modify your `index.html` to use real questions.

For now, here's the query logic you'll need:

```javascript
// Example: Fetch questions from Supabase
async function fetchRealQuestions(userProfile, questionCount = 10) {
    const { experience, companies, weakAreas } = userProfile;
    const interviewType = document.getElementById('interview-type').value;

    // Build query
    let query = supabase
        .from('interview_questions')
        .select('*');

    // Filter by company if user specified
    if (companies && companies.length > 0) {
        query = query.in('company', companies);
    }

    // Filter by question type
    if (interviewType !== 'mixed') {
        query = query.eq('question_type', interviewType);
    }

    // Get more questions than needed (we'll filter by experience level)
    query = query.limit(questionCount * 3);

    const { data, error } = await query;

    if (error) {
        console.error('Error fetching questions:', error);
        return [];
    }

    // Randomly sample questionCount questions
    const shuffled = data.sort(() => 0.5 - Math.random());
    return shuffled.slice(0, questionCount);
}
```

---

## 🎯 Verification Checklist

Before moving on, verify:

- [x] Table `interview_questions` exists in Supabase
- [x] Table has 300+ rows
- [x] Columns: question_text, company, difficulty, question_type, topics, source
- [x] Can run SELECT query successfully
- [x] Row Level Security enabled (optional but recommended)

---

## 🐛 Troubleshooting

### Problem: CSV import fails (file too large)
**Solution:** Use Python upload script (Method 2 above)

### Problem: "Column not found" error during import
**Solution:**
- Check CSV headers match table column names exactly
- Re-run CREATE TABLE SQL to ensure all columns exist

### Problem: Questions don't show up in app
**Solution:**
- Verify table has data: `SELECT COUNT(*) FROM interview_questions`
- Check Supabase URL and API key in config.js
- Check browser console for errors

### Problem: Row Level Security blocks access
**Solution:**
- Disable RLS temporarily: `ALTER TABLE interview_questions DISABLE ROW LEVEL SECURITY`
- Or create proper policy (see CREATE POLICY in Step 1)

---

## 📊 Database Schema Reference

```
interview_questions
├── id (UUID, primary key)
├── question_text (TEXT, not null) - The actual question
├── company (TEXT) - Company that asked this (e.g., "Meta", "Google")
├── difficulty (TEXT) - "easy", "medium", or "hard"
├── question_type (TEXT) - "coding", "stats", "ml", "case", "behavioral", "mixed"
├── topics (TEXT) - Pipe-separated topics (e.g., "regression|stats")
├── source (TEXT) - Where question came from (e.g., "github", "leetcode")
├── answer_text (TEXT) - Answer if available (usually empty for now)
└── created_at (TIMESTAMP) - When question was added
```

---

**Next:** See `APP_INTEGRATION.md` for how to update your app to use these real questions!
