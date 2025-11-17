# 📝 LeetCode Interview Questions - Manual Collection Tutorial

## 🎯 Goal

Collect 20-50 real data science interview questions from LeetCode Discuss forum and add them to your database.

**Time needed:** 30-60 minutes
**Questions you'll get:** 20-50 high-quality, company-specific questions
**Difficulty:** Easy (just copy-paste)

---

## STEP 1: Create the Template (Automated)

```bash
cd "/Users/basilsuhail/folders/Data Sets/Data_Science_Interview_Questions"
source venv/bin/activate
python scripts/scrape_leetcode_discuss.py
```

**Output:** Creates `templates/leetcode_manual_template.txt`

---

## STEP 2: Browse LeetCode Discuss

### Where to Go:
1. Open: https://leetcode.com/discuss/interview-experience

2. Use search bar and try these searches:
   - "data science"
   - "data scientist"
   - "machine learning engineer"
   - "ML engineer"
   - "data analyst"

### What to Look For:
- Posts with titles like: "Meta Data Scientist Interview Experience"
- Recent posts (2024-2025)
- Posts with detailed question lists

### Good Examples:
- "Google Data Scientist Interview - 5 Questions"
- "Meta DS Interview Experience (New Grad)"
- "Amazon ML Engineer Phone Screen"

---

## STEP 3: Copy Questions into Template

### Template Format:

```
---

## [Company Name] - [Role]

**Difficulty**: easy/medium/hard
**Type**: coding/stats/ml/case/behavioral

**Question 1:**
[Paste the actual question here]

**Question 2:**
[Paste the next question here]

---
```

### Real Example:

```
---

## Meta - Data Scientist

**Difficulty**: medium
**Type**: stats

**Question 1:**
Explain the bias-variance tradeoff. How would you diagnose if your model has high bias vs high variance?

**Question 2:**
You have a dataset with 1000 features and 100 samples. What problems might you face and how would you address them?

**Question 3:**
Design an A/B test to evaluate a new feature on Facebook News Feed. What metrics would you track?

---

## Google - Machine Learning Engineer

**Difficulty**: hard
**Type**: ml

**Question 1:**
Explain how gradient boosting works. What are the differences between XGBoost, LightGBM, and CatBoost?

**Question 2:**
You're building a recommendation system. Walk me through your approach from data collection to deployment.

---
```

---

## STEP 4: Tips for Finding Good Questions

### Best Sources on LeetCode Discuss:

1. **Interview Experience Posts**:
   - Filter by: "Interview Experience"
   - Sort by: "Hot" or "Most Votes"
   - Look for posts with 10+ upvotes

2. **What to Copy**:
   - ✅ Technical questions (stats, ML, coding)
   - ✅ Case study questions
   - ✅ System design questions
   - ❌ Skip: Generic behavioral ("tell me about yourself")
   - ❌ Skip: Company-specific logistics

3. **Quality Over Quantity**:
   - 20-30 high-quality questions > 100 generic ones
   - Focus on questions that test understanding
   - Prefer questions with context/scenarios

---

## STEP 5: Parse Your Template

Once you've filled the template with 20-50 questions:

```bash
python scripts/parse_manual_questions.py
```

**Output:** Creates `collected_questions/manual_questions.csv`

**What it does:**
- Reads your template
- Extracts questions
- Standardizes format
- Tags by company, difficulty, type

---

## STEP 6: Verify Your Questions

Check the CSV was created:

```bash
ls -lh collected_questions/manual_questions.csv
```

Quick preview:

```bash
head -5 collected_questions/manual_questions.csv
```

---

## 📊 Example Companies to Search For

### FAANG:
- Meta/Facebook
- Amazon
- Apple
- Netflix
- Google

### Other Top Companies:
- Microsoft
- LinkedIn
- Uber
- Airbnb
- Spotify
- TikTok/ByteDance
- Tesla
- NVIDIA

### Finance/Consulting:
- Goldman Sachs
- JP Morgan
- McKinsey
- BCG

---

## 🎯 Sample Questions You Might Find

### Statistics Questions:
- "Explain p-values and confidence intervals"
- "What is the Central Limit Theorem and why is it important?"
- "How would you test if a coin is fair?"
- "Explain Type I and Type II errors"

### Machine Learning Questions:
- "Difference between Random Forest and Gradient Boosting?"
- "How do you handle imbalanced datasets?"
- "Explain regularization (L1 vs L2)"
- "What is cross-validation and why use it?"

### SQL Questions:
- "Write a query to find the 2nd highest salary"
- "Explain the difference between INNER and LEFT JOIN"
- "How would you find duplicates in a table?"

### Case Study Questions:
- "How would you measure success of a new feature?"
- "Design metrics for Instagram Stories"
- "How would you reduce customer churn?"

---

## ⚠️ Common Mistakes to Avoid

### ❌ Don't:
- Copy entire posts (just the questions)
- Include answers in the question text (keep them separate)
- Forget to tag company/difficulty
- Mix multiple companies in one section

### ✅ Do:
- Keep each company in its own section
- Use clear question numbering
- Tag difficulty accurately
- Include context if the question has a scenario

---

## 🐛 Troubleshooting

### Problem: "No questions found in template"
**Solution:** Check your formatting:
- Each section should start with `---`
- Company should be marked: `## Company - Role`
- Questions should be: `**Question 1:**`

### Problem: Parser extracts incomplete questions
**Solution:** Make sure each question ends before the next `**Question N:**` marker

### Problem: Can't find good posts on LeetCode
**Solution:** Try these alternatives:
- Search "interview questions" on LeetCode
- Check LeetCode company tags
- Use specific company names in search

---

## 📈 Expected Results

**Time Invested:**
- 10 minutes: Find 5-10 good posts
- 20 minutes: Copy 20-30 questions
- 30-40 minutes: Copy 40-50 questions

**Quality:**
- LeetCode Discuss has **very high-quality** company-specific questions
- Questions are from real candidates
- Often includes follow-up questions
- Good diversity of topics

---

## ✅ Checklist

Before moving to next step:

- [ ] Template file created (`templates/leetcode_manual_template.txt`)
- [ ] Found 5-10 good LeetCode Discuss posts
- [ ] Copied 20-50 questions into template
- [ ] Each section has company name and difficulty
- [ ] Questions are properly formatted
- [ ] Ran `parse_manual_questions.py`
- [ ] Verified `collected_questions/manual_questions.csv` exists

---

**Next:** See `STRATASCRATCH_TUTORIAL.md` to add SQL questions!

Or skip to: `QUICK_START.md` to merge and upload everything.
