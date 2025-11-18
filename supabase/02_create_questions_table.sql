-- Create interview_questions table
-- This table stores 234 interview questions from multiple sources
-- Upload file: interview_questions_data.csv after running this

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

-- Create indexes for faster filtering and searching
CREATE INDEX IF NOT EXISTS idx_questions_difficulty
ON interview_questions(difficulty);

CREATE INDEX IF NOT EXISTS idx_questions_type
ON interview_questions(question_type);

CREATE INDEX IF NOT EXISTS idx_questions_company
ON interview_questions(company);

CREATE INDEX IF NOT EXISTS idx_questions_topics
ON interview_questions(topics);

CREATE INDEX IF NOT EXISTS idx_questions_search
ON interview_questions USING gin(to_tsvector('english', question_text));
