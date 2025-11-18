-- Create documents table for textbook content
-- This table stores the 10 textbooks (3,983 pages) for RAG-powered AI answers
-- Upload file: documents_data.csv after running this

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
