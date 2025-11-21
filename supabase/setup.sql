-- ============================================
-- PHASE 2: COMPLETE DATABASE SCHEMA
-- AI Interview Coach - Performance Tracking
-- ============================================
-- Run this in Supabase SQL Editor
-- This creates ALL tables needed for Phase 2

-- ============================================
-- 1. INTERVIEW QUESTIONS TABLE
-- ============================================
-- This table stores all real interview questions
CREATE TABLE IF NOT EXISTS interview_questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_text TEXT NOT NULL,
    company TEXT,  -- e.g., 'Meta', 'Google', 'Amazon', NULL for generic
    difficulty TEXT,  -- 'easy', 'medium', 'hard' (no strict constraint to allow flexibility)
    question_type TEXT,  -- 'coding', 'stats', 'ml', 'case', 'behavioral', 'mixed', 'sql', etc. (no strict constraint)
    topics TEXT,  -- Pipe-separated topics (e.g., "regression|hypothesis_testing|python")
    source TEXT,  -- Where the question came from (e.g., 'github', 'leetcode', 'glassdoor')
    answer_text TEXT,  -- Answer if available (can be NULL)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_company ON interview_questions(company);
CREATE INDEX IF NOT EXISTS idx_difficulty ON interview_questions(difficulty);
CREATE INDEX IF NOT EXISTS idx_question_type ON interview_questions(question_type);
CREATE INDEX IF NOT EXISTS idx_topics ON interview_questions USING gin(to_tsvector('english', topics));

-- ============================================
-- 2. USER PROFILES TABLE
-- ============================================
-- Stores user profile data (currently in localStorage, will migrate here later)
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_email TEXT UNIQUE,  -- Optional: for auth later
    experience_level TEXT CHECK (experience_level IN ('junior', 'mid', 'senior')),
    target_companies TEXT[],  -- Array of company names ['Meta', 'Google', 'Netflix']
    weak_areas TEXT[],  -- Array of weak areas ['coding', 'stats', 'ml', 'case', 'communication']
    interview_date DATE,  -- When is their interview (NULL if "Practice Only")
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 3. USER ANSWERS TABLE (Performance Tracking)
-- ============================================
-- Tracks every question a user answers
CREATE TABLE IF NOT EXISTS user_answers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID,  -- References user_profiles.id (NULL for anonymous users)
    session_id UUID,  -- Groups answers from the same practice session
    question_id UUID REFERENCES interview_questions(id) ON DELETE CASCADE,
    user_answer TEXT,  -- The user's actual answer
    is_correct BOOLEAN,  -- Did they get it right?
    time_spent_seconds INT,  -- How long did they take?
    hints_used INT DEFAULT 0,  -- How many hints did they use?
    difficulty_at_time TEXT,  -- What difficulty was this question when answered?
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Foreign key (optional, for later when we add auth)
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES user_profiles(id) ON DELETE CASCADE
);

-- Indexes for analytics
CREATE INDEX IF NOT EXISTS idx_user_answers_user ON user_answers(user_id);
CREATE INDEX IF NOT EXISTS idx_user_answers_session ON user_answers(session_id);
CREATE INDEX IF NOT EXISTS idx_user_answers_question ON user_answers(question_id);
CREATE INDEX IF NOT EXISTS idx_user_answers_created ON user_answers(created_at);

-- ============================================
-- 4. MOCK INTERVIEWS TABLE (Phase 3 prep)
-- ============================================
-- Tracks full mock interview sessions
CREATE TABLE IF NOT EXISTS mock_interviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID,  -- References user_profiles.id
    session_id UUID UNIQUE NOT NULL,  -- Same as session_id in user_answers
    duration_minutes INT,  -- How long was the interview?
    questions_answered INT,  -- Total questions answered
    questions_correct INT,  -- How many were correct?
    accuracy_percent FLOAT,  -- (questions_correct / questions_answered) * 100
    avg_time_per_question INT,  -- Average time per question in seconds
    interview_type TEXT,  -- 'coding', 'stats', 'ml', 'mixed', etc.
    target_company TEXT,  -- Which company were they practicing for?
    session_notes TEXT,  -- AI-generated feedback or user notes
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES user_profiles(id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_mock_interviews_user ON mock_interviews(user_id);
CREATE INDEX IF NOT EXISTS idx_mock_interviews_created ON mock_interviews(created_at);

-- ============================================
-- 5. USER PERFORMANCE STATS (Materialized View)
-- ============================================
-- This view calculates aggregate performance stats for each user
CREATE OR REPLACE VIEW user_performance_stats AS
SELECT
    user_id,
    COUNT(*) as total_questions_answered,
    SUM(CASE WHEN is_correct THEN 1 ELSE 0 END) as total_correct,
    ROUND(AVG(CASE WHEN is_correct THEN 1 ELSE 0 END) * 100, 2) as overall_accuracy_percent,
    AVG(time_spent_seconds) as avg_time_per_question,
    MAX(created_at) as last_practice_date,

    -- Performance by difficulty
    ROUND(AVG(CASE WHEN difficulty_at_time = 'easy' AND is_correct THEN 1.0 ELSE 0.0 END) * 100, 2) as easy_accuracy,
    ROUND(AVG(CASE WHEN difficulty_at_time = 'medium' AND is_correct THEN 1.0 ELSE 0.0 END) * 100, 2) as medium_accuracy,
    ROUND(AVG(CASE WHEN difficulty_at_time = 'hard' AND is_correct THEN 1.0 ELSE 0.0 END) * 100, 2) as hard_accuracy
FROM user_answers
WHERE user_id IS NOT NULL
GROUP BY user_id;

-- ============================================
-- 6. ROW LEVEL SECURITY (RLS) - ENABLE PUBLIC READ
-- ============================================
-- Enable RLS on all tables
ALTER TABLE interview_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_answers ENABLE ROW LEVEL SECURITY;
ALTER TABLE mock_interviews ENABLE ROW LEVEL SECURITY;

-- Allow public read access to interview questions (everyone can see questions)
CREATE POLICY "Allow public read access to questions"
ON interview_questions
FOR SELECT
TO anon
USING (true);

-- Allow public insert to questions (for scrapers/admin)
CREATE POLICY "Allow public insert to questions"
ON interview_questions
FOR INSERT
TO anon
WITH CHECK (true);

-- Allow anonymous users to insert their answers (for now)
CREATE POLICY "Allow anonymous users to insert answers"
ON user_answers
FOR INSERT
TO anon
WITH CHECK (true);

-- Allow anonymous users to read their own answers (by session_id)
CREATE POLICY "Allow users to read their own answers"
ON user_answers
FOR SELECT
TO anon
USING (true);  -- Later: restrict to user_id = auth.uid()

-- Allow anonymous users to insert mock interview data
CREATE POLICY "Allow anonymous users to insert mock interviews"
ON mock_interviews
FOR INSERT
TO anon
WITH CHECK (true);

-- Allow users to read their own mock interviews
CREATE POLICY "Allow users to read their own mock interviews"
ON mock_interviews
FOR SELECT
TO anon
USING (true);  -- Later: restrict to user_id = auth.uid()

-- ============================================
-- 7. HELPER FUNCTIONS
-- ============================================

-- Function: Get recommended difficulty for user based on performance
CREATE OR REPLACE FUNCTION get_recommended_difficulty(p_user_id UUID)
RETURNS TEXT AS $$
DECLARE
    v_accuracy FLOAT;
    v_total_answered INT;
BEGIN
    -- Get user's overall accuracy
    SELECT
        AVG(CASE WHEN is_correct THEN 1.0 ELSE 0.0 END),
        COUNT(*)
    INTO v_accuracy, v_total_answered
    FROM user_answers
    WHERE user_id = p_user_id
        AND created_at > NOW() - INTERVAL '7 days';  -- Last 7 days only

    -- If not enough data, start with easy
    IF v_total_answered < 5 THEN
        RETURN 'easy';
    END IF;

    -- Adaptive difficulty logic
    IF v_accuracy >= 0.80 THEN
        RETURN 'hard';      -- Doing great, challenge them!
    ELSIF v_accuracy >= 0.60 THEN
        RETURN 'medium';    -- Good performance, medium level
    ELSE
        RETURN 'easy';      -- Struggling, keep it easy
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Function: Get user's weak question types
CREATE OR REPLACE FUNCTION get_weak_question_types(p_user_id UUID)
RETURNS TABLE(question_type TEXT, accuracy FLOAT) AS $$
BEGIN
    RETURN QUERY
    SELECT
        iq.question_type,
        AVG(CASE WHEN ua.is_correct THEN 1.0 ELSE 0.0 END) as accuracy
    FROM user_answers ua
    JOIN interview_questions iq ON ua.question_id = iq.id
    WHERE ua.user_id = p_user_id
        AND ua.created_at > NOW() - INTERVAL '14 days'
    GROUP BY iq.question_type
    HAVING COUNT(*) >= 3  -- At least 3 questions answered
    ORDER BY accuracy ASC
    LIMIT 3;  -- Return top 3 weakest areas
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- 8. VERIFICATION QUERIES
-- ============================================
-- Run these after uploading data to verify everything works

-- Check question counts
-- SELECT COUNT(*) as total_questions FROM interview_questions;

-- Check questions by type
-- SELECT question_type, COUNT(*)
-- FROM interview_questions
-- GROUP BY question_type
-- ORDER BY COUNT(*) DESC;

-- Check questions by company
-- SELECT company, COUNT(*)
-- FROM interview_questions
-- WHERE company IS NOT NULL AND company != ''
-- GROUP BY company
-- ORDER BY COUNT(*) DESC
-- LIMIT 15;

-- Check questions by difficulty
-- SELECT difficulty, COUNT(*)
-- FROM interview_questions
-- GROUP BY difficulty;

-- ============================================
-- DONE! 🎉
-- ============================================
-- Next steps:
-- 1. Upload your CSV data to interview_questions table
-- 2. Test the helper functions
-- 3. Update the app to use these tables
