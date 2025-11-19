# 🤖 Gemini AI Evaluation - Web App Integration

**AI-powered answer evaluation is now ready for your interview coach web app!**

---

## ✅ What Was Created

### New Files:
1. **gemini-evaluator.js** - JavaScript module for AI answer evaluation
2. **Updated config.js** - Added GEMINI_API_KEY field

### Features Added:
- ✅ Evaluate user answers (0-10 score)
- ✅ Identify strengths
- ✅ Suggest improvements
- ✅ Provide actionable feedback
- ✅ Works entirely in the browser (no backend needed!)

---

## 🚀 Setup (3 Steps)

### Step 1: Get Free Gemini API Key

1. Go to: **https://aistudio.google.com/app/apikey**
2. Click **"Create API Key"**
3. Copy the key (starts with `AIza...`)

**Free tier includes:**
- 15 requests per minute
- 1,500 requests per day
- Perfect for interview practice!

### Step 2: Add API Key to config.js

Open `config.js` and replace the placeholder:

```javascript
const CONFIG = {
    // ... existing keys ...

    // Add your Gemini key here:
    GEMINI_API_KEY: 'AIzaSy...'  // <-- Paste your key here
};
```

### Step 3: Include the Script in Your HTML

Add this line to your `index.html` (after `config.js`):

```html
<script src="config.js"></script>
<script src="gemini-evaluator.js"></script>  <!-- NEW! -->
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
```

**That's it!** The AI evaluator is now available in your app.

---

## 💡 How to Use It

### Method 1: Simple Evaluation

```javascript
// Evaluate any answer
const result = await evaluateAnswer(
    "What is the bias-variance tradeoff?",
    "Bias is underfitting, variance is overfitting...",
    "Data Scientist",
    "ml"
);

console.log(result);
// {
//   score: 7,
//   strengths: ["Clear explanation", "Mentioned key concepts"],
//   improvements: ["Add examples", "Discuss practical implications"],
//   final_comment: "Solid foundational answer..."
// }
```

### Method 2: Display Evaluation UI

```javascript
// Show evaluation result in a div
displayEvaluation(result, 'evaluation-container');
```

### Method 3: Complete Answer Input UI

```javascript
// Create a complete answer input + evaluation UI
createAnswerInputUI(
    "What is overfitting in machine learning?",
    'answer-container',
    { role: "ML Engineer", questionType: "ml" }
);
```

---

## 🎯 Integration into Your Existing App

### Option A: Add to Question Accordion (Recommended)

Modify the `toggleQuestionAnswer()` function in your `index.html`:

```javascript
// In your existing index.html, find toggleQuestionAnswer function
async function toggleQuestionAnswer(index) {
    // ... existing code ...

    // AFTER showing the textbook answer, add AI evaluation UI:
    const questionText = currentQuestions[index];

    // Add answer input UI
    answerDiv.innerHTML += `
        <div style="margin-top: 1.5rem; border-top: 2px solid var(--border); padding-top: 1.5rem;">
            <h4 style="color: var(--accent); margin-bottom: 1rem;">🎯 Practice Your Answer</h4>
            <textarea
                id="practice-answer-${index}"
                style="width: 100%; min-height: 120px; padding: 1rem; border: 2px solid var(--border); border-radius: 0.5rem; background: var(--bg); color: var(--text); font-size: 0.9375rem; resize: vertical; font-family: inherit;"
                placeholder="Type your answer here to get AI feedback..."
            ></textarea>
            <button
                onclick="evaluateMyAnswer(${index})"
                style="margin-top: 0.75rem; padding: 0.75rem 1.5rem; background: var(--accent); color: white; border: none; border-radius: 0.5rem; font-weight: 500; cursor: pointer;"
            >
                Get AI Feedback
            </button>
            <div id="eval-result-${index}"></div>
        </div>
    `;
}

// Add this new function to your index.html
async function evaluateMyAnswer(index) {
    const textarea = document.getElementById(`practice-answer-${index}`);
    const resultDiv = document.getElementById(`eval-result-${index}`);
    const questionText = currentQuestions[index];

    const userAnswer = textarea.value.trim();

    if (!userAnswer) {
        resultDiv.innerHTML = '<p style="color: #f59e0b; margin-top: 1rem;">Please type an answer first.</p>';
        return;
    }

    // Show loading
    resultDiv.innerHTML = '<div style="text-align: center; padding: 1.5rem; color: var(--text-light);">⏳ Evaluating...</div>';

    // Evaluate with Gemini
    const evaluation = await evaluateAnswer(questionText, userAnswer, "Data Scientist", "ml");

    // Display results
    displayEvaluation(evaluation, `eval-result-${index}`);

    // Scroll to results
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
```

### Option B: Add Dedicated "Practice" Tab

Add a new tab to your app for practicing answers:

```html
<!-- In index.html, add a new tab -->
<div class="tabs">
    <button class="tab" onclick="switchTab('search')">Search</button>
    <button class="tab active" onclick="switchTab('questions')">Questions</button>
    <button class="tab" onclick="switchTab('practice')">Practice</button>  <!-- NEW -->
</div>

<!-- Add new tab content -->
<div id="practice-tab" class="tab-content">
    <h2>Practice Your Answers</h2>
    <p>Answer questions and get instant AI feedback!</p>
    <!-- Your practice UI here -->
</div>
```

### Option C: Add "Practice Mode" Button

Add a button next to each generated question:

```javascript
// In displayQuestions function, add a practice button:
questionsDiv.innerHTML = currentQuestions.map((text, i) => {
    return `<div class="question-card" id="question-${i}">
        <div class="question-header">
            <div class="question-text">${text}</div>
            <div class="question-actions">
                <button onclick="practiceQuestion(${i})" class="btn" style="padding: 0.5rem 1rem;">
                    🎯 Practice
                </button>
                <span class="badge badge-${difficulties[i]}">${difficulties[i]}</span>
                <span class="expand-icon">▼</span>
            </div>
        </div>
        <!-- ... rest of card ... -->
    </div>`;
}).join('');

// Add practiceQuestion function
function practiceQuestion(index) {
    const questionText = currentQuestions[index];
    // Show practice modal or expand with answer input
    // ... your implementation ...
}
```

---

## 📊 Example Output

When a user answers a question, they'll see:

```
📊 AI Evaluation Results

🎯 8/10
Strong - Good candidate
AI-powered assessment

✅ Strengths
1. Clear explanation of key concepts
2. Mentioned practical examples
3. Professional terminology

💡 Areas for Improvement
1. Could discuss when to use each method
2. Add more depth on trade-offs
3. Mention real-world applications

💬 Final Comment
Solid answer demonstrating good understanding. Adding
specific examples and practical use cases would strengthen
your response for senior-level interviews.
```

---

## 🔧 API Reference

### `evaluateAnswer(question, userAnswer, role, questionType)`

**Parameters:**
- `question` (string) - The interview question
- `userAnswer` (string) - User's answer text
- `role` (string) - Job role (default: "Data Scientist")
- `questionType` (string) - Question category: ml, stats, sql, coding, case, behavioral

**Returns:** Promise<Object>
```javascript
{
    score: 0-10,
    strengths: ["...", "..."],
    improvements: ["...", "..."],
    final_comment: "..."
}
```

### `displayEvaluation(evaluation, containerId)`

**Parameters:**
- `evaluation` (Object) - Result from evaluateAnswer()
- `containerId` (string) - ID of DOM element to display results

**Returns:** void (displays HTML in container)

### `createAnswerInputUI(questionText, containerId, options)`

**Parameters:**
- `questionText` (string) - The question to answer
- `containerId` (string) - ID of DOM element for the UI
- `options` (Object) - `{ role: string, questionType: string }`

**Returns:** void (creates complete answer input + evaluation UI)

### `getScoreInterpretation(score)`

**Parameters:**
- `score` (number) - Score from 0-10

**Returns:** string
- 9-10: "Excellent - Hire immediately!"
- 7-8: "Strong - Good candidate"
- 5-6: "Acceptable - Needs improvement"
- 3-4: "Weak - Significant gaps"
- 0-2: "Poor - Not ready"

---

## 🎨 Styling

The evaluation UI uses your existing CSS variables:
- `--bg` - Background color
- `--bg-secondary` - Secondary background
- `--text` - Text color
- `--text-light` - Light text color
- `--accent` - Accent color
- `--accent-light` - Light accent color

It will automatically match your light/dark theme!

---

## 💰 Cost

**FREE** with Gemini API free tier:
- 15 requests/minute = 15 answer evaluations/minute
- 1,500 requests/day = 1,500 evaluations/day
- More than enough for interview practice!

**Compared to alternatives:**
- OpenAI GPT: $0.002 per evaluation
- Claude API: $0.003 per evaluation
- **Gemini: $0.00 (FREE!)** ✅

---

## 🐛 Troubleshooting

### Error: "Gemini API key not configured"
**Solution:** Add your API key to `config.js`:
```javascript
GEMINI_API_KEY: 'AIzaSy...'  // Your actual key
```

### Error: "403 Forbidden" or "API key not valid"
**Solution:**
1. Check your API key is correct
2. Make sure you copied the full key
3. API key must start with `AIza`
4. Get a new key at https://aistudio.google.com/app/apikey

### Evaluation returns generic error
**Solution:**
1. Check browser console for details
2. Verify internet connection
3. Check if you've exceeded free tier limit (1,500/day)

### UI doesn't appear
**Solution:**
1. Make sure `gemini-evaluator.js` is loaded after `config.js`
2. Check browser console for JavaScript errors
3. Verify container ID exists in your HTML

---

## 🚀 Next Steps

1. **Get your Gemini API key** - https://aistudio.google.com/app/apikey
2. **Add it to config.js**
3. **Include gemini-evaluator.js in your HTML**
4. **Choose an integration option** (Option A recommended)
5. **Test it out!**

---

## 💡 Pro Tips

1. **Save user answers** to localStorage for practice history
2. **Track scores over time** to show improvement
3. **Add difficulty adjustment** based on user performance
4. **Create practice sets** focusing on weak areas
5. **Add timer** for realistic interview practice
6. **Export results** to PDF for review

---

## 📞 Need Help?

The gemini-evaluator.js file is fully documented with JSDoc comments.
Open it in your code editor to see detailed function documentation!

---

**You're all set!** Your interview coach now has AI-powered evaluation. 🎉

Get your API key and start helping users practice their answers!
