# Simple Instructions - 3 Steps Only!

## What You Need

1. ✅ `SIMPLE_SUPABASE.sql` - Database setup
2. ✅ `simple_upload.py` - Upload your data
3. ✅ `simple_search.html` - Search interface

---

## Step 1: Setup Supabase (5 minutes)

### 1.1 Create Account
- Go to https://supabase.com
- Sign up with GitHub

### 1.2 Create Project
- Click "New Project"
- Name it whatever you want
- Choose a password
- Wait 2 minutes for setup

### 1.3 Run SQL Script
- In Supabase dashboard, click **"SQL Editor"** (left sidebar)
- Click **"New Query"**
- Open the file `SIMPLE_SUPABASE.sql`
- Copy ALL the text
- Paste into SQL Editor
- Click **"Run"**
- Done! ✅

### 1.4 Get Your Keys
- Click **⚙️ Settings** (left sidebar)
- Click **"API"**
- Copy these two things:
  - **Project URL** (looks like: https://xxxxx.supabase.co)
  - **anon public key** (long string starting with eyJ...)
  - **service_role key** (another long string)

---

## Step 2: Upload Your Data (10 minutes)

### 2.1 Install Python Libraries
```bash
pip install supabase sentence-transformers
```

### 2.2 Edit simple_upload.py
- Open `simple_upload.py`
- Line 9: Paste your Project URL
- Line 10: Paste your service_role key
- Save

### 2.3 Run It
```bash
python simple_upload.py
```

Wait 5-10 minutes. It will upload your data.

---

## Step 3: Use the Search (1 minute)

### 3.1 Edit simple_search.html
- Open `simple_search.html`
- Line 69: Paste your Project URL
- Line 70: Paste your anon public key
- Save

### 3.2 Open It
- Double-click `simple_search.html`
- Opens in your browser
- Type a question
- Click Search!

---

## That's It!

You now have:
- ✅ Database with vector search
- ✅ Your data uploaded
- ✅ Working search interface

---

## To Make It Public (Optional)

### Upload simple_search.html to Netlify:
1. Go to https://netlify.com
2. Drag and drop `simple_search.html`
3. Get a public URL
4. Share with anyone!

---

## Troubleshooting

**"No results found"**
- Make sure you ran `python simple_upload.py`
- Check Supabase Table Editor → "documents" table has data

**"Error: relation documents does not exist"**
- Run the SQL script again in Supabase SQL Editor

**"Import error"**
- Run: `pip install supabase sentence-transformers`

---

That's all you need! 🎉
