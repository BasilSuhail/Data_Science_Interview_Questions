# Data Science Interview Questions - Simple Search

Search through data science books with Supabase. No complicated setup!

---

## ✅ What You Have

1. ✅ **supabase_data.csv** - 2,343 rows ready to upload
2. ✅ **simple_search.html** - Search interface
3. ✅ **SIMPLE_SUPABASE.sql** - Database setup

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Setup Supabase Database

1. Go to https://supabase.com and sign up
2. Create a new project
3. Go to **SQL Editor** (left sidebar)
4. Copy ALL text from `SIMPLE_SUPABASE.sql`
5. Paste and click **Run**

### Step 2: Upload CSV File

1. In Supabase, go to **Table Editor** (left sidebar)
2. Click on **"documents"** table
3. Click **"Insert"** → **"Import data from CSV"**
4. Select `supabase_data.csv`
5. Wait 1-2 minutes for upload
6. Done! You now have 2,343 searchable chunks!

### Step 3: Update Search Page

1. In Supabase, go to **Settings** → **API**
2. Copy your **Project URL** and **anon public key**
3. Open `simple_search.html`
4. Lines 123-124: Paste your credentials
5. Save and open in browser!

**Done!** 🎉

---

## 📁 Files You Need

```
.
├── SIMPLE_SUPABASE.sql      # Step 1: Database setup
├── supabase_data.csv        # Step 2: Upload this
├── simple_search.html       # Step 3: Search interface
├── create_csv.py            # (Optional) Regenerate CSV
└── README.md                # This file
```

---

## 📚 Your Data

- **Books**: 6 data science books
- **Total chunks**: 2,343
- **Each chunk**: ~2000 characters
- **Topics**: ML, Stats, Python, Math, Data Structures

**Books included:**
1. Introduction to Data Science (256 chunks)
2. Python for Data Science (261 chunks)
3. A Mathematical Introduction to Data Science (387 chunks)
4. An Introduction to Statistics and Machine Learning (355 chunks)
5. Data Science: Foundations (410 chunks)
6. Materials Data Science (674 chunks)

---

## 🆕 Adding More Books

### Step 1: Add PDF to "Books used" folder

Put your new PDF in the `Books used/` folder.

### Step 2: Extract text

```bash
python3 extract_pdf_content.py
```

This creates a new folder in `extracted_text/` with the book's text.

### Step 3: Create new CSV

```bash
python3 create_csv.py
```

This creates a fresh `supabase_data.csv` with ALL books (old + new).

### Step 4: Upload to Supabase

**Option A: Replace all data**
1. Supabase → Table Editor → documents table
2. Select all rows → Delete
3. Import new CSV

**Option B: Add only new book**
1. Manually edit `create_csv.py` to only process the new book
2. Generate CSV
3. Import (will append to existing data)

---

## 🔍 Using the Search

**Try these searches:**
- "machine learning"
- "python list"
- "statistics"
- "neural network"
- "data cleaning"

The search highlights matching text in yellow!

---

## 🌐 Make It Public

### Deploy on Netlify (Free!)

1. Push your code to GitHub
2. Go to https://netlify.com
3. **New site** → Connect to GitHub
4. Select your repo
5. Deploy!

Your search will be live at: `https://your-site.netlify.app`

**OR simply:**
1. Go to https://netlify.com
2. Drag and drop `simple_search.html`
3. Done!

---

## 💡 How It Works

```
PDF Books
   ↓
Extract Text (extract_pdf_content.py)
   ↓
Create CSV (create_csv.py)
   ↓
Upload to Supabase
   ↓
Search with HTML page
```

**Simple keyword search** - No AI needed, just plain text matching!

---

## 🛠️ Troubleshooting

**"No results found"**
- Try simpler keywords
- Make sure CSV was uploaded
- Check Supabase Table Editor has data

**"Error: relation documents does not exist"**
- Run the SQL script again

**Want to add more books?**
- See "Adding More Books" section above

**Search too slow?**
- Add indexes in Supabase (already in SQL script)
- Limit results to 10 instead of 20

---

## 📊 Supabase Table Structure

| Column | Type | Description |
|--------|------|-------------|
| id | bigserial | Auto-generated ID |
| book_name | text | Name of the book |
| page_number | integer | Chunk number |
| content | text | The actual text |
| embedding | vector(384) | (Optional, for AI search) |

**Note:** The CSV upload only fills the first 3 columns. That's all you need for basic search!

---

## 🎯 Next Steps

- ✅ Add more books
- ✅ Share search page with friends
- ✅ Deploy to Netlify
- ✅ Customize the design
- ⬜ Add filters by book name
- ⬜ Add download/export feature

---

Built with Supabase 🚀

Questions? Check `SIMPLE_INSTRUCTIONS.md`
