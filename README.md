# Data Science Search - Intelligent Q&A System

Search through data science books with natural language questions and get smart, composed answers.

---

## 🚀 How to Start the App

### Step 1: Set Up Configuration File

1. Copy `config.example.js` to `config.js`:
   ```bash
   cp config.example.js config.js
   ```
   (Or manually copy the file if on Windows)

### Step 2: Get a Free Groq API Key

1. Go to https://console.groq.com/keys
2. Sign up for a free account
3. Create a new API key
4. Copy the key

### Step 3: Add Your API Key

1. Open `config.js` in a text editor
2. Replace `YOUR_GROQ_API_KEY_HERE` with your actual Groq API key
3. Save the file

**⚠️ IMPORTANT:** Never commit `config.js` to Git! It's already in `.gitignore` to protect your API key.

### Step 4: Open the App

1. Open `index.html` in any web browser
2. That's it!

---

## 📚 How to Add More Books

### Step 1: Install Python Package

```bash
pip install PyPDF2
```

### Step 2: Add PDF Books

Put your PDF files in the `Books used/` folder

### Step 3: Generate CSV

```bash
python add_more_books.py
```

This creates `new_books_data.csv`

### Step 4: Upload to Supabase

1. Go to https://supabase.com
2. Open your project → Table Editor → documents table
3. Click Insert → Import data from CSV
4. Select `new_books_data.csv`
5. Click Import

Done! Your new books are now searchable.

---

Built with Supabase & Intelligence 🚀
