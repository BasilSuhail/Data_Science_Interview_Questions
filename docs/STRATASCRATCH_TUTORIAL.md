# 🎯 StrataScratch SQL Questions - Collection Tutorial

## 🎯 Goal

Collect 20-50 SQL interview questions from StrataScratch to fill the biggest gap in your database.

**Why this matters:** 85% of data science interviews include SQL questions, and you currently have 0% SQL coverage!

**Time needed:** 30-60 minutes (manual) OR 10 minutes (automation)
**Questions you'll get:** 20-50 real SQL questions from top companies
**Difficulty:** Easy-Medium

---

## OPTION A: Automated Collection (Recommended if comfortable)

### Requirements:
- Free StrataScratch account
- Playwright installed
- 10 minutes

### Steps:

#### 1. Sign Up for StrataScratch:
- Go to: https://www.stratascratch.com
- Click "Sign Up"
- Use Google or Email (free account)
- Verify email if needed

#### 2. Install Playwright:
```bash
cd "/Users/basilsuhail/folders/Data Sets/Data_Science_Interview_Questions"
source venv/bin/activate
pip install playwright
playwright install chromium
```

#### 3. Run the Automation Script:
```bash
python scripts/scrape_stratascratch.py
```

#### 4. What Happens:
1. Browser window opens
2. **You manually log in** (script waits 60 seconds)
3. Script automatically collects questions
4. Browser closes when done

#### 5. Output:
- `collected_questions/stratascratch_questions.csv` with 50+ SQL questions

---

## OPTION B: Manual Collection (Safer, more control)

### Steps:

#### 1. Sign Up:
- Go to: https://www.stratascratch.com
- Create free account

#### 2. Create Template:
```bash
python scripts/scrape_stratascratch.py
```

This creates: `templates/stratascratch_manual_template.txt`

#### 3. Browse Questions:

**Navigate to:**
- https://www.stratascratch.com/coding
- Click "SQL" filter
- Sort by: "Most Popular" or "Company"

**Filter by Company:**
- Meta/Facebook
- Amazon
- Google
- Netflix
- Uber
- Airbnb

#### 4. Copy Questions into Template:

**Template Format:**
```
---

**Company**: [Company Name]
**Difficulty**: easy/medium/hard
**Type**: sql

**Question Title:**
[Title of the question]

**Question Details:**
[Full question text if available]

---
```

**Real Example:**
```
---

**Company**: Netflix
**Difficulty**: medium
**Type**: sql

**Question Title:**
Count the number of movies per genre

**Question Details:**
Write a query to find the number of movies in each genre. Return the genre name and count, ordered by count descending.

Tables: movies (id, title, genre_id), genres (id, name)

---

**Company**: Meta
**Difficulty**: hard
**Type**: sql

**Question Title:**
Find the friend requests acceptance rate

**Question Details:**
Calculate the overall acceptance rate of friend requests rounded to 2 decimal places.

Tables: friend_request (sender_id, send_to_id, request_date), request_accepted (requester_id, accepter_id, accept_date)

---
```

#### 5. Parse Template:
```bash
python scripts/parse_manual_questions.py
```

**Output:** `collected_questions/manual_questions.csv`

---

## 📊 What Questions to Look For

### High-Value SQL Topics:

#### 1. **JOINs** (most common):
- INNER JOIN vs LEFT JOIN vs RIGHT JOIN
- Self-joins
- Multiple table joins
- Join on conditions with filters

#### 2. **Aggregations**:
- COUNT, SUM, AVG, MAX, MIN
- GROUP BY with multiple columns
- HAVING clause
- DISTINCT counts

#### 3. **Window Functions** (medium-hard):
- ROW_NUMBER()
- RANK() / DENSE_RANK()
- LAG() / LEAD()
- PARTITION BY

#### 4. **Subqueries**:
- IN / NOT IN
- EXISTS / NOT EXISTS
- Correlated subqueries
- WITH (Common Table Expressions)

#### 5. **Date Functions**:
- DATE_DIFF / DATE_ADD
- EXTRACT (year, month, day)
- Date formatting
- Rolling windows

#### 6. **String Functions**:
- LIKE / ILIKE
- CONCAT / SUBSTRING
- UPPER / LOWER
- Pattern matching

---

## 🎯 Example Questions from StrataScratch

### Easy Questions:
1. **Find all customers who made purchases in the last 30 days**
   - Tables: customers, orders
   - Company: Amazon

2. **Count users by country**
   - Tables: users
   - Company: Meta

3. **Find the top 10 most expensive products**
   - Tables: products
   - Company: Walmart

### Medium Questions:
4. **Calculate monthly active users (MAU)**
   - Tables: user_activity (user_id, activity_date)
   - Company: LinkedIn

5. **Find users who made purchases but never returned items**
   - Tables: purchases, returns
   - Company: Amazon

6. **Calculate retention rate by cohort**
   - Tables: user_signups, user_activity
   - Company: Netflix

### Hard Questions:
7. **Find the top 3 products by revenue in each category**
   - Tables: products, sales
   - Company: Google

8. **Calculate friend request acceptance rate per day**
   - Tables: friend_requests, friend_accepts
   - Company: Meta

9. **Find users with consecutive login days >= 7**
   - Tables: user_logins
   - Company: Spotify

---

## 💡 Pro Tips

### 1. **Focus on Company-Specific Questions**:
   - Each company has preferred question styles
   - Meta: Social network queries (friends, posts, likes)
   - Amazon: E-commerce queries (orders, products, returns)
   - Netflix: Content queries (movies, ratings, genres)

### 2. **Balance Difficulty**:
   - 40% Easy (warm-up questions)
   - 40% Medium (core interview level)
   - 20% Hard (stretch questions)

### 3. **Include Context**:
   - Copy table schemas if provided
   - Note any specific requirements
   - Include expected output format

### 4. **Diversity**:
   - Mix different SQL concepts
   - Include both analytical and operational queries
   - Add some real-world scenarios

---

## 🚀 Quick Collection Strategy

### 15-Minute Version (Minimum Viable):
1. Sign up for StrataScratch
2. Go to SQL questions, filter by "Meta"
3. Copy 5 questions
4. Filter by "Amazon", copy 5 questions
5. Filter by "Netflix", copy 5 questions
6. Parse template → **15 SQL questions!**

### 30-Minute Version (Recommended):
1. Follow 15-minute version
2. Add 5 questions from Google
3. Add 5 questions from Uber
4. Add 5 questions with window functions
5. Parse template → **30 SQL questions!**

### 60-Minute Version (Comprehensive):
1. Follow 30-minute version
2. Add 10 medium difficulty questions
3. Add 5 hard questions
4. Add 5 questions on date functions
5. Parse template → **50 SQL questions!**

---

## ⚠️ Important Notes

### Free Tier Limits:
- StrataScratch free tier: First 50 questions are free
- You can view question titles and descriptions
- Some detailed hints/solutions require paid tier
- **For our purpose:** Question titles/descriptions are enough!

### What to Collect:
- ✅ Question title
- ✅ Company tag
- ✅ Difficulty level
- ✅ Brief description
- ❌ Don't need: Full solution code
- ❌ Don't need: Detailed hints (our textbooks will provide answers)

---

## 🐛 Troubleshooting

### Problem: Automation script fails to open browser
**Solution:**
```bash
playwright install chromium
```

### Problem: Automation doesn't collect questions
**Solution:** Use manual collection (Option B) - more reliable

### Problem: Can't access certain questions (paywall)
**Solution:** Skip paid questions, focus on free ones - you have 50+ free questions available

### Problem: Parser says "no questions found"
**Solution:** Check template formatting:
```
**Company**: [Company]  ← Must have this exact format
**Difficulty**: [Level]  ← Must have this exact format
**Type**: sql            ← Must be lowercase "sql"
```

---

## ✅ Verification

After collection, verify:

```bash
# Check file exists
ls -lh collected_questions/stratascratch_questions.csv

# Quick preview
head -10 collected_questions/stratascratch_questions.csv

# Count questions
wc -l collected_questions/stratascratch_questions.csv
```

Expected: 20-50 rows (questions)

---

## 📈 Impact on Your Database

### Before StrataScratch:
- SQL Coverage: **0%**
- Coding Questions: 13 (mostly Python)
- Interview Weakness: SQL interviews

### After StrataScratch:
- SQL Coverage: **90%** (with 30-50 questions)
- Coding Questions: 43-63 (SQL + Python)
- Interview Strength: SQL interviews covered!

**This is the single biggest improvement you can make to your question database!**

---

## ✅ Checklist

Before moving to next step:

- [ ] StrataScratch account created
- [ ] Chose automation OR manual collection
- [ ] If automation: Playwright installed
- [ ] Collected 20-50 SQL questions
- [ ] Questions include company tags
- [ ] Mix of easy/medium/hard difficulty
- [ ] Ran `parse_manual_questions.py`
- [ ] Verified CSV file exists

---

**Next:** Run `merge_all_questions.py` to combine everything!

Or see: `docs/QUICK_START.md` for the merge instructions.
