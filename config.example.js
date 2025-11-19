// Configuration file for API keys
// INSTRUCTIONS:
// 1. Copy this file and rename it to "config.js"
// 2. Replace the placeholder values with your actual API keys
// 3. NEVER commit config.js to Git (it's in .gitignore)

const CONFIG = {
    // Get your free Groq API key from: https://console.groq.com/keys
    GROQ_API_KEY: 'YOUR_GROQ_API_KEY_HERE',

    // Supabase credentials (these are public and safe to commit)
    SUPABASE_URL: 'YOUR_SUPABASE_URL_HERE',
    SUPABASE_ANON_KEY: 'YOUR_SUPABASE_ANON_KEY_HERE',

    // Get your free Gemini API key from: https://aistudio.google.com/app/apikey
    // This enables AI-powered answer evaluation (NEW!)
    GEMINI_API_KEY: 'YOUR_GEMINI_API_KEY_HERE'  // <-- ADD YOUR KEY HERE
};
