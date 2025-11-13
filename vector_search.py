"""
Vector Search System for Interview Questions
Uses sentence embeddings to find semantically similar content
Works with extracted text files from PDFs
"""

import os
import json
import pickle
from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np

# Check for required libraries
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    print("⚠️  sentence-transformers not installed!")
    print("Install with: pip install sentence-transformers")
    EMBEDDINGS_AVAILABLE = False


class VectorSearchEngine:
    """
    Vector-based semantic search engine for interview questions.
    Automatically indexes all text files in extracted_text/ folder.
    """

    def __init__(self, extracted_text_dir='extracted_text', cache_file='vector_cache.pkl'):
        self.extracted_text_dir = Path(extracted_text_dir)
        self.cache_file = cache_file
        self.model = None
        self.documents = []  # List of {file, chunk, page, text}
        self.embeddings = None  # Numpy array of embeddings

        if EMBEDDINGS_AVAILABLE:
            print("Loading sentence transformer model...")
            # Using a lightweight, fast model
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✓ Model loaded!")
        else:
            print("⚠️  Vector search not available without sentence-transformers")

    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Split text into overlapping chunks for better context preservation.
        """
        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)

        return chunks

    def extract_page_number(self, text_section: str) -> int:
        """
        Try to extract page number from text section headers.
        """
        lines = text_section.split('\n')
        for line in lines[:5]:  # Check first few lines
            if 'PAGE' in line.upper():
                try:
                    return int(''.join(filter(str.isdigit, line)))
                except:
                    pass
        return None

    def index_all_files(self, force_reindex: bool = False):
        """
        Index all text files in the extracted_text directory.
        Creates vector embeddings for semantic search.
        """
        if not EMBEDDINGS_AVAILABLE:
            print("Cannot index without sentence-transformers library!")
            return

        # Check if we can load from cache
        if not force_reindex and os.path.exists(self.cache_file):
            print("Loading from cache...")
            with open(self.cache_file, 'rb') as f:
                data = pickle.load(f)
                self.documents = data['documents']
                self.embeddings = data['embeddings']
            print(f"✓ Loaded {len(self.documents)} cached documents")
            return

        print(f"\n{'='*80}")
        print("INDEXING TEXT FILES FOR VECTOR SEARCH")
        print(f"{'='*80}\n")

        if not self.extracted_text_dir.exists():
            print(f"⚠️  Directory not found: {self.extracted_text_dir}")
            print("Please run 'python extract_pdf_content.py' first")
            return

        self.documents = []
        all_texts = []

        # Find all text files
        book_dirs = [d for d in self.extracted_text_dir.iterdir() if d.is_dir()]

        if not book_dirs:
            print("⚠️  No book directories found in extracted_text/")
            return

        print(f"Found {len(book_dirs)} books to index\n")

        # Process each book
        for book_dir in book_dirs:
            full_text_path = book_dir / 'full_text.txt'

            if not full_text_path.exists():
                print(f"⚠️  Skipping {book_dir.name} - no full_text.txt")
                continue

            print(f"Processing: {book_dir.name}")

            with open(full_text_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Split by page markers
            pages = content.split('=' * 80)

            for page_section in pages:
                if not page_section.strip():
                    continue

                page_num = self.extract_page_number(page_section)

                # Chunk the page content
                chunks = self.chunk_text(page_section, chunk_size=400)

                for chunk in chunks:
                    if len(chunk.strip()) < 50:  # Skip very short chunks
                        continue

                    self.documents.append({
                        'book': book_dir.name,
                        'page': page_num,
                        'text': chunk.strip()
                    })
                    all_texts.append(chunk.strip())

            print(f"  ✓ Indexed {len([d for d in self.documents if d['book'] == book_dir.name])} chunks")

        print(f"\n{'='*80}")
        print(f"Total documents indexed: {len(self.documents)}")
        print(f"{'='*80}\n")

        # Create embeddings
        print("Creating vector embeddings (this may take a minute)...")
        self.embeddings = self.model.encode(all_texts, show_progress_bar=True, convert_to_numpy=True)

        # Cache the results
        print("\nSaving to cache...")
        with open(self.cache_file, 'wb') as f:
            pickle.dump({
                'documents': self.documents,
                'embeddings': self.embeddings
            }, f)

        print("✓ Indexing complete!")

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Semantic search using vector similarity.
        Returns top_k most relevant documents.
        """
        if not EMBEDDINGS_AVAILABLE:
            print("Vector search not available!")
            return []

        if self.embeddings is None or len(self.documents) == 0:
            print("⚠️  No indexed documents. Run index_all_files() first.")
            return []

        # Encode the query
        query_embedding = self.model.encode([query], convert_to_numpy=True)[0]

        # Calculate cosine similarity
        similarities = np.dot(self.embeddings, query_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
        )

        # Get top-k results
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                'book': self.documents[idx]['book'],
                'page': self.documents[idx]['page'],
                'text': self.documents[idx]['text'],
                'similarity': float(similarities[idx])
            })

        return results

    def search_within_book(self, query: str, book_name: str, top_k: int = 5) -> List[Dict]:
        """
        Search within a specific book only.
        """
        if self.embeddings is None:
            print("⚠️  No indexed documents.")
            return []

        # Filter documents by book
        book_indices = [i for i, doc in enumerate(self.documents) if doc['book'] == book_name]

        if not book_indices:
            print(f"⚠️  Book '{book_name}' not found in index")
            return []

        # Encode query
        query_embedding = self.model.encode([query], convert_to_numpy=True)[0]

        # Calculate similarities only for this book
        book_embeddings = self.embeddings[book_indices]
        similarities = np.dot(book_embeddings, query_embedding) / (
            np.linalg.norm(book_embeddings, axis=1) * np.linalg.norm(query_embedding)
        )

        # Get top results
        top_local_indices = np.argsort(similarities)[::-1][:top_k]
        top_indices = [book_indices[i] for i in top_local_indices]

        results = []
        for idx, local_idx in zip(top_indices, top_local_indices):
            results.append({
                'book': self.documents[idx]['book'],
                'page': self.documents[idx]['page'],
                'text': self.documents[idx]['text'],
                'similarity': float(similarities[local_idx])
            })

        return results

    def get_statistics(self) -> Dict:
        """Get indexing statistics"""
        if not self.documents:
            return {'total_documents': 0, 'books': []}

        books = {}
        for doc in self.documents:
            book_name = doc['book']
            books[book_name] = books.get(book_name, 0) + 1

        return {
            'total_documents': len(self.documents),
            'total_books': len(books),
            'books': books
        }


def interactive_search():
    """Interactive search interface"""

    print("\n" + "="*80)
    print("VECTOR SEARCH - SEMANTIC SEARCH ENGINE")
    print("="*80 + "\n")

    # Initialize search engine
    engine = VectorSearchEngine()

    # Check if we need to index
    if not os.path.exists(engine.cache_file):
        print("First time setup - indexing all files...")
        engine.index_all_files()
    else:
        # Load from cache
        engine.index_all_files(force_reindex=False)

    if len(engine.documents) == 0:
        print("\n⚠️  No documents indexed!")
        print("Make sure you've run 'python extract_pdf_content.py' first")
        return

    # Show statistics
    stats = engine.get_statistics()
    print(f"\n📊 Database Statistics:")
    print(f"   Total chunks indexed: {stats['total_documents']}")
    print(f"   Books: {stats['total_books']}")
    for book, count in stats['books'].items():
        print(f"      - {book}: {count} chunks")

    # Search loop
    while True:
        print(f"\n{'='*80}")
        print("SEARCH OPTIONS")
        print(f"{'='*80}")
        print("1. Semantic search (all books)")
        print("2. Search within specific book")
        print("3. Re-index files (if you added new ones)")
        print("4. Show statistics")
        print("5. Exit")

        choice = input("\nSelect option: ").strip()

        if choice == '1':
            query = input("\nEnter your search query: ").strip()
            if not query:
                continue

            top_k = input("Number of results (default 5): ").strip()
            top_k = int(top_k) if top_k.isdigit() else 5

            print(f"\nSearching for: '{query}'...\n")
            results = engine.search(query, top_k=top_k)

            print(f"{'='*80}")
            print(f"SEARCH RESULTS ({len(results)} found)")
            print(f"{'='*80}\n")

            for i, result in enumerate(results, 1):
                print(f"[{i}] Book: {result['book']}")
                print(f"    Page: {result['page'] if result['page'] else 'Unknown'}")
                print(f"    Similarity: {result['similarity']:.2%}")
                print(f"    Text: {result['text'][:300]}...")
                print("-" * 80)

        elif choice == '2':
            # Show available books
            stats = engine.get_statistics()
            print("\nAvailable books:")
            books = list(stats['books'].keys())
            for i, book in enumerate(books, 1):
                print(f"  {i}. {book}")

            book_choice = input("\nSelect book number: ").strip()
            if not book_choice.isdigit() or int(book_choice) < 1 or int(book_choice) > len(books):
                print("Invalid selection!")
                continue

            selected_book = books[int(book_choice) - 1]

            query = input("\nEnter your search query: ").strip()
            if not query:
                continue

            results = engine.search_within_book(query, selected_book, top_k=5)

            print(f"\n{'='*80}")
            print(f"RESULTS IN: {selected_book}")
            print(f"{'='*80}\n")

            for i, result in enumerate(results, 1):
                print(f"[{i}] Page: {result['page'] if result['page'] else 'Unknown'}")
                print(f"    Similarity: {result['similarity']:.2%}")
                print(f"    Text: {result['text'][:300]}...")
                print("-" * 80)

        elif choice == '3':
            print("\nRe-indexing all files...")
            engine.index_all_files(force_reindex=True)

        elif choice == '4':
            stats = engine.get_statistics()
            print(f"\n📊 Database Statistics:")
            print(f"   Total chunks: {stats['total_documents']}")
            print(f"   Books: {stats['total_books']}")
            for book, count in stats['books'].items():
                print(f"      - {book}: {count} chunks")

        elif choice == '5':
            print("\nGoodbye!")
            break


if __name__ == '__main__':
    if not EMBEDDINGS_AVAILABLE:
        print("\nPlease install required library:")
        print("  pip install sentence-transformers")
        exit(1)

    interactive_search()
