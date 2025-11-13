-- Enable pgvector extension for vector similarity search
CREATE EXTENSION IF NOT EXISTS vector;

-- Table to store book metadata
CREATE TABLE IF NOT EXISTS books (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title TEXT NOT NULL,
    filename TEXT NOT NULL,
    total_chunks INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table to store text chunks with vector embeddings
CREATE TABLE IF NOT EXISTS document_chunks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    book_id UUID REFERENCES books(id) ON DELETE CASCADE,
    book_name TEXT NOT NULL,
    page_number INTEGER,
    chunk_text TEXT NOT NULL,
    embedding vector(384),  -- all-MiniLM-L6-v2 produces 384-dimensional vectors
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for vector similarity search (using cosine distance)
CREATE INDEX ON document_chunks USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Create regular indexes for faster filtering
CREATE INDEX idx_chunks_book_id ON document_chunks(book_id);
CREATE INDEX idx_chunks_book_name ON document_chunks(book_name);

-- Function to search similar chunks using vector similarity
CREATE OR REPLACE FUNCTION match_documents(
    query_embedding vector(384),
    match_count INT DEFAULT 5,
    filter_book_name TEXT DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    book_name TEXT,
    page_number INTEGER,
    chunk_text TEXT,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        document_chunks.id,
        document_chunks.book_name,
        document_chunks.page_number,
        document_chunks.chunk_text,
        1 - (document_chunks.embedding <=> query_embedding) AS similarity
    FROM document_chunks
    WHERE
        CASE
            WHEN filter_book_name IS NOT NULL THEN document_chunks.book_name = filter_book_name
            ELSE TRUE
        END
    ORDER BY document_chunks.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Create view for statistics
CREATE OR REPLACE VIEW book_statistics AS
SELECT
    b.id,
    b.title,
    b.filename,
    COUNT(dc.id) as chunk_count,
    b.created_at
FROM books b
LEFT JOIN document_chunks dc ON b.id = dc.book_id
GROUP BY b.id, b.title, b.filename, b.created_at;

-- Enable Row Level Security (RLS)
ALTER TABLE books ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_chunks ENABLE ROW LEVEL SECURITY;

-- Allow public read access (anyone can search)
CREATE POLICY "Allow public read access on books"
    ON books FOR SELECT
    TO anon
    USING (true);

CREATE POLICY "Allow public read access on document_chunks"
    ON document_chunks FOR SELECT
    TO anon
    USING (true);

-- Only authenticated users can insert/update (for uploading data)
CREATE POLICY "Allow authenticated insert on books"
    ON books FOR INSERT
    TO authenticated
    WITH CHECK (true);

CREATE POLICY "Allow authenticated insert on document_chunks"
    ON document_chunks FOR INSERT
    TO authenticated
    WITH CHECK (true);

-- Comments for documentation
COMMENT ON TABLE books IS 'Stores metadata about source books/PDFs';
COMMENT ON TABLE document_chunks IS 'Stores text chunks with vector embeddings for semantic search';
COMMENT ON FUNCTION match_documents IS 'Performs vector similarity search on document chunks';
