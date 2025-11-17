# 📚 Complete Interview Questions Collection Guide

## 🎯 Overview

You now have 5 scripts to collect real interview questions from multiple sources:

1. **collect_github_questions.py** - Fully automated (GitHub repos)
2. **scrape_leetcode_discuss.py** - Creates manual template
3. **scrape_stratascratch.py** - Browser automation (requires login)
4. **parse_manual_questions.py** - Parses manual templates
5. **merge_all_questions.py** - Combines & deduplicates everything

---

## 📋 STEP-BY-STEP INSTRUCTIONS

### **STEP 1: Install Dependencies** (5 minutes)

```bash
cd "/Users/basilsuhail/folders/Data Sets/Data_Science_Interview_Questions"
source venv/bin/activate

# Install required packages
pip install requests beautifulsoup4 playwright

# Install Playwright browser (for StrataScratch automation)
playwright install chromium
```

---

### **STEP 2: Run GitHub Collector** (EASIEST - Fully Automated)

```bash
python collect_github_questions.py
```

**What it does:**
- Fetches questions from curated GitHub repositories
- No login required
- 100% automated
- Takes ~30 seconds

**Expected output:**
- `github_questions.csv` with 100-300 questions
- Statistics by type, difficulty, company

---

### **STEP 3A: LeetCode - Manual Collection** (30-60 minutes of your time)

Since LeetCode uses JavaScript-rendered content, automation is difficult.

**What to do:**

1. Run the script to create the template:
```bash
python scrape_leetcode_discuss.py
```

2. This creates: `leetcode_manual_template.txt`

3. **Open in browser:** https://leetcode.com/discuss/interview-experience

4. **Search for:** "data science" or "machine learning"

5. **Copy questions** from interesting posts and paste into the template

6. **Format:**
```
---

## Meta - Data Scientist

**Difficulty**: medium
**Type**: stats

**Question 1:**
Explain the bias-variance tradeoff in the context of model selection.

**Question 2:**
How would you design an experiment to test a new feature?

---
```

7. **Parse the template** when you're done:
```bash
python parse_manual_questions.py
```

**Expected output:**
- `manual_questions.csv` with however many you collected (20-100 recommended)

---

### **STEP 3B: StrataScratch - Automated or Manual** (Choose one)

#### **Option A: Automated with Browser** (Recommended if comfortable)

1. **Sign up** at https://www.stratascratch.com (free account)

2. **Run the script:**
```bash
python scrape_stratascratch.py
```

3. **What happens:**
   - Browser opens automatically
   - You log in manually (60 seconds)
   - Script collects questions automatically
   - Browser closes when done

4. **Expected output:**
   - `stratascratch_questions.csv` with 50+ SQL questions

**⚠️ Note:** If automation fails, use Option B

#### **Option B: Manual Collection**

1. Sign up at StrataScratch

2. Browse questions and copy them into: `stratascratch_manual_template.txt`

3. Format:
```
---

**Company**: Netflix
**Difficulty**: medium
**Type**: sql

**Question Title:**
Count the number of movies per genre

**Question Details:**
Write a query to find the number of movies in each genre.

---
```

4. Parse when done:
```bash
python parse_manual_questions.py
```

---

### **STEP 4: Merge Everything** (Automated - 1 minute)

Once you've collected from all sources, merge them:

```bash
python merge_all_questions.py
```

**What it does:**
- Loads all CSV files
- Removes duplicates (fuzzy matching with 85% similarity threshold)
- Standardizes format
- Generates statistics

**Expected output:**
- `final_interview_questions.csv` with 300-700 unique questions

---

### **STEP 5: Upload to Supabase** (10 minutes)

See `SUPABASE_SETUP.md` for detailed instructions.

**Quick version:**

1. Go to Supabase → Table Editor

2. Create new table: `interview_questions`

3. Import `final_interview_questions.csv`

4. Done!

---

## 📊 Expected Results

### **Minimum Effort** (GitHub only - fully automated):
- **Time:** 1 minute
- **Questions:** 100-300
- **Quality:** Good, but may lack SQL questions

### **Moderate Effort** (GitHub + Manual templates):
- **Time:** 1-2 hours
- **Questions:** 300-500
- **Quality:** Very good, diverse question types

### **Maximum Effort** (All sources + automation):
- **Time:** 2-3 hours
- **Questions:** 500-800
- **Quality:** Excellent, comprehensive coverage

---

## 🎯 Recommended Approach

**For Quick Start:**
1. Run GitHub collector (1 minute)
2. Upload to Supabase (5 minutes)
3. **Result:** 100-300 questions immediately

**For Best Results:**
1. Run GitHub collector
2. Spend 30 minutes filling LeetCode template (20-50 questions)
3. Spend 30 minutes filling StrataScratch template (20-50 questions)
4. Parse and merge
5. Upload to Supabase
6. **Result:** 300-500 high-quality questions

---

## 🐛 Troubleshooting

### Problem: `ModuleNotFoundError: No module named 'requests'`
**Solution:**
```bash
pip install requests beautifulsoup4
```

### Problem: Playwright automation fails
**Solution:**
- Use manual templates instead
- Or check: `playwright install chromium` was run

### Problem: GitHub script returns 0 questions
**Solution:**
- Check internet connection
- GitHub may be rate-limiting (wait 10 minutes and retry)

### Problem: Merge script finds too many duplicates
**Solution:**
- This is normal! Similar questions appear across sources
- Deduplication protects database quality

---

## 📁 Output Files Summary

| File | Source | Question Count | Automated? |
|------|--------|----------------|------------|
| `github_questions.csv` | GitHub repos | 100-300 | ✅ Yes |
| `leetcode_questions.csv` | LeetCode Discuss | 0 (uses template) | ❌ No |
| `stratascratch_questions.csv` | StrataScratch | 50-100 | ⚠️ Semi-automated |
| `manual_questions.csv` | Your manual collection | Varies | ❌ No |
| `final_interview_questions.csv` | **All sources merged** | **300-700** | ✅ Final output |

**Upload this file to Supabase:** `final_interview_questions.csv`

---

## 🚀 Next Steps After Collection

1. ✅ Upload `final_interview_questions.csv` to Supabase
2. ✅ Update app to use real questions instead of AI-generated
3. ✅ Test question quality
4. 🎯 Build Mock Interview Simulator (Phase 3)

---

Need help? Check the error messages in the script output or re-run with verbose logging.

Good luck! 🎉
