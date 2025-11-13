# Complete Supabase Setup Guide

This guide will walk you through setting up Supabase from scratch, creating tables, enabling vector search, and uploading your data.

---

## 📋 Table of Contents

1. [Create Supabase Account](#step-1-create-supabase-account)
2. [Create New Project](#step-2-create-new-project)
3. [Enable pgvector Extension](#step-3-enable-pgvector-extension)
4. [Create Tables Using SQL Editor](#step-4-create-tables-using-sql-editor)
5. [Get Your API Keys](#step-5-get-your-api-keys)
6. [Install Python Libraries](#step-6-install-python-libraries)
7. [Upload Your Data](#step-7-upload-your-data)
8. [Verify Data in Table Editor](#step-8-verify-data-in-table-editor)
9. [Test Vector Search](#step-9-test-vector-search)

---

## Step 1: Create Supabase Account

### 1.1 Go to Supabase
Visit: https://supabase.com

### 1.2 Sign Up
- Click **"Start your project"** or **"Sign In"**
- Sign up with:
  - GitHub (recommended)
  - Google
  - Email

### 1.3 Verify Email
- Check your email for verification link
- Click the link to verify

✅ **You now have a Supabase account!**

---

## Step 2: Create New Project

### 2.1 Click "New Project"
After logging in, click the **"New Project"** button

### 2.2 Fill in Project Details
- **Name**: `data-science-interview-questions` (or any name you like)
- **Database Password**: Choose a strong password (SAVE THIS!)
- **Region**: Choose closest to you (e.g., US East, EU Central)
- **Pricing Plan**: Free tier is fine to start

### 2.3 Wait for Setup
- Project creation takes 1-2 minutes
- You'll see a progress screen

✅ **Your Supabase project is now created!**

---

## Step 3: Enable pgvector Extension

### 3.1 Open SQL Editor
In your Supabase dashboard:
1. Click **"SQL Editor"** in the left sidebar
2. You'll see a text editor where you can run SQL commands

### 3.2 Enable the Extension
Copy and paste this command into the SQL editor:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### 3.3 Run the Query
- Click **"Run"** button (or press Ctrl+Enter / Cmd+Enter)
- You should see: ✅ Success. No rows returned

✅ **pgvector extension is now enabled!**

**What this does:** Enables vector similarity search in your database

---

## Step 4: Create Tables Using SQL Editor

### 4.1 Still in SQL Editor
Keep the SQL Editor open from Step 3

### 4.2 Copy the Schema SQL
Open the file: `supabase/migrations/001_initial_schema.sql`

**OR** copy this entire SQL script:

```sql
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
    embedding vector(384),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for vector similarity search
CREATE INDEX ON document_chunks USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Create regular indexes for faster filtering
CREATE INDEX idx_chunks_book_id ON document_chunks(book_id);
CREATE INDEX idx_chunks_book_name ON document_chunks(book_name);

-- Function to search similar chunks
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

-- Enable Row Level Security
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

-- Only authenticated users can insert/update
CREATE POLICY "Allow authenticated insert on books"
    ON books FOR INSERT
    TO authenticated
    WITH CHECK (true);

CREATE POLICY "Allow authenticated insert on document_chunks"
    ON document_chunks FOR INSERT
    TO authenticated
    WITH CHECK (true);
```

### 4.3 Paste and Run
1. Paste the entire script into the SQL Editor
2. Click **"Run"** button
3. Wait for completion (might take 5-10 seconds)
4. You should see: ✅ Success

✅ **Your tables are now created!**

**What this created:**
- ✅ `books` table - Stores book metadata
- ✅ `document_chunks` table - Stores text chunks with embeddings
- ✅ `match_documents()` function - For semantic search
- ✅ `book_statistics` view - For statistics
- ✅ Security policies - Public can read, auth can write

---

## Step 5: Get Your API Keys

### 5.1 Go to Project Settings
1. Click the **⚙️ Settings** icon in the left sidebar
2. Click **"API"** in the settings menu

### 5.2 Copy Your Credentials

You'll see two important things:

#### **Project URL**
```
https://xxxxxxxxxxxxx.supabase.co
```
Copy this - you'll need it!

#### **API Keys**
You'll see two keys:

1. **anon public** key - Safe to use in browsers
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

2. **service_role secret** key - NEVER share this! Use for uploading
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

### 5.3 Save These Credentials

Create a file called `.env` in your project folder:

```bash
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_KEY=your-service-role-key-here
SUPABASE_ANON_KEY=your-anon-public-key-here
```

**⚠️ IMPORTANT:**
- Add `.env` to your `.gitignore` file
- NEVER commit this file to GitHub
- The service_role key has full database access

✅ **You have your API credentials!**

---

## Step 6: Install Python Libraries

### 6.1 Open Terminal
Navigate to your project folder:
```bash
cd "/Users/basilsuhail/folders/Data Sets/Data_Science_Interview_Questions"
```

### 6.2 Install Required Libraries
```bash
pip install supabase sentence-transformers python-dotenv
```

**What each library does:**
- `supabase` - Connect to Supabase from Python
- `sentence-transformers` - Create vector embeddings
- `python-dotenv` - Load credentials from .env file

### 6.3 Verify Installation
```bash
python -c "import supabase; print('✓ Supabase installed')"
python -c "from sentence_transformers import SentenceTransformer; print('✓ Embeddings installed')"
```

✅ **All libraries installed!**

---

## Step 7: Upload Your Data

### 7.1 Make Sure You Have Extracted Text
First, check if you have extracted text from PDFs:

```bash
ls -la extracted_text/
```

If empty, run:
```bash
python extract_pdf_content.py
```

### 7.2 Run the Upload Script

```bash
python upload_to_supabase.py
```

### 7.3 Enter Your Credentials

When prompted:
```
Supabase URL: [paste your project URL]
Supabase Service Key: [paste your service_role key]
```

**OR** if you created the `.env` file, it will load automatically!

### 7.4 Upload Process

You'll see a menu:
```
OPTIONS
1. Upload all books
2. Upload with force overwrite
3. Show statistics
4. Exit

Select option: 1
```

Choose **1** to upload all books.

### 7.5 Wait for Upload

You'll see progress:
```
Processing: Introduction_to_Data_Science
  Extracted 250 chunks
  Creating embeddings...
  100%|████████████████████| 250/250
  Uploading 250 chunks in batches of 50...
    Uploaded 50/250 chunks
    Uploaded 100/250 chunks
    ...
  ✓ Successfully uploaded 250 chunks
```

**This may take 5-15 minutes** depending on how many books you have!

✅ **Your data is now in Supabase!**

---

## Step 8: Verify Data in Table Editor

### 8.1 Go to Table Editor
In Supabase dashboard:
1. Click **"Table Editor"** in the left sidebar
2. You'll see your tables listed

### 8.2 Check the `books` Table
1. Click on **"books"** table
2. You should see your books listed:

| id | title | filename | total_chunks | created_at |
|----|-------|----------|--------------|------------|
| abc-123 | Introduction_to_Data_Science | ... | 250 | 2025-11-13 |
| def-456 | Python_for_Data_Science | ... | 180 | 2025-11-13 |

### 8.3 Check the `document_chunks` Table
1. Click on **"document_chunks"** table
2. You should see hundreds/thousands of rows:

| id | book_name | page_number | chunk_text | embedding |
|----|-----------|-------------|------------|-----------|
| abc | Intro... | 15 | What is machine learning... | [0.123, -0.456...] |

### 8.4 Table Editor Features

**Filter data:**
- Click column headers to sort
- Use the filter icon to filter by value

**Search:**
- Use the search bar at top

**Edit rows:**
- Click any cell to edit (be careful!)
- Click ✓ to save, ✗ to cancel

**Export data:**
- Click the **"Export to CSV"** button at top

✅ **You can see and manage your data!**

---

## Step 9: Test Vector Search

### 9.1 Go Back to SQL Editor
Click **"SQL Editor"** in the left sidebar

### 9.2 Test the Search Function

First, we need to get a sample embedding. For testing, we'll create a simple query:

```sql
-- Get a random embedding from the database for testing
SELECT embedding FROM document_chunks LIMIT 1;
```

Copy the embedding output (it will look like `[0.123, -0.456, ...]`)

### 9.3 Test the Match Function

```sql
-- Test search with a sample embedding
SELECT
    book_name,
    page_number,
    LEFT(chunk_text, 100) as preview,
    similarity
FROM match_documents(
    '[0.0234, -0.1234, 0.5678, ...]'::vector,  -- Replace with actual embedding
    5  -- top 5 results
)
ORDER BY similarity DESC;
```

### 9.4 Better Way: Test from Python

Create a test script `test_search.py`:

```python
import os
from supabase import create_client
from sentence_transformers import SentenceTransformer

# Load credentials
url = "your-supabase-url"
key = "your-anon-key"  # Use anon key for search

supabase = create_client(url, key)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Search query
query = "What is machine learning?"
query_embedding = model.encode([query])[0].tolist()

# Call the match function
result = supabase.rpc('match_documents', {
    'query_embedding': query_embedding,
    'match_count': 5
}).execute()

# Print results
for i, doc in enumerate(result.data, 1):
    print(f"\n[{i}] Book: {doc['book_name']}")
    print(f"    Page: {doc['page_number']}")
    print(f"    Similarity: {doc['similarity']:.2%}")
    print(f"    Text: {doc['chunk_text'][:200]}...")
```

Run it:
```bash
python test_search.py
```

✅ **Vector search is working!**

---

## 🎯 What You've Accomplished

- ✅ Created Supabase account and project
- ✅ Enabled pgvector extension
- ✅ Created tables with proper schema
- ✅ Set up security policies (public read, auth write)
- ✅ Uploaded all your text data with vector embeddings
- ✅ Tested vector similarity search
- ✅ Verified data in Table Editor

---

## 📊 Understanding Your Database Structure

### Tables

**1. books**
- Stores metadata about your PDF books
- Each book gets a unique ID
- Tracks how many chunks each book has

**2. document_chunks**
- Stores actual text chunks
- Each chunk has a 384-dimensional vector embedding
- Links to parent book via `book_id`
- Stores page numbers for reference

**3. book_statistics (view)**
- Auto-generated view showing stats
- Shows chunk count per book
- Useful for the frontend

### Functions

**match_documents()**
- Main search function
- Takes a vector embedding as input
- Returns most similar chunks
- Can filter by specific book
- Uses cosine similarity

---

## 🔍 Using the SQL Editor

### Common Queries

**Count total chunks:**
```sql
SELECT COUNT(*) FROM document_chunks;
```

**See all books:**
```sql
SELECT * FROM books ORDER BY created_at DESC;
```

**Get statistics:**
```sql
SELECT * FROM book_statistics;
```

**Find chunks from specific book:**
```sql
SELECT book_name, page_number, LEFT(chunk_text, 100) as preview
FROM document_chunks
WHERE book_name = 'Introduction_to_Data_Science'
LIMIT 10;
```

**Delete all data (if you need to start over):**
```sql
DELETE FROM document_chunks;
DELETE FROM books;
```

---

## 🛠️ Troubleshooting

### Problem: "extension vector does not exist"
**Solution:** Run `CREATE EXTENSION vector;` in SQL Editor

### Problem: "permission denied for table"
**Solution:** Check Row Level Security policies are created correctly

### Problem: Upload script fails with authentication error
**Solution:**
- Make sure you're using the `service_role` key (not anon key)
- Check the key is correct and not expired

### Problem: No data showing in tables
**Solution:**
- Check upload script completed successfully
- Verify extracted_text/ folder has content
- Check for errors in upload output

### Problem: Vector search returns no results
**Solution:**
- Verify embeddings were created (check document_chunks table)
- Make sure embedding dimensions match (384 for all-MiniLM-L6-v2)
- Test with SQL query first

---

## 🚀 Next Steps

Now that your data is in Supabase:

1. ✅ Build a web frontend for public access
2. ✅ Create API endpoints for search
3. ✅ Add authentication for uploading new content
4. ✅ Deploy the frontend (Vercel, Netlify, etc.)
5. ✅ Share with others!

---

## 📚 Additional Resources

- **Supabase Docs:** https://supabase.com/docs
- **pgvector Guide:** https://supabase.com/docs/guides/ai/vector-indexes
- **SQL Reference:** https://supabase.com/docs/guides/database/overview
- **API Reference:** https://supabase.com/docs/reference/javascript

---

## 💡 Tips

1. **Backup Your Data**
   - Go to Database → Backups in Supabase dashboard
   - Free tier gets daily backups

2. **Monitor Usage**
   - Check Database → Usage
   - Free tier limits: 500MB database, 2GB bandwidth

3. **Upgrade When Needed**
   - If you hit limits, consider upgrading to Pro ($25/month)
   - Gets you more storage and bandwidth

4. **API Keys Security**
   - NEVER commit service_role key to Git
   - Use environment variables
   - Rotate keys if exposed

---

You're all set! Your data is now in Supabase and ready for vector search! 🎉
