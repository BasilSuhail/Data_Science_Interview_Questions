"""
Test script to check how PDFs with tables/images are being extracted.
This will help us understand what we're missing.
"""

from PyPDF2 import PdfReader
import os

def analyze_pdf_structure(pdf_path, sample_pages=[10, 50, 100]):
    """Analyze how tables and images appear in extracted text."""

    print(f"\n{'='*80}")
    print(f"Analyzing: {os.path.basename(pdf_path)}")
    print(f"{'='*80}\n")

    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)

    print(f"Total pages: {total_pages}")

    for page_num in sample_pages:
        if page_num >= total_pages:
            continue

        print(f"\n{'─'*80}")
        print(f"PAGE {page_num + 1} SAMPLE (first 500 chars):")
        print(f"{'─'*80}")

        page = reader.pages[page_num]
        text = page.extract_text()

        # Show sample
        print(text[:500])
        print("\n[... truncated ...]")

        # Check for table indicators
        has_table_keyword = any(keyword in text.lower() for keyword in ['table', 'figure', 'chart'])
        has_columns = '|' in text or '\t' in text
        has_numbers = any(char.isdigit() for char in text[:200])

        print(f"\nPage Analysis:")
        print(f"  - Contains 'table/figure/chart': {has_table_keyword}")
        print(f"  - Contains column separators (|, tabs): {has_columns}")
        print(f"  - Contains numbers (likely table data): {has_numbers}")
        print(f"  - Total characters extracted: {len(text)}")

if __name__ == "__main__":
    books_folder = "Books used"

    # Test the new critical books
    test_books = [
        "Introduction to Statistical Learning.pdf",
        "OpenIntro Statistics.pdf",
        "Think Stats.pdf"
    ]

    for book in test_books:
        pdf_path = os.path.join(books_folder, book)
        if os.path.exists(pdf_path):
            analyze_pdf_structure(pdf_path, sample_pages=[20, 50, 100])
        else:
            print(f"❌ Not found: {book}")

    print(f"\n{'='*80}")
    print("SUMMARY: How PyPDF2 handles tables/images")
    print(f"{'='*80}")
    print("""
PyPDF2 Limitations:
1. ❌ IMAGES: PyPDF2 cannot extract images - it only extracts text
2. ⚠️  TABLES: Tables are extracted as text, but formatting is often lost
3. ⚠️  COMPLEX LAYOUTS: Multi-column layouts may have jumbled text order
4. ⚠️  FORMULAS: Mathematical formulas may be extracted poorly or not at all

What gets extracted:
✅ Plain text (paragraphs, headings)
✅ Table data (but without structure - just numbers/text in a line)
✅ Some formatting (spacing preserved to some degree)

What gets LOST:
❌ Images, charts, graphs, diagrams
❌ Table borders and structure (becomes unformatted text)
❌ Mathematical notation (LaTeX, symbols)
❌ Visual layouts (columns, boxes, callouts)
""")
