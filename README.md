# AI Interview Coach for Data Science Jobs

Personalized interview practice tailored to your experience level, target companies, and weak areas.

---

## 🚀 Quick Start

### Step 1: Set Up Configuration

1. Copy `config.example.js` to `config.js`:
   ```bash
   cp config.example.js config.js
   ```

2. Get a free Groq API key from https://console.groq.com/keys

3. Add your API key to `config.js`:
   ```javascript
   const CONFIG = {
       GROQ_API_KEY: 'your_actual_key_here'
   };
   ```

**⚠️ IMPORTANT:** Never commit `config.js` to Git! It's already in `.gitignore`.

### Step 2: Open the App

Simply open `index.html` in any web browser. No server needed!

---

## 🎯 Features

### ✅ Personalized Question Generation
- **Experience-Level Targeting**: Junior, Mid-Level, or Senior questions
- **Company-Specific Practice**: Questions tailored to Meta, Google, Amazon, etc.
- **Focus Area Weighting**: More questions from your weak areas
- **Interview Urgency**: Different prep based on days until interview

### ✅ Interview Type Selector
- Mixed Practice (all types)
- Coding Interviews (Python, SQL, algorithms)
- Statistics & Probability
- Machine Learning Algorithms
- Case Studies
- Behavioral Questions

### ✅ Smart Answer System
- Click any question to see detailed explanations
- Answers pulled from 10 data science textbooks using RAG
- Includes tables, formulas, and examples

---

## 📚 Database Content

**Current Books (10 total, 3,983 pages):**

**Core Interview Prep:**
- ✅ Introduction to Statistical Learning (ISLR) - 617 pages
- ✅ OpenIntro Statistics - 465 pages
- ✅ Think Stats - 141 pages

**Foundational Content:**
- A Mathematical Introduction to Data Science - 486 pages
- An Introduction to Statistics and Machine Learning - 371 pages
- Data Science in Practice - 199 pages
- Data Science: Foundations with R - 422 pages
- Introduction to Data Science - 255 pages
- Materials Data Science - 629 pages
- Python for Data Science - 398 pages

**Coverage:**
- ✅ Statistics & Hypothesis Testing: 80%
- ✅ Machine Learning Algorithms: 75%
- ✅ Probability Distributions: 85%
- ✅ Linear/Logistic Regression: 90%
- ⚠️ SQL: 0% (needs addition)
- ⚠️ Business Metrics: 20%

---

## 📤 Uploading Database to Supabase

### Option A: Supabase Dashboard (Easiest)

1. Go to https://supabase.com and open your project
2. Navigate to **Table Editor** → **documents** table
3. Click **Insert** → **Import data from CSV**
4. Select `supabase_dataset.csv`
5. Map columns: `book_name`, `page_number`, `content`
6. Click **Import**
7. Done! (May take 2-3 minutes for 3,983 rows)

### Option B: Supabase CLI (Advanced)

```bash
supabase db reset
supabase db push
# Then import CSV via dashboard
```

---

## 🔧 Adding More Books

### Step 1: Add PDF Books

Put new PDF files in the `Books used/` folder

### Step 2: Extract Content

```bash
cd "Data Science Interview Questions"
source venv/bin/activate
pip install pdfplumber pillow  # First time only
python add_books_enhanced.py
```

This creates `supabase_dataset.csv` with enhanced table extraction.

### Step 3: Upload to Supabase

Follow the upload instructions above.

**Recommended Books to Add:**
- SQL for Data Scientists (critical - 85% of interviews)
- Hands-On Machine Learning (Aurélien Géron)
- Trustworthy Online Controlled Experiments (A/B testing)
- Cracking the Coding Interview (data structures chapter)

---

## 🎨 UI Features

### Clean, Modern Design
- Dark/Light mode toggle
- Responsive layout (works on mobile)
- Smooth animations
- Accordion-style answers (expand/collapse inline)

### User Profile System
- Save experience level
- Track target companies (30+ pre-defined)
- Mark weak areas for focused practice
- Interview countdown with urgency indicators

### Onboarding Flow
- First-time visitor modal
- Setup profile wizard
- Profile summary always visible

---

## 🛠️ Technical Stack

- **Frontend**: Pure HTML/CSS/JavaScript (no frameworks)
- **AI**: Groq API (llama-3.3-70b-versatile)
- **Database**: Supabase (PostgreSQL)
- **RAG Architecture**: Keyword extraction + relevance scoring
- **PDF Extraction**: pdfplumber (with table support)

---

## 📊 Project Status

**Phase 1: Foundation** ✅ 90% Complete
- [x] User Profile System
- [x] Personalized Question Generation
- [x] Interview Type Selector
- [x] Onboarding Modal
- [x] Database Upgrade (3 critical books added)
- [x] Enhanced table extraction

**Phase 2: Personalized Practice** ⏳ 40% Complete
- [x] Experience-level targeting
- [x] Company-specific patterns
- [x] Focus area weighting
- [ ] Performance history tracking
- [ ] Real interview questions database

**Phase 3: Mock Interview Simulator** ❌ Not Started
- [ ] Timed practice sessions
- [ ] Mixed question types
- [ ] Performance analytics

See `THE ROADMAP.md` for full project plan.

---

## 🐛 Known Issues

- ❌ No SQL coverage in database (need to add SQL textbook)
- ⚠️ Images/charts not extracted from PDFs (only text + tables)
- ⚠️ Mathematical formulas may be partially garbled

---

## 📝 License

Personal project - not for commercial distribution.

---

Built with ❤️ to help people ace data science interviews
