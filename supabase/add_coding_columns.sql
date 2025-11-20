-- ========================================
-- SQL Script to Update interview_questions Table
-- For Adding Coding Questions Support
-- ========================================

-- Step 1: Ensure the 'category' column exists (if it doesn't)
-- If you get an error that category already exists, that's fine - skip to Step 2

ALTER TABLE interview_questions
ADD COLUMN IF NOT EXISTS category TEXT;

-- Step 2: Add new columns for coding questions metadata
-- These columns are optional and will store additional coding problem details

ALTER TABLE interview_questions
ADD COLUMN IF NOT EXISTS tags TEXT;

ALTER TABLE interview_questions
ADD COLUMN IF NOT EXISTS constraints TEXT;

ALTER TABLE interview_questions
ADD COLUMN IF NOT EXISTS examples TEXT;

ALTER TABLE interview_questions
ADD COLUMN IF NOT EXISTS hints TEXT;

-- Step 3: Create an index on category for faster queries
CREATE INDEX IF NOT EXISTS idx_interview_questions_category
ON interview_questions(category);

-- Step 4: Create an index on difficulty for faster queries
CREATE INDEX IF NOT EXISTS idx_interview_questions_difficulty
ON interview_questions(difficulty);

-- Step 5: Verify the changes
-- Run this query to see all columns in your table:
-- SELECT column_name, data_type, is_nullable
-- FROM information_schema.columns
-- WHERE table_name = 'interview_questions';

-- ========================================
-- INSTRUCTIONS FOR USE:
-- ========================================
-- 1. Go to Supabase Dashboard
-- 2. Navigate to SQL Editor
-- 3. Copy and paste this entire script
-- 4. Click "Run" button
-- 5. You should see "Success. No rows returned"
-- 6. Now you can import the CSV file using the Table Editor:
--    - Go to Table Editor
--    - Select "interview_questions" table
--    - Click "Insert" -> "Insert rows from CSV"
--    - Upload supabase/coding_questions.csv
-- ========================================
