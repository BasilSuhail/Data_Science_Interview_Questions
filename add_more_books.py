"""
Simple script to add more books to your Data Science search database.

HOW TO USE:
1. Put your new PDF books in the "Books used" folder
2. Install required package: pip install PyPDF2
3. Run this script: python add_more_books.py
4. It will create a new CSV file called "new_books_data.csv"
5. Upload the CSV to Supabase using the upload script

The script will:
- Read all PDFs from "Books used" folder
- Extract text from each page
- Split into chunks (each page = 1 chunk)
- Create CSV with columns: book_name, page_number, content
"""

import os
import csv
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file, page by page."""
    print(f"  Processing: {os.path.basename(pdf_path)}")

    try:
        reader = PdfReader(pdf_path)
        pages_text = []

        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            if text.strip():  # Only add non-empty pages
                pages_text.append({
                    'page_number': page_num,
                    'content': text.strip()
                })

        print(f"    ✓ Extracted {len(pages_text)} pages")
        return pages_text

    except Exception as e:
        print(f"    ✗ Error: {str(e)}")
        return []

def create_csv_from_books(books_folder="Books used", output_file="new_books_data.csv"):
    """
    Create a CSV file from all PDF books in the specified folder.

    Args:
        books_folder: Folder containing PDF files (default: "Books used")
        output_file: Name of output CSV file (default: "new_books_data.csv")
    """

    print(f"\n🔍 Looking for PDF files in '{books_folder}' folder...\n")

    # Check if folder exists
    if not os.path.exists(books_folder):
        print(f"❌ Error: Folder '{books_folder}' not found!")
        print(f"   Please create it and add your PDF books there.")
        return

    # Find all PDF files
    pdf_files = [f for f in os.listdir(books_folder) if f.lower().endswith('.pdf')]

    if not pdf_files:
        print(f"❌ No PDF files found in '{books_folder}' folder!")
        print(f"   Please add some PDF books and try again.")
        return

    print(f"📚 Found {len(pdf_files)} PDF file(s):\n")

    # Prepare CSV data
    all_data = []

    # Process each PDF
    for pdf_file in pdf_files:
        pdf_path = os.path.join(books_folder, pdf_file)
        book_name = os.path.splitext(pdf_file)[0]  # Remove .pdf extension

        pages = extract_text_from_pdf(pdf_path)

        # Add to data
        for page in pages:
            all_data.append({
                'book_name': book_name,
                'page_number': page['page_number'],
                'content': page['content']
            })

    # Write to CSV
    if all_data:
        print(f"\n📝 Writing {len(all_data)} chunks to '{output_file}'...")

        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['book_name', 'page_number', 'content'])
            writer.writeheader()
            writer.writerows(all_data)

        print(f"✅ Success! Created '{output_file}' with {len(all_data)} chunks from {len(pdf_files)} book(s)")
        print(f"\n📤 Next steps:")
        print(f"   1. Upload '{output_file}' to Supabase")
        print(f"   2. Use the upload script or Supabase dashboard")
        print(f"   3. Your search will now include the new books!")
    else:
        print(f"\n❌ No data extracted. Please check your PDF files.")

if __name__ == "__main__":
    print("=" * 60)
    print("  📖 Add More Books to Data Science Search")
    print("=" * 60)

    # Run the extraction
    create_csv_from_books()

    print("\n" + "=" * 60)
