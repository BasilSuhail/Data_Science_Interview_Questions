-- Copy and paste this ENTIRE file into Supabase SQL Editor
-- This creates everything you need!

-- Enable vector search
CREATE EXTENSION IF NOT EXISTS vector;

-- Simple table for storing text chunks with vectors
CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    book_name TEXT,
    page_number INTEGER,
    content TEXT,
    embedding vector(384)
);

-- Create index for fast vector search
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Search function
CREATE OR REPLACE FUNCTION search_documents(
    query_embedding vector(384),
    match_count INT DEFAULT 10
)
RETURNS TABLE (
    book_name TEXT,
    page_number INTEGER,
    content TEXT,
    similarity FLOAT
)
LANGUAGE SQL STABLE
AS $$
    SELECT
        book_name,
        page_number,
        content,
        1 - (embedding <=> query_embedding) AS similarity
    FROM documents
    ORDER BY embedding <=> query_embedding
    LIMIT match_count;
$$;

-- Allow public to read (so anyone can search)
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public can read documents"
ON documents FOR SELECT
TO anon, authenticated
USING (true);
