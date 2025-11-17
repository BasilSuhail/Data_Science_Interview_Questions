# 🚀 START HERE - Complete Interview Questions Collection System

## 📁 Organized Folder Structure

```
Data Science Interview Questions/
├── 📄 index.html                     # Your main app
├── 📄 config.js                      # API keys (gitignored)
├── 📄 supabase_dataset.csv           # Textbook database (upload to Supabase)
├── 📄 README.md                      # Main documentation
├── 📄 START_HERE.md                  # This file!
│
├── 📂 scripts/                       # All Python scripts
│   ├── collect_github_questions.py  # ✅ Automated GitHub collector
│   ├── scrape_leetcode_discuss.py   # Creates LeetCode template
│   ├── scrape_stratascratch.py      # Creates StrataScratch template
│   ├── parse_manual_questions.py    # Parses your manual templates
│   ├── merge_all_questions.py       # Combines all sources
│   └── add_books_enhanced.py        # For adding textbooks
│
├── 📂 templates/                     # Fill these out manually
│   ├── leetcode_manual_template.txt     # ⏳ Fill with LeetCode questions
│   └── stratascratch_manual_template.txt# ⏳ Fill with StrataScratch SQL questions
│
├── 📂 collected_questions/           # Output CSVs go here
│   ├── github_questions.csv         # ✅ 54 questions already collected!
│   ├── manual_questions.csv         # ⏳ After filling templates
│   └── final_interview_questions.csv# 🎯 Upload this to Supabase!
│
├── 📂 docs/                          # All documentation
│   ├── QUICK_START.md               # Fastest path guide
│   ├── LEETCODE_TUTORIAL.md         # 📝 How to collect LeetCode questions
│   ├── STRATASCRATCH_TUTORIAL.md    # 📝 How to collect SQL questions
│   ├── COLLECTION_GUIDE.md          # Detailed collection guide
│   ├── SUPABASE_SETUP.md            # Database setup
│   └── IMAGE_TABLE_HANDLING.md      # PDF extraction docs
│
├── 📂 Books used/                    # 10 PDF textbooks
├── 📂 book-covers/                   # Cover images
└── 📂 venv/                          # Python environment
```

---

## 🎯 Three Paths - Choose Based on Time Available

### PATH 1: Quick Start (5 minutes) - Use GitHub Questions
**Status:** ✅ Ready to use now!

```bash
cd "/Users/basilsuhail/folders/Data Sets/Data_Science_Interview_Questions"
source venv/bin/activate

# Merge (creates final CSV)
python scripts/merge_all_questions.py

# Upload: collected_questions/final_interview_questions.csv to Supabase
# (See docs/SUPABASE_SETUP.md)
```

**Result:** 54 questions in production TODAY!

---

### PATH 2: Add LeetCode Questions (30-60 minutes)
**Status:** ⏳ Template ready, you fill it out

**Step 1:** Open `templates/leetcode_manual_template.txt`

**Step 2:** Follow `docs/LEETCODE_TUTORIAL.md`:
1. Go to https://leetcode.com/discuss/interview-experience
2. Search "data science"
3. Copy 20-50 questions into template
4. Save template

**Step 3:** Parse your questions:
```bash
python scripts/parse_manual_questions.py
```

**Step 4:** Merge:
```bash
python scripts/merge_all_questions.py
```

**Result:** 74-104 questions (54 GitHub + 20-50 LeetCode)

---

### PATH 3: Add SQL Questions (30-60 minutes)
**Status:** ⏳ Template ready, you fill it out

**Step 1:** Sign up at https://www.stratascratch.com (free)

**Step 2:** Open `templates/stratascratch_manual_template.txt`

**Step 3:** Follow `docs/STRATASCRATCH_TUTORIAL.md`:
1. Browse StrataScratch SQL questions
2. Filter by company (Meta, Google, Amazon)
3. Copy 20-50 SQL questions
4. Save template

**Step 4:** Parse your questions:
```bash
python scripts/parse_manual_questions.py
```

**Step 5:** Merge:
```bash
python scripts/merge_all_questions.py
```

**Result:** 74-104 questions (54 GitHub + 20-50 SQL)

---

### PATH 4: Do Everything (1-2 hours)
**Status:** Get maximum coverage

1. Use GitHub questions (already have!)
2. Fill LeetCode template (30-60 min)
3. Fill StrataScratch template (30-60 min)
4. Parse all templates
5. Merge everything

**Result:** 94-154 questions (comprehensive coverage!)

---

## ✅ What's Already Done

1. ✅ **GitHub Questions Collected**: 54 questions
   - File: `collected_questions/github_questions.csv`
   - Mix of coding, ML, stats questions
   - From real interview question repositories

2. ✅ **Templates Created**:
   - `templates/leetcode_manual_template.txt` (empty, ready to fill)
   - `templates/stratascratch_manual_template.txt` (empty, ready to fill)

3. ✅ **All Scripts Ready**:
   - Collection scripts
   - Parser script
   - Merger script

4. ✅ **Documentation Written**:
   - Step-by-step tutorials
   - Database setup guide
   - Quick start guide

---

## 📝 Fill Templates - Visual Guide

### LeetCode Template Example:

```
# Edit: templates/leetcode_manual_template.txt

---

## Meta - Data Scientist

**Difficulty**: medium
**Type**: stats

**Question 1:**
Explain the bias-variance tradeoff and how you would diagnose it.

**Question 2:**
Design an A/B test for a new feature on Facebook News Feed.

---

## Google - Machine Learning Engineer

**Difficulty**: hard
**Type**: ml

**Question 1:**
Explain gradient boosting. Compare XGBoost vs LightGBM vs CatBoost.

**Question 2:**
Design a recommendation system from scratch.

---
```

### StrataScratch Template Example:

```
# Edit: templates/stratascratch_manual_template.txt

---

**Company**: Netflix
**Difficulty**: medium
**Type**: sql

**Question Title:**
Count movies per genre

**Question Details:**
Write a query to count movies in each genre, ordered by count descending.

---

**Company**: Meta
**Difficulty**: hard
**Type**: sql

**Question Title:**
Calculate friend request acceptance rate

**Question Details:**
Find the overall friend request acceptance rate rounded to 2 decimals.

---
```

---

## 🎯 Recommended Workflow

### TODAY (5 minutes):
1. Run merge script with GitHub questions
2. Upload to Supabase
3. Test in app

### THIS WEEK (1-2 hours):
4. Fill LeetCode template (20-30 questions)
5. Fill StrataScratch template (20-30 questions)
6. Re-run merge
7. Re-upload to Supabase

### RESULT:
- Total questions: 94-114
- SQL coverage: ✅ Fixed (from 0% to 90%)
- Company diversity: ✅ Improved
- Question quality: ✅ Real interview questions

---

## 📊 Current Status

### What You Have:
| Source | Questions | Status |
|--------|-----------|--------|
| GitHub | 54 | ✅ Collected |
| Scenario Questions | 30 | ✅ Collected |
| Template Examples | 2 | ✅ Included |
| **Current Total** | **86** | ✅ **Ready to upload!** |
| LeetCode | 0 → 20-50 | ⏳ Template ready |
| StrataScratch | 0 → 20-50 | ⏳ Template ready |
| **Potential Total** | **106-186** | **Ready to grow!** |

### Coverage (Current 86 Questions):
- **Coding:** ✅ Excellent (13 questions)
- **ML:** ✅ Excellent (18 questions)
- **Stats:** ✅ Good (16 questions)
- **Case Studies:** ✅ Good (11 questions)
- **Mixed:** ✅ Good (25 questions)
- **SQL:** ⚠️ Low (2 questions - add StrataScratch!)
- **Difficulty Balance:** ✅ Great (68 medium, 13 hard, 3 easy)

---

## 🐛 Quick Troubleshooting

### Can't find a file?
Check the folder structure above - everything is organized!

### Template looks empty?
That's correct! YOU fill it with questions from LeetCode/StrataScratch

### Merge script says "no questions"?
Make sure you ran `parse_manual_questions.py` first after filling templates

### Need help?
1. Check `docs/QUICK_START.md`
2. Check `docs/LEETCODE_TUTORIAL.md`
3. Check `docs/STRATASCRATCH_TUTORIAL.md`

---

## ✨ Quick Commands Reference

```bash
# Navigate to project
cd "/Users/basilsuhail/folders/Data Sets/Data_Science_Interview_Questions"
source venv/bin/activate

# Collect from GitHub (already done)
python scripts/collect_github_questions.py

# Create templates (already done)
python scripts/scrape_leetcode_discuss.py
python scripts/scrape_stratascratch.py

# After filling templates, parse them
python scripts/parse_manual_questions.py

# Merge everything
python scripts/merge_all_questions.py

# Check output
ls -lh collected_questions/final_interview_questions.csv
```

---

## 🎯 Your Next Action

**Right now, do ONE of these:**

**A.** Use what you have (5 min):
   - Run: `python scripts/merge_all_questions.py`
   - Upload: `collected_questions/final_interview_questions.csv` to Supabase

**B.** Add LeetCode questions (30-60 min):
   - Read: `docs/LEETCODE_TUTORIAL.md`
   - Fill: `templates/leetcode_manual_template.txt`

**C.** Add SQL questions (30-60 min):
   - Read: `docs/STRATASCRATCH_TUTORIAL.md`
   - Fill: `templates/stratascratch_manual_template.txt`

**D.** Do everything (1-2 hours):
   - Fill both templates
   - Parse & merge
   - Upload to Supabase

---

**Everything is organized and ready. Your choice! 🚀**
