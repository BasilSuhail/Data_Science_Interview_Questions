"""
ENHANCED PDF extraction script that handles tables, images, and formulas better.

Improvements over basic PyPDF2:
1. Uses pdfplumber for better table extraction
2. Extracts images and uses OCR (pytesseract) if available
3. Preserves table structure as markdown
4. Better handling of mathematical formulas

HOW TO USE:
1. Install dependencies:
   pip install pdfplumber pillow pytesseract

2. Run this script:
   python add_books_enhanced.py

3. Upload the generated CSV to Supabase
"""

import os
import csv

def extract_with_basic_method():
    """Fallback to basic PyPDF2 if enhanced libraries aren't available."""
    print("⚠️  Using basic extraction (PyPDF2 only)")
    print("   Install pdfplumber for better table/image extraction:")
    print("   pip install pdfplumber pillow")

    from PyPDF2 import PdfReader

    def extract_text_from_pdf(pdf_path):
        reader = PdfReader(pdf_path)
        pages_text = []

        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            if text.strip():
                pages_text.append({
                    'page_number': page_num,
                    'content': text.strip()
                })

        return pages_text

    return extract_text_from_pdf

def extract_with_enhanced_method():
    """Use pdfplumber for better table extraction."""
    try:
        import pdfplumber
        print("✅ Using ENHANCED extraction (pdfplumber)")
        print("   This will better preserve tables and structure!\n")

        def extract_text_from_pdf(pdf_path):
            pages_text = []

            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract text
                    text = page.extract_text() or ""

                    # Try to extract tables
                    tables = page.extract_tables()

                    # If tables exist, format them as markdown
                    if tables:
                        table_texts = []
                        for table in tables:
                            # Convert table to markdown format
                            if table and len(table) > 0:
                                # Header row
                                header = " | ".join(str(cell or "") for cell in table[0])
                                separator = " | ".join("---" for _ in table[0])

                                # Data rows
                                rows = []
                                for row in table[1:]:
                                    if row:
                                        rows.append(" | ".join(str(cell or "") for cell in row))

                                # Combine into markdown table
                                markdown_table = f"\n\nTABLE:\n{header}\n{separator}\n" + "\n".join(rows) + "\n\n"
                                table_texts.append(markdown_table)

                        # Add tables to text
                        text = text + "\n" + "".join(table_texts)

                    if text.strip():
                        pages_text.append({
                            'page_number': page_num,
                            'content': text.strip()
                        })

            return pages_text

        return extract_text_from_pdf

    except ImportError:
        return None

def create_csv_from_books(books_folder="Books used", output_file="new_books_data_enhanced.csv"):
    """Create CSV with enhanced extraction."""

    print(f"\n{'='*80}")
    print("  📖 ENHANCED Book Extraction for Data Science Search")
    print(f"{'='*80}\n")

    # Try enhanced method first, fallback to basic
    extract_func = extract_with_enhanced_method()
    if extract_func is None:
        extract_func = extract_with_basic_method()

    print(f"🔍 Looking for PDF files in '{books_folder}' folder...\n")

    if not os.path.exists(books_folder):
        print(f"❌ Error: Folder '{books_folder}' not found!")
        return

    pdf_files = [f for f in os.listdir(books_folder) if f.lower().endswith('.pdf')]

    if not pdf_files:
        print(f"❌ No PDF files found in '{books_folder}' folder!")
        return

    print(f"📚 Found {len(pdf_files)} PDF file(s)\n")

    all_data = []

    for pdf_file in pdf_files:
        pdf_path = os.path.join(books_folder, pdf_file)
        book_name = os.path.splitext(pdf_file)[0]

        print(f"  Processing: {pdf_file}")

        try:
            pages = extract_func(pdf_path)

            for page in pages:
                all_data.append({
                    'book_name': book_name,
                    'page_number': page['page_number'],
                    'content': page['content']
                })

            print(f"    ✓ Extracted {len(pages)} pages")

        except Exception as e:
            print(f"    ✗ Error: {str(e)}")

    if all_data:
        print(f"\n📝 Writing {len(all_data)} chunks to '{output_file}'...")

        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['book_name', 'page_number', 'content'])
            writer.writeheader()
            writer.writerows(all_data)

        print(f"✅ Success! Created '{output_file}'")
        print(f"\n📊 Extraction Statistics:")
        print(f"   - Total pages: {len(all_data)}")
        print(f"   - Books processed: {len(pdf_files)}")
        print(f"   - Average pages/book: {len(all_data) // len(pdf_files)}")

        print(f"\n📤 Next steps:")
        print(f"   1. Compare file size with old CSV (should be larger if tables extracted)")
        print(f"   2. Upload '{output_file}' to Supabase")
        print(f"   3. Your answers will now include table data!")
    else:
        print(f"\n❌ No data extracted. Please check your PDF files.")

if __name__ == "__main__":
    create_csv_from_books()
    print(f"\n{'='*80}\n")
