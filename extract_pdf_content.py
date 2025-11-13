import os
import sqlite3
from pathlib import Path

try:
    import PyPDF2
    PDF_LIBRARY = 'PyPDF2'
except ImportError:
    try:
        import pdfplumber
        PDF_LIBRARY = 'pdfplumber'
    except ImportError:
        print("⚠️  No PDF library found!")
        print("Please install one of these:")
        print("  pip install PyPDF2")
        print("  OR")
        print("  pip install pdfplumber")
        exit(1)


def extract_text_pypdf2(pdf_path):
    """Extract text from PDF using PyPDF2"""
    text_by_page = []

    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)

            print(f"  Extracting {total_pages} pages...")

            for page_num in range(total_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                text_by_page.append({
                    'page': page_num + 1,
                    'text': text
                })

                if (page_num + 1) % 10 == 0:
                    print(f"  Progress: {page_num + 1}/{total_pages} pages")

            return text_by_page, total_pages
    except Exception as e:
        print(f"  ✗ Error extracting PDF: {e}")
        return [], 0


def extract_text_pdfplumber(pdf_path):
    """Extract text from PDF using pdfplumber (usually better quality)"""
    text_by_page = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)

            print(f"  Extracting {total_pages} pages...")

            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                text_by_page.append({
                    'page': page_num + 1,
                    'text': text if text else ""
                })

                if (page_num + 1) % 10 == 0:
                    print(f"  Progress: {page_num + 1}/{total_pages} pages")

            return text_by_page, total_pages
    except Exception as e:
        print(f"  ✗ Error extracting PDF: {e}")
        return [], 0


def save_extracted_text(book_title, text_by_page, output_dir='extracted_text'):
    """Save extracted text to individual text files"""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Create a subdirectory for this book
    book_dir = os.path.join(output_dir, book_title.replace(' ', '_').replace('.pdf', ''))
    os.makedirs(book_dir, exist_ok=True)

    # Save all text to a single file
    all_text_path = os.path.join(book_dir, 'full_text.txt')
    with open(all_text_path, 'w', encoding='utf-8') as f:
        for page_data in text_by_page:
            f.write(f"\n{'='*80}\n")
            f.write(f"PAGE {page_data['page']}\n")
            f.write(f"{'='*80}\n\n")
            f.write(page_data['text'])
            f.write("\n\n")

    print(f"  ✓ Saved full text to: {all_text_path}")

    return all_text_path


def register_book_in_database(title, filename, total_pages, status='extracted'):
    """Register the book in the database"""
    conn = sqlite3.connect('interview_questions.db')
    cursor = conn.cursor()

    # Check if book already exists
    cursor.execute('SELECT id FROM books WHERE filename = ?', (filename,))
    existing = cursor.fetchone()

    if existing:
        # Update existing record
        cursor.execute('''
            UPDATE books
            SET total_pages = ?, extraction_status = ?
            WHERE filename = ?
        ''', (total_pages, status, filename))
        print(f"  ✓ Updated book record in database")
    else:
        # Insert new record
        cursor.execute('''
            INSERT INTO books (title, filename, total_pages, extraction_status)
            VALUES (?, ?, ?, ?)
        ''', (title, filename, total_pages, status))
        print(f"  ✓ Registered book in database")

    conn.commit()
    conn.close()


def extract_all_pdfs(pdf_directory='Books used'):
    """Extract text from all PDFs in the specified directory"""

    print(f"\n{'='*80}")
    print(f"PDF TEXT EXTRACTION")
    print(f"{'='*80}\n")
    print(f"Using library: {PDF_LIBRARY}\n")

    # Get all PDF files
    pdf_path = Path(pdf_directory)
    pdf_files = list(pdf_path.glob('*.pdf'))

    if not pdf_files:
        print(f"⚠️  No PDF files found in '{pdf_directory}'")
        return

    print(f"Found {len(pdf_files)} PDF file(s):\n")

    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n[{i}/{len(pdf_files)}] Processing: {pdf_file.name}")
        print("-" * 80)

        # Extract text
        if PDF_LIBRARY == 'PyPDF2':
            text_by_page, total_pages = extract_text_pypdf2(pdf_file)
        else:
            text_by_page, total_pages = extract_text_pdfplumber(pdf_file)

        if text_by_page:
            # Save extracted text
            save_extracted_text(pdf_file.name, text_by_page)

            # Register in database
            register_book_in_database(
                title=pdf_file.stem,
                filename=pdf_file.name,
                total_pages=total_pages,
                status='extracted'
            )

            print(f"  ✓ Successfully processed '{pdf_file.name}'")
        else:
            print(f"  ✗ Failed to process '{pdf_file.name}'")

    print(f"\n{'='*80}")
    print("EXTRACTION COMPLETE!")
    print(f"{'='*80}\n")
    print("Next steps:")
    print("1. Check the 'extracted_text' folder for the extracted content")
    print("2. Run 'python curate_questions.py' to start identifying questions")


if __name__ == '__main__':
    # Make sure database exists
    if not os.path.exists('interview_questions.db'):
        print("⚠️  Database not found. Creating it now...")
        import create_database
        create_database.create_database()
        print()

    # Extract all PDFs
    extract_all_pdfs()
