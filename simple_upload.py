"""
Simple script to upload your data to Supabase
Just run: python simple_upload.py
"""

from pathlib import Path
from sentence_transformers import SentenceTransformer
from supabase import create_client

# YOUR SUPABASE CREDENTIALS HERE
SUPABASE_URL = "https://iteavenjozhzxupbxosu.supabase.co"  # Like: https://xxxxx.supabase.co
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml0ZWF2ZW5qb3poenh1cGJ4b3N1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzAyOTg1OCwiZXhwIjoyMDc4NjA1ODU4fQ.uzK5i3xDTNHOObMIZKffzaKODAGU-I4mRqfP-jjUzd4"

print("Loading model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Process all extracted text files
for book_dir in Path('extracted_text').glob('*'):
    if not book_dir.is_dir():
        continue

    print(f"\nProcessing: {book_dir.name}")

    text_file = book_dir / 'full_text.txt'
    if not text_file.exists():
        continue

    text = text_file.read_text()

    # Split into chunks (simple version)
    chunks = [text[i:i+2000] for i in range(0, len(text), 2000)]

    for i, chunk in enumerate(chunks[:100]):  # Upload first 100 chunks per book
        if len(chunk.strip()) < 100:
            continue

        # Create embedding
        embedding = model.encode([chunk])[0].tolist()

        # Upload to Supabase
        supabase.table('documents').insert({
            'book_name': book_dir.name,
            'page_number': i + 1,
            'content': chunk,
            'embedding': embedding
        }).execute()

        print(f"  Uploaded chunk {i+1}")

print("\n✓ Done!")
