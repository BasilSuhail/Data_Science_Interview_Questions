"""
Creates a CSV file from your extracted text files
Simple - no AI needed, just text!
"""

import csv
from pathlib import Path

print("Creating CSV file...")

# Create CSV file
with open('supabase_data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)

    # Write header (matches Supabase table)
    writer.writerow(['book_name', 'page_number', 'content'])

    total_rows = 0

    # Process each book
    for book_dir in Path('extracted_text').glob('*'):
        if not book_dir.is_dir():
            continue

        print(f"\nProcessing: {book_dir.name}")

        text_file = book_dir / 'full_text.txt'
        if not text_file.exists():
            print(f"  No full_text.txt found, skipping...")
            continue

        # Read the text
        text = text_file.read_text(encoding='utf-8')

        # Split into chunks (2000 characters each)
        chunk_size = 2000
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

        # Write each chunk as a row
        for i, chunk in enumerate(chunks, 1):
            # Skip very short chunks
            if len(chunk.strip()) < 100:
                continue

            writer.writerow([
                book_dir.name.replace('_', ' '),  # Clean book name
                i,                                 # Page/chunk number
                chunk.strip()                      # Content
            ])
            total_rows += 1

        print(f"  Added {len([c for c in chunks if len(c.strip()) >= 100])} chunks")

print(f"\n✓ Done!")
print(f"✓ Created: supabase_data.csv")
print(f"✓ Total rows: {total_rows}")
print(f"\nNext: Upload this CSV to Supabase (see README.md)")
