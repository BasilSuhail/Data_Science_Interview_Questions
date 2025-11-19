/**
 * GEMINI AI EVALUATOR - JavaScript Version
 *
 * Adds AI-powered answer evaluation to your Interview Coach web app.
 *
 * Features:
 * - Score user answers (0-10)
 * - Identify strengths
 * - Suggest improvements
 * - Provide actionable feedback
 *
 * Usage:
 * 1. Add GEMINI_API_KEY to config.js
 * 2. Include this file in your HTML: <script src="gemini-evaluator.js"></script>
 * 3. Call: evaluateAnswer(question, userAnswer, role, questionType)
 */

/**
 * Evaluate a user's answer using Gemini AI
 *
 * @param {string} question - The interview question
 * @param {string} userAnswer - The user's answer
 * @param {string} role - Job role (default: "Data Scientist")
 * @param {string} questionType - Question type: ml, stats, sql, coding, case, behavioral
 * @returns {Promise<Object>} Evaluation result with score, strengths, improvements, comment
 */
async function evaluateAnswer(question, userAnswer, role = "Data Scientist", questionType = "general") {
    // Check if Gemini API key is configured
    if (!CONFIG.GEMINI_API_KEY || CONFIG.GEMINI_API_KEY === 'YOUR_GEMINI_API_KEY_HERE') {
        return {
            error: 'Gemini API key not configured',
            message: 'Please add your Gemini API key to config.js to enable answer evaluation.',
            instructions: 'Get a free API key at: https://aistudio.google.com/app/apikey',
            score: 0,
            strengths: [],
            improvements: ['Configure Gemini API to get evaluation'],
            final_comment: 'Add your Gemini API key to enable AI-powered feedback.'
        };
    }

    const prompt = `You are an expert interview evaluator for data science and software engineering roles.

Evaluate the candidate's answer in these categories:
- Clarity: Is the answer clear and well-structured?
- Relevance: Does it directly answer the question?
- Technical Depth: Shows understanding of concepts?
- Communication: Professional and articulate?
- Completeness: Covers key points?

Return ONLY valid JSON (no markdown, no code blocks):

{
  "score": <0-10>,
  "strengths": ["point 1", "point 2", "point 3"],
  "improvements": ["point 1", "point 2"],
  "final_comment": "2-3 sentence summary with actionable advice"
}

Question: ${question}
Answer: ${userAnswer}
Role: ${role}
Question Type: ${questionType}`;

    try {
        const response = await fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=' + CONFIG.GEMINI_API_KEY, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: prompt
                    }]
                }],
                generationConfig: {
                    temperature: 0.7,
                    maxOutputTokens: 1024
                }
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Gemini API error: ${errorData.error?.message || response.statusText}`);
        }

        const result = await response.json();

        // Extract text from Gemini response
        const text = result.candidates?.[0]?.content?.parts?.[0]?.text;

        if (!text) {
            throw new Error('No response from Gemini API');
        }

        // Parse JSON from response
        const evaluation = parseEvaluationResponse(text);

        return evaluation;

    } catch (error) {
        console.error('Gemini evaluation error:', error);
        return {
            error: error.message,
            score: 0,
            strengths: [],
            improvements: [`Error: ${error.message}`],
            final_comment: 'Unable to evaluate answer due to technical error. Please try again.'
        };
    }
}

/**
 * Parse Gemini response and extract JSON evaluation
 * @param {string} text - Response text from Gemini
 * @returns {Object} Parsed evaluation object
 */
function parseEvaluationResponse(text) {
    // Remove markdown code blocks if present
    let cleaned = text.replace(/```json/g, '').replace(/```/g, '').trim();

    // Try to extract JSON object
    const jsonMatch = cleaned.match(/\{[\s\S]*\}/);

    if (jsonMatch) {
        try {
            const parsed = JSON.parse(jsonMatch[0]);

            // Validate required fields
            if (parsed.score !== undefined &&
                Array.isArray(parsed.strengths) &&
                Array.isArray(parsed.improvements) &&
                parsed.final_comment) {
                return parsed;
            }
        } catch (e) {
            console.error('JSON parse error:', e);
        }
    }

    // Fallback: return error
    return {
        error: 'Failed to parse evaluation',
        raw_response: text,
        score: 0,
        strengths: [],
        improvements: ['Could not parse AI evaluation response'],
        final_comment: 'Evaluation format error. Please try again.'
    };
}

/**
 * Get human-readable interpretation of score
 * @param {number} score - Score from 0-10
 * @returns {string} Interpretation text
 */
function getScoreInterpretation(score) {
    if (score >= 9) return "Excellent - Hire immediately!";
    if (score >= 7) return "Strong - Good candidate";
    if (score >= 5) return "Acceptable - Needs some improvement";
    if (score >= 3) return "Weak - Significant gaps";
    return "Poor - Not ready";
}

/**
 * Display evaluation results in a nice format
 * @param {Object} evaluation - Evaluation result from evaluateAnswer()
 * @param {string} containerId - ID of container element to display results
 */
function displayEvaluation(evaluation, containerId) {
    const container = document.getElementById(containerId);

    if (!container) {
        console.error(`Container #${containerId} not found`);
        return;
    }

    const score = evaluation.score || 0;
    const interpretation = getScoreInterpretation(score);

    let html = `
        <div style="background: var(--bg-secondary); border: 2px solid var(--accent); border-radius: 0.75rem; padding: 1.5rem; margin: 1.5rem 0;">
            <h3 style="margin-bottom: 1rem; color: var(--accent); font-size: 1.25rem;">📊 AI Evaluation Results</h3>

            <div style="margin-bottom: 1.5rem;">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                    <span style="font-size: 2.5rem; font-weight: 700; color: var(--accent);">${score}/10</span>
                    <div>
                        <div style="font-weight: 600; color: var(--text);">${interpretation}</div>
                        <div style="font-size: 0.875rem; color: var(--text-light);">AI-powered assessment</div>
                    </div>
                </div>
            </div>

            <div style="margin-bottom: 1.25rem;">
                <h4 style="color: #10b981; margin-bottom: 0.75rem; font-size: 1rem;">✅ Strengths</h4>
                <ul style="margin: 0; padding-left: 1.5rem; list-style: disc;">
                    ${(evaluation.strengths || []).map(s => `<li style="margin-bottom: 0.5rem;">${s}</li>`).join('')}
                </ul>
            </div>

            <div style="margin-bottom: 1.25rem;">
                <h4 style="color: #f59e0b; margin-bottom: 0.75rem; font-size: 1rem;">💡 Areas for Improvement</h4>
                <ul style="margin: 0; padding-left: 1.5rem; list-style: disc;">
                    ${(evaluation.improvements || []).map(i => `<li style="margin-bottom: 0.5rem;">${i}</li>`).join('')}
                </ul>
            </div>

            <div style="background: var(--bg); border-left: 3px solid var(--accent); padding: 1rem; border-radius: 0.5rem;">
                <h4 style="color: var(--text); margin-bottom: 0.5rem; font-size: 0.9rem; font-weight: 600;">💬 Final Comment</h4>
                <p style="margin: 0; color: var(--text-light); line-height: 1.6;">${evaluation.final_comment || 'N/A'}</p>
            </div>
        </div>
    `;

    // Show error if present
    if (evaluation.error) {
        html = `
            <div style="background: #fee2e2; border: 2px solid #ef4444; border-radius: 0.75rem; padding: 1.5rem; margin: 1.5rem 0;">
                <h3 style="margin-bottom: 1rem; color: #ef4444;">⚠️ Evaluation Error</h3>
                <p style="margin-bottom: 0.5rem;"><strong>Error:</strong> ${evaluation.error}</p>
                ${evaluation.message ? `<p style="margin-bottom: 0.5rem;">${evaluation.message}</p>` : ''}
                ${evaluation.instructions ? `<p style="margin: 0;"><small>${evaluation.instructions}</small></p>` : ''}
            </div>
        `;
    }

    container.innerHTML = html;
}

/**
 * Create an interactive answer input UI for a question
 * @param {string} questionText - The question to answer
 * @param {string} containerId - ID of container for the UI
 * @param {Object} options - Optional configuration {role, questionType}
 */
function createAnswerInputUI(questionText, containerId, options = {}) {
    const container = document.getElementById(containerId);

    if (!container) {
        console.error(`Container #${containerId} not found`);
        return;
    }

    const role = options.role || "Data Scientist";
    const questionType = options.questionType || "general";

    const html = `
        <div style="background: var(--bg-secondary); border-radius: 0.75rem; padding: 1.5rem; margin: 1.5rem 0;">
            <h4 style="margin-bottom: 1rem; color: var(--accent);">📝 Your Answer</h4>
            <textarea
                id="${containerId}-answer-input"
                style="width: 100%; min-height: 150px; padding: 1rem; border: 2px solid var(--border); border-radius: 0.5rem; background: var(--bg); color: var(--text); font-size: 0.9375rem; font-family: inherit; resize: vertical;"
                placeholder="Type your answer here..."
            ></textarea>
            <button
                onclick="submitAnswerForEvaluation('${containerId}')"
                style="margin-top: 1rem; padding: 0.75rem 1.5rem; background: var(--accent); color: white; border: none; border-radius: 0.5rem; font-weight: 500; cursor: pointer; transition: background 0.2s;"
                onmouseover="this.style.background='var(--accent-light)'"
                onmouseout="this.style.background='var(--accent)'"
            >
                Get AI Feedback
            </button>
            <div id="${containerId}-evaluation-result"></div>
        </div>
    `;

    container.innerHTML = html;

    // Store question data for later evaluation
    window[`${containerId}_questionData`] = {
        question: questionText,
        role: role,
        questionType: questionType
    };
}

/**
 * Submit answer for evaluation (called by UI button)
 * @param {string} containerId - Container ID
 */
async function submitAnswerForEvaluation(containerId) {
    const answerInput = document.getElementById(`${containerId}-answer-input`);
    const resultDiv = document.getElementById(`${containerId}-evaluation-result`);
    const questionData = window[`${containerId}_questionData`];

    if (!answerInput || !questionData) {
        console.error('Answer input or question data not found');
        return;
    }

    const userAnswer = answerInput.value.trim();

    if (!userAnswer) {
        resultDiv.innerHTML = `
            <div style="background: #fef3c7; border: 2px solid #f59e0b; border-radius: 0.5rem; padding: 1rem; margin-top: 1rem;">
                <p style="margin: 0; color: #92400e;">Please type an answer before submitting.</p>
            </div>
        `;
        return;
    }

    // Show loading
    resultDiv.innerHTML = `
        <div style="text-align: center; padding: 2rem; color: var(--text-light);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⏳</div>
            <div>Evaluating your answer with Gemini AI...</div>
        </div>
    `;

    // Evaluate
    const evaluation = await evaluateAnswer(
        questionData.question,
        userAnswer,
        questionData.role,
        questionData.questionType
    );

    // Display results
    displayEvaluation(evaluation, `${containerId}-evaluation-result`);
}

// Make functions globally available
window.evaluateAnswer = evaluateAnswer;
window.getScoreInterpretation = getScoreInterpretation;
window.displayEvaluation = displayEvaluation;
window.createAnswerInputUI = createAnswerInputUI;
window.submitAnswerForEvaluation = submitAnswerForEvaluation;

console.log('✅ Gemini AI Evaluator loaded successfully!');
console.log('📘 Usage: evaluateAnswer(question, userAnswer, role, questionType)');
