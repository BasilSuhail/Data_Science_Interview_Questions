-- ========================================
-- COMPLETE DATABASE SETUP - ALL IN ONE
-- Run this single script to set up everything
-- ========================================

-- ========================================
-- PART 1: CREATE TABLES
-- ========================================

-- DOCUMENTS TABLE (for textbooks)
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
CREATE INDEX IF NOT EXISTS idx_documents_book
ON documents(book_name);

-- Create index for page number
CREATE INDEX IF NOT EXISTS idx_documents_page
ON documents(page_number);

-- INTERVIEW_QUESTIONS TABLE
CREATE TABLE IF NOT EXISTS interview_questions (
    id BIGSERIAL PRIMARY KEY,
    question_text TEXT,
    company TEXT,
    difficulty TEXT,
    question_type TEXT,
    topics TEXT,
    source TEXT,
    answer_text TEXT,
    category TEXT,
    tags TEXT,
    constraints TEXT,
    examples TEXT,
    hints TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for faster filtering and searching
CREATE INDEX IF NOT EXISTS idx_questions_difficulty
ON interview_questions(difficulty);

CREATE INDEX IF NOT EXISTS idx_questions_type
ON interview_questions(question_type);

CREATE INDEX IF NOT EXISTS idx_questions_company
ON interview_questions(company);

CREATE INDEX IF NOT EXISTS idx_questions_topics
ON interview_questions(topics);

CREATE INDEX IF NOT EXISTS idx_questions_category
ON interview_questions(category);

CREATE INDEX IF NOT EXISTS idx_questions_search
ON interview_questions USING gin(to_tsvector('english', question_text));

-- ========================================
-- DONE! Now upload your CSV files:
-- 1. documents_data.csv -> documents table
-- 2. interview_questions_data.csv -> interview_questions table
-- ========================================
