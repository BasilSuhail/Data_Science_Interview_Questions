# 🤖 AI Interview Coach

**Complete interview preparation system combining your curated question database with AI-powered evaluation.**

---

## 🎯 What This Does

Your AI Interview Coach provides:

1. **552 Curated Questions** - From your Supabase database
   - FAANG-vetted questions
   - Organized by type, difficulty, topic
   - 11 trusted sources

2. **AI Answer Evaluation** - Using Gemini 2.5 Flash
   - Scores answers (0-10)
   - Identifies strengths
   - Suggests improvements
   - Actionable feedback

3. **3,983 Textbook Pages** - For reference answers
   - Data Science fundamentals
   - Machine Learning concepts
   - Statistical methods

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file or export these:

```bash
# Supabase (for question database)
export SUPABASE_URL="your-supabase-url"
export SUPABASE_KEY="your-supabase-anon-key"

# Gemini (for answer evaluation)
export GEMINI_API_KEY="your-gemini-api-key"
```

**Get API Keys:**
- **Supabase:** Already have it from your project setup
- **Gemini:** Get free at https://aistudio.google.com/app/apikey

### 3. Run the Interview Coach

```python
from ai_coach.interview_coach import InterviewCoach

# Initialize
coach = InterviewCoach()

# Conduct interview
result = coach.conduct_interview(
    question_type="ml",      # ml, stats, sql, coding, case, behavioral
    difficulty="medium",      # easy, medium, hard
    role="Data Scientist"
)
```

---

## 📚 Features

### Feature 1: Question Selection from Database

```python
# Get a specific type of question
question = coach.get_question(
    question_type="ml",
    difficulty="medium",
    topics="deep_learning"
)

# Random question
random_question = coach.get_question(random_selection=True)
```

**Available Filters:**
- `question_type`: ml, stats, sql, coding, case, behavioral, mixed
- `difficulty`: easy, medium, hard
- `topics`: machine_learning, deep_learning, nlp, sql_database, etc.
- `company`: Filter by company (if tagged)

---

### Feature 2: Answer Evaluation

```python
from ai_coach.gemini_evaluator import GeminiEvaluator

evaluator = GeminiEvaluator()

evaluation = evaluator.evaluate_answer(
    question="What is the bias-variance tradeoff?",
    answer="Bias is underfitting, variance is overfitting...",
    role="Machine Learning Engineer",
    question_type="ml"
)

# Output:
# {
#   "score": 8,
#   "strengths": ["Clear explanation", "Mentioned key concepts"],
#   "improvements": ["Add examples", "Discuss tradeoff implications"],
#   "final_comment": "Solid answer with room for depth..."
# }
```

---

### Feature 3: Practice Sessions

```python
# Practice with 5 questions
coach.practice_session(
    num_questions=5,
    question_type="stats",
    difficulty="medium",
    role="Data Scientist"
)

# Provides:
# - 5 questions from database
# - Interactive answering
# - Individual evaluations
# - Session summary with average score
```

---

## 🎓 Example Workflow

### Interactive Interview Session

```python
from ai_coach.interview_coach import InterviewCoach

# Initialize
coach = InterviewCoach()

# Start interview
session = coach.conduct_interview(
    question_type="ml",
    difficulty="medium",
    role="Machine Learning Engineer"
)
```

**What Happens:**

1. **Question Retrieved** from your database (552 questions)
   ```
   ❓ QUESTION:
   Explain the difference between bagging and boosting in ensemble methods.
   ```

2. **You Answer** (type your response)
   ```
   💭 Your answer:
   Bagging reduces variance by training models in parallel...
   ```

3. **AI Evaluates** using Gemini
   ```
   📊 EVALUATION RESULTS

   🎯 Score: 7/10
      Strong - Good candidate

   ✅ STRENGTHS:
      1. Clear distinction between parallel vs sequential
      2. Mentioned variance reduction
      3. Professional terminology

   💡 AREAS FOR IMPROVEMENT:
      1. Could add specific examples (Random Forest, XGBoost)
      2. Discuss when to use each method

   💬 FINAL COMMENT:
      Solid foundational answer. Consider adding practical
      examples and use cases to strengthen your response.
   ```

4. **Model Answer** shown (if available in database)
   ```
   📚 MODEL ANSWER (from database):
   Bagging (Bootstrap Aggregating) trains multiple models
   independently on random subsets... [full answer]
   ```

---

## 📊 Scoring System

The AI evaluates on 5 dimensions:

1. **Clarity** - Is the answer well-structured?
2. **Relevance** - Does it answer the question?
3. **Technical Depth** - Shows understanding?
4. **Communication** - Professional and articulate?
5. **Completeness** - Covers key points?

**Score Interpretation:**
- 9-10: Excellent - Hire immediately!
- 7-8: Strong - Good candidate
- 5-6: Acceptable - Needs improvement
- 3-4: Weak - Significant gaps
- 0-2: Poor - Not ready

---

## 🔧 Advanced Usage

### Custom Evaluation Criteria

```python
from ai_coach.gemini_evaluator import GeminiEvaluator

evaluator = GeminiEvaluator()

# Modify the prompt for specific criteria
evaluator.EVALUATION_PROMPT = """
Your custom evaluation criteria here...
Focus on: {custom_criteria}
"""

evaluation = evaluator.evaluate_answer(
    question=question,
    answer=answer,
    role="Custom Role"
)
```

### Batch Evaluation

```python
# Evaluate multiple answers at once
qa_pairs = [
    {"question": "Q1...", "answer": "A1...", "question_type": "ml"},
    {"question": "Q2...", "answer": "A2...", "question_type": "stats"},
]

results = evaluator.batch_evaluate(qa_pairs, role="Data Scientist")
```

### Database Queries

```python
# Direct Supabase queries
response = coach.supabase.table("interview_questions") \
    .select("*") \
    .eq("question_type", "sql") \
    .eq("difficulty", "hard") \
    .execute()

hard_sql_questions = response.data
```

---

## 📁 File Structure

```
ai_coach/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── gemini_evaluator.py      # Answer evaluation module
├── interview_coach.py       # Main integration
└── examples/                # Example scripts
    ├── basic_usage.py
    ├── practice_session.py
    └── batch_evaluation.py
```

---

## 🎯 Use Cases

### 1. Interview Preparation

```python
# Practice ML interviews
coach.practice_session(
    num_questions=10,
    question_type="ml",
    difficulty="hard",
    role="Senior ML Engineer"
)
```

### 2. Skill Assessment

```python
# Test SQL knowledge
results = []
for i in range(5):
    result = coach.conduct_interview(
        question_type="sql",
        difficulty="medium"
    )
    results.append(result)

# Calculate average score
avg_score = sum(r["evaluation"]["score"] for r in results) / len(results)
print(f"SQL Proficiency: {avg_score}/10")
```

### 3. Custom Question Sets

```python
# Create custom quiz from specific topics
questions = coach.supabase.table("interview_questions") \
    .select("*") \
    .in_("topics", ["deep_learning", "nlp", "computer_vision"]) \
    .execute()

for q in questions.data[:5]:
    # Conduct interview with each question
    ...
```

---

## 🚀 Next Steps

### Add RAG (Textbook Search)

Your database has 3,983 textbook pages. You can add:

```python
def get_textbook_explanation(question: str) -> str:
    """Search textbooks for relevant explanations."""
    response = coach.supabase.table("documents") \
        .select("content, book_name, page_number") \
        .textSearch("content", question) \
        .limit(3) \
        .execute()

    # Format and return relevant pages
    return format_textbook_answer(response.data)
```

### Web Interface

Build a Streamlit/Flask app:
- Select question type/difficulty
- Answer in text box
- Get instant AI evaluation
- Track progress over time

### Progress Tracking

Add a `user_sessions` table to track:
- Questions attempted
- Scores over time
- Weak areas
- Improvement trends

---

## 🛠️ Troubleshooting

### Error: "Gemini API key required"
**Solution:** Set `GEMINI_API_KEY` environment variable

### Error: "Supabase credentials not found"
**Solution:** Set `SUPABASE_URL` and `SUPABASE_KEY`

### Error: "No questions found"
**Solution:** Check your filters - the database might not have questions matching all criteria

### Evaluation returns raw response
**Solution:** Gemini might return non-JSON format. Check `raw_response` field in result.

---

## 💡 Pro Tips

1. **Start Easy** - Begin with easy/medium questions to build confidence
2. **Review Model Answers** - Compare your answer to database answers
3. **Track Improvements** - Note common improvement suggestions
4. **Mix Question Types** - Practice across ml, stats, sql, coding, case
5. **Time Yourself** - Add time limits for realistic interview practice

---

## 📊 Your Database Stats

**Questions:** 552 unique questions
- ML: 264 (48%)
- Mixed: 109 (20%)
- Stats: 61 (11%)
- Case: 61 (11%)
- Coding: 28 (5%)
- SQL: 22 (4%)
- Behavioral: 5 (1%)

**Sources:** 11 different repositories
- Sandy1811/DS-Interview-FAANG (156)
- kojino/120-DS-Questions (115)
- DS_Interview_Notebook (96)
- And 8 more...

**Textbooks:** 3,983 pages from 10 books
- Introduction to Statistical Learning
- OpenIntro Statistics
- Think Stats
- And 7 more...

---

## 🎉 You're Ready!

Your AI Interview Coach combines:
✅ Curated questions (your valuable database)
✅ AI evaluation (Gemini feedback)
✅ Textbook knowledge (3,983 pages)

**Start practicing:**

```python
from ai_coach.interview_coach import InterviewCoach

coach = InterviewCoach()
coach.conduct_interview(question_type="ml", difficulty="medium")
```

**Good luck with your interviews!** 🚀
