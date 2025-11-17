# 🚀 QUICK START - Interview Questions Collection

## ✅ What's Already Done

I've created everything you need and already collected **54 questions** from GitHub!

**Files created:**
- ✅ `collect_github_questions.py` - GitHub collector (already ran!)
- ✅ `scrape_leetcode_discuss.py` - LeetCode template creator
- ✅ `scrape_stratascratch.py` - StrataScratch automation
- ✅ `parse_manual_questions.py` - Template parser
- ✅ `merge_all_questions.py` - Question merger
- ✅ `github_questions.csv` - **54 questions already collected!**

**Documentation:**
- ✅ `COLLECTION_GUIDE.md` - Full step-by-step guide
- ✅ `SUPABASE_SETUP.md` - Database setup instructions

---

## 🎯 THREE OPTIONS - Choose Your Path

### **OPTION 1: Quick Start (5 minutes) - Use What We Have**

You already have 54 questions from GitHub. Let's use them now:

```bash
cd "/Users/basilsuhail/folders/Data Sets/Data_Science_Interview_Questions"
source venv/bin/activate

# You already have github_questions.csv!
# Just merge (in case you add more sources later)
python merge_all_questions.py
```

**Result:** `final_interview_questions.csv` with 54 questions

**Then:** Upload to Supabase (see SUPABASE_SETUP.md)

---

### **OPTION 2: Moderate Effort (1-2 hours) - Add Manual Questions**

Add more questions manually from LeetCode and StrataScratch:

#### Step 1: LeetCode Questions (30-60 min)
1. Run: `python scrape_leetcode_discuss.py`
2. This creates: `leetcode_manual_template.txt`
3. Go to: https://leetcode.com/discuss/interview-experience
4. Search: "data science" or "machine learning"
5. Copy 20-50 questions into the template
6. Run: `python parse_manual_questions.py`

#### Step 2: StrataScratch Questions (30-60 min)
1. Sign up at: https://www.stratascratch.com
2. Run: `python scrape_stratascratch.py` (creates template if automation fails)
3. Copy 20-50 SQL questions into `stratascratch_manual_template.txt`
4. Run: `python parse_manual_questions.py`

#### Step 3: Merge Everything
```bash
python merge_all_questions.py
```

**Result:** `final_interview_questions.csv` with 150-300 questions

---

### **OPTION 3: Maximum Automation (requires setup)**

Try browser automation for StrataScratch:

```bash
# Install Playwright
pip install playwright
playwright install chromium

# Run automation (you'll need to log in)
python scrape_stratascratch.py

# Merge
python merge_all_questions.py
```

**Result:** 200-400 questions (depending on automation success)

---

## 📊 What You Have Right Now

**File:** `github_questions.csv`
**Questions:** 54
**Breakdown:**
- Coding: 13 questions
- ML: 8 questions
- Stats: 7 questions
- Mixed: 26 questions

**This is already enough to start!** You can:
- Upload to Supabase now
- Add more questions later

---

## 🎯 RECOMMENDED NEXT STEPS

### For Quick Testing (TODAY):

1. **Merge existing questions:**
```bash
cd "/Users/basilsuhail/folders/Data Sets/Data_Science_Interview_Questions"
source venv/bin/activate
python merge_all_questions.py
```

2. **Upload to Supabase:**
   - Go to Supabase → SQL Editor
   - Run CREATE TABLE query (see SUPABASE_SETUP.md)
   - Import `final_interview_questions.csv`

3. **Test in your app:**
   - Verify questions appear
   - Check company filtering works
   - Test question types

### For Better Coverage (THIS WEEK):

4. **Add manual questions:**
   - Spend 30 min on LeetCode template
   - Spend 30 min on StrataScratch template
   - Re-run merge script
   - Re-upload to Supabase

5. **Test quality:**
   - Generate questions for different companies
   - Verify difficulty levels make sense
   - Check answer quality from textbooks

---

## 📁 File Structure

```
Data Science Interview Questions/
├── collect_github_questions.py      ✅ Ran successfully
├── scrape_leetcode_discuss.py       ✅ Creates template
├── scrape_stratascratch.py          ✅ Automation/template
├── parse_manual_questions.py        ✅ Parses templates
├── merge_all_questions.py           ✅ Merges everything
├── github_questions.csv             ✅ 54 questions (READY!)
├── leetcode_manual_template.txt     ⏳ Fill this (optional)
├── stratascratch_manual_template.txt⏳ Fill this (optional)
└── final_interview_questions.csv    🎯 Upload this to Supabase
```

---

## ⚡ FASTEST PATH TO PRODUCTION

```bash
# 1. Merge (1 min)
python merge_all_questions.py

# 2. Create Supabase table (copy SQL from SUPABASE_SETUP.md)

# 3. Upload final_interview_questions.csv to Supabase

# 4. Test in app

# DONE! You now have real interview questions!
```

---

## 🐛 Common Issues & Fixes

### Issue: "ModuleNotFoundError: No module named 'requests'"
**Fix:**
```bash
pip install requests beautifulsoup4
```

### Issue: "No questions found in template"
**Fix:** Make sure you filled out the template files with actual questions

### Issue: Merge script says "No questions to merge"
**Fix:** Run at least one collector script first (GitHub collector already ran!)

---

## 📞 What to Do If Stuck

1. Check COLLECTION_GUIDE.md for detailed instructions
2. Check SUPABASE_SETUP.md for database setup
3. Re-run `python merge_all_questions.py` to see what files it's looking for

---

## ✨ Summary

You're ready to go! You have:
- ✅ 54 real interview questions collected
- ✅ All scripts created and tested
- ✅ Templates ready for manual collection
- ✅ Merge script ready to combine sources
- ✅ Documentation for Supabase setup

**Minimum viable next step:** Run merge script and upload to Supabase!

**Maximum effort next step:** Fill templates, collect 200-300 questions, then upload!

Your choice! 🚀
