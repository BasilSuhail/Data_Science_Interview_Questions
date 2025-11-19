# 🚀 AI Interview Coach - Setup Guide

**Get your AI Interview Coach running in 5 minutes!**

---

## Prerequisites

- Python 3.8+
- Supabase account (you already have this!)
- Gemini API key (free)

---

## Step 1: Install Dependencies

```bash
cd ai_coach/
pip install -r requirements.txt
```

**What gets installed:**
- `google-genai` - Gemini AI SDK
- `supabase` - Database client
- `python-dotenv` - Environment variables

---

## Step 2: Get Your Gemini API Key

1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key (starts with `AIza...`)

**Free tier includes:**
- 15 requests per minute
- 1,500 requests per day
- More than enough for interview practice!

---

## Step 3: Configure Environment Variables

### Option A: Using .env file (Recommended)

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use any text editor
```

Fill in:
```bash
SUPABASE_URL=https://iteavenjozhzxupbxosu.supabase.co
SUPABASE_KEY=your-actual-key-here
GEMINI_API_KEY=AIza...your-gemini-key
```

### Option B: Export variables

```bash
export SUPABASE_URL="https://iteavenjozhzxupbxosu.supabase.co"
export SUPABASE_KEY="your-supabase-key"
export GEMINI_API_KEY="your-gemini-key"
```

---

## Step 4: Test the Setup

Run the basic example:

```bash
python examples/basic_usage.py
```

**Expected output:**
```
✅ Connected to Supabase database
✅ Gemini evaluator ready

🎯 AI INTERVIEW COACH - Basic Usage Example

📋 Fetching medium ml question from database...

❓ QUESTION:
What is the difference between supervised and unsupervised learning?

💭 Your answer:
(Type your answer here...)
```

---

## Step 5: Try Different Examples

### Example 1: Basic Interview
```bash
python examples/basic_usage.py
```

### Example 2: Practice Session (3 questions)
```bash
python examples/practice_session.py
```

### Example 3: Batch Evaluation
```bash
python examples/batch_evaluation.py
```

---

## 🎯 Quick Reference

### Question Types Available
- `ml` - Machine Learning (264 questions)
- `stats` - Statistics (61 questions)
- `sql` - SQL/Database (22 questions)
- `coding` - Coding/Algorithms (28 questions)
- `case` - Case Studies (61 questions)
- `behavioral` - Behavioral (5 questions)
- `mixed` - Mixed Topics (109 questions)

### Difficulty Levels
- `easy` - 52 questions
- `medium` - 309 questions
- `hard` - 189 questions

### Topics Available
- `machine_learning`
- `deep_learning`
- `nlp`
- `computer_vision`
- `sequence_models`
- `sql_database`
- `data_science`

---

## 🐛 Troubleshooting

### Error: "Module not found: google.genai"
```bash
pip install google-genai
```

### Error: "Module not found: supabase"
```bash
pip install supabase
```

### Error: "Gemini API key required"
Check that:
1. You set `GEMINI_API_KEY` in `.env` or environment
2. The key is valid (test at https://aistudio.google.com)

### Error: "Supabase credentials not found"
Check that:
1. `SUPABASE_URL` and `SUPABASE_KEY` are set
2. The URL is correct (should end with `.supabase.co`)

### Questions not loading
Make sure you've uploaded your questions to Supabase:
1. Check if tables exist in Supabase dashboard
2. Verify data is in `interview_questions` table
3. See main project [UPLOAD_READY.md](../UPLOAD_READY.md)

---

## 📖 Next Steps

### Option 1: Interactive Use

Create your own script:

```python
from ai_coach.interview_coach import InterviewCoach

coach = InterviewCoach()

# Start practicing!
coach.conduct_interview(
    question_type="ml",
    difficulty="hard",
    role="Senior Data Scientist"
)
```

### Option 2: Jupyter Notebook

Great for experimentation:

```python
# In Jupyter:
from ai_coach.interview_coach import InterviewCoach
import os

# Set credentials
os.environ["SUPABASE_URL"] = "your-url"
os.environ["SUPABASE_KEY"] = "your-key"
os.environ["GEMINI_API_KEY"] = "your-key"

# Initialize
coach = InterviewCoach()

# Practice
result = coach.conduct_interview("ml", "medium")
```

### Option 3: Build a Web App

Use Streamlit or Flask to create a UI:
- Question selection interface
- Text area for answers
- Real-time evaluation display
- Progress tracking

See [README.md](README.md) for more details.

---

## 💡 Tips for Best Results

1. **Be Specific** - Give detailed answers, not just definitions
2. **Use Examples** - Gemini rewards concrete examples
3. **Explain Why** - Don't just say what, explain why
4. **Structure Answers** - Use clear paragraphs or bullet points
5. **Review Feedback** - Read improvements carefully

---

## 🎉 You're All Set!

Your AI Interview Coach is ready:

✅ 552 curated questions from 11 sources
✅ AI-powered answer evaluation
✅ Instant feedback and scoring
✅ 3,983 textbook pages for reference

**Start practicing:**

```bash
python examples/practice_session.py
```

**Good luck with your interviews!** 🚀
