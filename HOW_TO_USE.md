# 🚀 How to Use Your AI Interview Coach

**Your complete interview preparation app is ready!**

---

## ✅ What You Have

**Main App:** [interview-coach-app.html](interview-coach-app.html)

**Features:**
1. ✅ **552 curated interview questions** from 11 sources
2. ✅ **30 coding practice problems** with constraints, examples, and hints (NEW!)
3. ✅ **3,983 textbook pages** for AI-generated answers
4. ✅ **AI answer evaluation** with Gemini
5. ✅ **AI code review** for coding solutions (NEW!)
6. ✅ **Personalized question generation** based on your profile
7. ✅ **Company-specific prep** (FAANG, consulting, finance)
8. ✅ **Interview countdown** timer

---

## 🎯 How to Use It

### Step 1: Open the App

```bash
# In your browser, open:
interview-coach-app.html
```

Or simply **double-click** the file!

---

### Step 2: Set Up Your Profile (Optional but Recommended)

1. Click the **👤 Profile** button in top right
2. Set your:
   - **Experience Level** (Junior, Mid, Senior)
   - **Target Companies** (Google, Meta, Amazon, etc.)
   - **Weak Areas** (Coding, Stats, ML, etc.)
   - **Interview Date** (optional - adds countdown timer!)
3. Click **Save Profile**

**Your profile personalizes:**
- Question difficulty
- Company-specific questions
- Focus on your weak areas
- Urgency based on interview date

---

### Step 3: Generate Questions

1. Select **question type** (ML, Stats, SQL, **Coding Interview**, Case, Mixed)
2. Select **difficulty** (Easy, Medium, Hard)
3. Select **number of questions** (5, 10, 15, 20)
4. Click **"Generate"**

Questions are **personalized** based on your profile!

**NEW: Coding Interview Mode**
- Select "Coding Interview" to get actual coding problems from our database
- Each problem includes:
  - Problem statement
  - Constraints
  - Example inputs/outputs
  - Hints
  - Code editor for your solution
  - AI code review with complexity analysis!

---

### Step 4: Practice with AI Feedback 🤖

**For Theory Questions:**

1. **Click the question** to expand it
2. **See the textbook-based answer** (from your 3,983 pages!)
3. **Type your own answer** in the practice box
4. **Click "Get AI Feedback"**

**You'll get:**
- ✅ Score (0-10)
- ✅ Strengths identified
- ✅ Areas for improvement
- ✅ Actionable feedback

**For Coding Questions:** (NEW!)

1. **Click the coding problem** to expand it
2. **Read constraints, examples, and hints**
3. **Write your code solution** in any language (Python, JavaScript, Java, Go, etc.)
4. **Click "Get AI Code Review"**

**You'll get:**
- ✅ Code quality score (0-10)
- ✅ Correctness evaluation
- ✅ Time & space complexity analysis
- ✅ Good practices identified
- ✅ Specific improvements suggested

**This is powered by Gemini AI** - completely free!

---

## 🎨 Features Walkthrough

### 1. Profile-Based Question Generation

Your profile affects:
- **Experience Level:** Junior gets foundational questions, Senior gets architecture/leadership
- **Target Companies:** Get Meta-style metrics questions, Google-style system design, etc.
- **Weak Areas:** More questions from your selected weak areas
- **Interview Date:** Urgent prep mode if interview is <7 days away!

### 2. Textbook-Based Answers

When you expand a question, the app:
1. Searches your **3,983 textbook pages**
2. Finds relevant content
3. Uses **Groq AI** to compose a comprehensive answer
4. Cites sources from the textbooks

### 3. AI Answer Evaluation (NEW!)

When you practice your answer:
1. **Gemini AI** analyzes your response
2. Compares to expert-level answers
3. Scores on:
   - Clarity
   - Relevance
   - Technical depth
   - Communication
   - Completeness

**Example Feedback:**
```
🎯 Score: 8/10
Strong - Good candidate

✅ Strengths:
1. Clear explanation of key concepts
2. Mentioned practical examples
3. Professional terminology

💡 Areas for Improvement:
1. Add more depth on trade-offs
2. Discuss when to use each method
```

---

## 💡 Pro Tips

### Tip 1: Set a Realistic Interview Date
Even if you don't have a real interview, set a date 2-3 weeks out. The countdown creates urgency!

### Tip 2: Focus on Weak Areas First
Check "Weak Areas" in your profile. The app will generate more questions from those topics.

### Tip 3: Practice Writing Answers
Don't just read the textbook answers - **write your own** and get AI feedback. This is the best way to improve!

### Tip 4: Track Your Scores
Keep a spreadsheet of your AI scores per topic:
- ML: 6.5/10 avg
- Stats: 7.2/10 avg
- SQL: 8.1/10 avg

This shows your improvement over time!

### Tip 5: Use Different Difficulty Levels
- **Warm up:** Start with Easy
- **Practice:** Use Medium
- **Challenge:** End with Hard

---

## 🔥 Sample Workflow

**Day 1-7: Build Foundation**
1. Set profile to "Junior" level
2. Generate 10 Medium questions on ML
3. Practice answers, get AI feedback
4. Review textbook explanations
5. Track scores

**Day 8-14: Deepen Knowledge**
1. Upgrade to "Mid" level
2. Generate 10 Hard questions on weak areas
3. Practice with AI feedback
4. Aim for 7+/10 scores

**Day 15-21: Company-Specific Prep**
1. Add target companies to profile
2. Generate company-specific questions
3. Practice behavioral + technical together
4. Review AI feedback patterns

**Final Week: Mock Interviews**
1. Set interview date (creates urgency!)
2. Generate 20 Mixed questions
3. Time yourself (2 min per answer)
4. Get AI feedback on all
5. Review improvements needed

---

## 📊 Database Stats

**Theory Questions:** 552 unique from 11 sources
- ML: 264 (48%)
- Mixed: 109 (20%)
- Stats: 61 (11%)
- Case: 61 (11%)
- Coding: 28 (5%)
- SQL: 22 (4%)
- Behavioral: 5 (1%)

**Coding Problems:** 30 curated challenges (NEW!)
- Easy: 7 problems (arrays, strings, search, greedy)
- Medium: 13 problems (concurrency, APIs, design patterns, databases)
- Advanced: 10 problems (system design, algorithms, OAuth, caching)
- Source: Go Interview Practice + Classic DSA

**Textbooks:** 3,983 pages from 10 books
- Introduction to Statistical Learning
- OpenIntro Statistics
- Think Stats
- And 7 more...

**AI Models:**
- Question Generation: Groq (Llama 3.3 70B)
- Answer Generation: Groq (Llama 3.3 70B)
- Answer Evaluation: Gemini 2.5 Flash
- Code Review: Gemini 2.5 Flash (NEW!)

---

## 🆘 Troubleshooting

### "No questions generated"
**Fix:** Check that Groq API key is set in [config.js](config.js)

### "AI Feedback not working"
**Fix:** Check that Gemini API key is set in [config.js](config.js)

### "Textbook answers too slow"
**Fix:** Normal! Searching 3,983 pages takes 5-10 seconds

### "Questions not personalized"
**Fix:** Make sure you saved your profile (click Save Profile button)

---

## 🎯 Quick Start Checklist

- [ ] Open `interview-coach-app.html` in browser
- [ ] Set up profile (experience, companies, weak areas)
- [ ] Generate first set of questions
- [ ] Expand a question to see textbook answer
- [ ] Type your own answer in practice box
- [ ] Get AI feedback
- [ ] Review score and improvements
- [ ] Repeat with more questions!

---

## 🚀 You're Ready!

Your AI Interview Coach is fully set up with:
- ✅ 552 questions from FAANG interviews
- ✅ 3,983 textbook pages for answers
- ✅ AI-powered evaluation with instant feedback
- ✅ Personalized question generation
- ✅ Company-specific prep

**Start practicing and ace those interviews!** 🎉

---

*For technical details, see [GEMINI_INTEGRATION_GUIDE.md](GEMINI_INTEGRATION_GUIDE.md)*
