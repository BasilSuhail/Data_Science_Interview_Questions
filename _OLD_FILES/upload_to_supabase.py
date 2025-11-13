"""
Upload extracted text files to Supabase with vector embeddings
Automatically processes all files in extracted_text/ folder
"""

import os
from pathlib import Path
from typing import List, Dict
import numpy as np

# Check for required libraries
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    print("⚠️  sentence-transformers not installed!")
    print("Install with: pip install sentence-transformers")
    EMBEDDINGS_AVAILABLE = False

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    print("⚠️  supabase not installed!")
    print("Install with: pip install supabase")
    SUPABASE_AVAILABLE = False


class SupabaseUploader:
    """
    Uploads extracted text to Supabase with vector embeddings.
    Processes entire extracted_text/ folder automatically.
    """

    def __init__(self, supabase_url: str, supabase_key: str):
        if not SUPABASE_AVAILABLE:
            raise Exception("Supabase library not installed")
        if not EMBEDDINGS_AVAILABLE:
            raise Exception("sentence-transformers library not installed")

        self.supabase: Client = create_client(supabase_url, supabase_key)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✓ Connected to Supabase")
        print("✓ Loaded embedding model")

    def chunk_text(self, text: str, chunk_size: int = 400, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if len(chunk.strip()) > 50:  # Skip very short chunks
                chunks.append(chunk.strip())

        return chunks

    def extract_page_number(self, text_section: str) -> int:
        """Extract page number from text section"""
        lines = text_section.split('\n')
        for line in lines[:5]:
            if 'PAGE' in line.upper():
                try:
                    return int(''.join(filter(str.isdigit, line)))
                except:
                    pass
        return None

    def create_or_get_book(self, title: str, filename: str) -> str:
        """Create book record in Supabase or get existing"""
        # Check if book already exists
        result = self.supabase.table('books').select('id').eq('filename', filename).execute()

        if result.data:
            book_id = result.data[0]['id']
            print(f"  Book already exists (ID: {book_id})")
            return book_id

        # Create new book record
        book_data = {
            'title': title,
            'filename': filename
        }
        result = self.supabase.table('books').insert(book_data).execute()
        book_id = result.data[0]['id']
        print(f"  Created new book (ID: {book_id})")
        return book_id

    def upload_chunks_batch(self, chunks_data: List[Dict], batch_size: int = 50):
        """Upload chunks in batches to avoid timeout"""
        total = len(chunks_data)
        print(f"  Uploading {total} chunks in batches of {batch_size}...")

        for i in range(0, total, batch_size):
            batch = chunks_data[i:i + batch_size]
            try:
                self.supabase.table('document_chunks').insert(batch).execute()
                print(f"    Uploaded {min(i + batch_size, total)}/{total} chunks")
            except Exception as e:
                print(f"    ⚠️  Error uploading batch: {e}")
                # Try one by one if batch fails
                for chunk in batch:
                    try:
                        self.supabase.table('document_chunks').insert(chunk).execute()
                    except Exception as e2:
                        print(f"    ⚠️  Failed to upload chunk: {e2}")

    def process_book(self, book_dir: Path, force_reupload: bool = False):
        """Process a single book directory"""
        book_name = book_dir.name
        full_text_path = book_dir / 'full_text.txt'

        if not full_text_path.exists():
            print(f"⚠️  Skipping {book_name} - no full_text.txt found")
            return

        print(f"\nProcessing: {book_name}")

        # Create or get book record
        book_id = self.create_or_get_book(book_name, book_name)

        # Check if already uploaded
        if not force_reupload:
            result = self.supabase.table('document_chunks').select('id', count='exact').eq('book_id', book_id).execute()
            if result.count and result.count > 0:
                print(f"  Book already has {result.count} chunks uploaded")
                overwrite = input("  Overwrite? (y/n): ").strip().lower()
                if overwrite != 'y':
                    print("  Skipped")
                    return
                # Delete existing chunks
                print("  Deleting existing chunks...")
                self.supabase.table('document_chunks').delete().eq('book_id', book_id).execute()

        # Read content
        with open(full_text_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split by pages
        pages = content.split('=' * 80)
        all_chunks = []
        all_texts = []

        print("  Extracting chunks...")
        for page_section in pages:
            if not page_section.strip():
                continue

            page_num = self.extract_page_number(page_section)
            chunks = self.chunk_text(page_section)

            for chunk in chunks:
                all_chunks.append({
                    'book_id': book_id,
                    'book_name': book_name,
                    'page_number': page_num,
                    'chunk_text': chunk
                })
                all_texts.append(chunk)

        print(f"  Extracted {len(all_chunks)} chunks")

        # Create embeddings
        print("  Creating embeddings...")
        embeddings = self.model.encode(all_texts, show_progress_bar=True, convert_to_numpy=True)

        # Add embeddings to chunks
        for i, chunk in enumerate(all_chunks):
            chunk['embedding'] = embeddings[i].tolist()

        # Upload to Supabase
        self.upload_chunks_batch(all_chunks)

        # Update book total_chunks
        self.supabase.table('books').update({'total_chunks': len(all_chunks)}).eq('id', book_id).execute()

        print(f"  ✓ Successfully uploaded {len(all_chunks)} chunks")

    def upload_all(self, extracted_text_dir: str = 'extracted_text', force_reupload: bool = False):
        """Upload all books from extracted_text directory"""
        print("\n" + "="*80)
        print("UPLOADING TO SUPABASE")
        print("="*80 + "\n")

        extracted_dir = Path(extracted_text_dir)

        if not extracted_dir.exists():
            print(f"⚠️  Directory not found: {extracted_text_dir}")
            print("Please run 'python extract_pdf_content.py' first")
            return

        book_dirs = [d for d in extracted_dir.iterdir() if d.is_dir()]

        if not book_dirs:
            print("⚠️  No book directories found")
            return

        print(f"Found {len(book_dirs)} books to upload\n")

        for book_dir in book_dirs:
            try:
                self.process_book(book_dir, force_reupload)
            except Exception as e:
                print(f"⚠️  Error processing {book_dir.name}: {e}")

        print("\n" + "="*80)
        print("UPLOAD COMPLETE!")
        print("="*80)

    def get_statistics(self):
        """Display statistics from Supabase"""
        print("\n" + "="*80)
        print("SUPABASE DATABASE STATISTICS")
        print("="*80 + "\n")

        # Get total chunks
        result = self.supabase.table('document_chunks').select('*', count='exact').execute()
        print(f"Total chunks: {result.count}")

        # Get books
        result = self.supabase.table('book_statistics').select('*').execute()
        print(f"\nBooks ({len(result.data)}):")
        for book in result.data:
            print(f"  - {book['title']}: {book['chunk_count']} chunks")

        print("\n" + "="*80)


def main():
    """Main function with interactive setup"""

    if not SUPABASE_AVAILABLE or not EMBEDDINGS_AVAILABLE:
        print("\n⚠️  Missing required libraries!")
        print("\nInstall with:")
        print("  pip install supabase sentence-transformers")
        return

    print("\n" + "="*80)
    print("SUPABASE UPLOADER - SETUP")
    print("="*80 + "\n")

    # Check for environment variables first
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')

    if not supabase_url or not supabase_key:
        print("Please provide your Supabase credentials:")
        print("(You can also set SUPABASE_URL and SUPABASE_KEY environment variables)\n")

        supabase_url = input("Supabase URL: ").strip()
        supabase_key = input("Supabase Service Key: ").strip()

    if not supabase_url or not supabase_key:
        print("\n⚠️  Supabase credentials required!")
        return

    try:
        uploader = SupabaseUploader(supabase_url, supabase_key)

        # Menu
        while True:
            print("\n" + "="*80)
            print("OPTIONS")
            print("="*80)
            print("1. Upload all books")
            print("2. Upload with force overwrite")
            print("3. Show statistics")
            print("4. Exit")

            choice = input("\nSelect option: ").strip()

            if choice == '1':
                uploader.upload_all(force_reupload=False)
            elif choice == '2':
                uploader.upload_all(force_reupload=True)
            elif choice == '3':
                uploader.get_statistics()
            elif choice == '4':
                print("\nGoodbye!")
                break
            else:
                print("Invalid choice!")

    except Exception as e:
        print(f"\n⚠️  Error: {e}")


if __name__ == '__main__':
    main()
