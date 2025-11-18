-- Verification queries to run after uploading data
-- Run these to make sure everything uploaded correctly

-- 1. Check documents table row count (should be ~3,983)
SELECT COUNT(*) as total_pages FROM documents;

-- 2. Check interview_questions table row count (should be 234)
SELECT COUNT(*) as total_questions FROM interview_questions;

-- 3. View documents by book
SELECT
    book_name,
    COUNT(*) as page_count
FROM documents
GROUP BY book_name
ORDER BY page_count DESC;

-- 4. View questions by type
SELECT
    question_type,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) as percentage
FROM interview_questions
GROUP BY question_type
ORDER BY count DESC;

-- 5. View questions by difficulty
SELECT
    difficulty,
    COUNT(*) as count
FROM interview_questions
GROUP BY difficulty
ORDER BY count DESC;

-- 6. View questions by source
SELECT
    source,
    COUNT(*) as count
FROM interview_questions
GROUP BY source
ORDER BY count DESC;

-- 7. Test text search on documents (search for "regression")
SELECT
    book_name,
    page_number,
    LEFT(content, 100) as preview
FROM documents
WHERE to_tsvector('english', content) @@ to_tsquery('english', 'regression')
LIMIT 5;

-- 8. Test filtering questions (get medium ML questions)
SELECT
    question_text,
    source
FROM interview_questions
WHERE difficulty = 'medium'
  AND question_type = 'ml'
LIMIT 5;
