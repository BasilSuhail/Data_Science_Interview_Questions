// Configuration - Replace these with your Supabase credentials
const SUPABASE_URL = 'YOUR_SUPABASE_URL_HERE';
const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY_HERE';

// Initialize Supabase client
const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Embedding model endpoint (you'll need to set this up)
const EMBEDDING_API_URL = 'https://api.openai.com/v1/embeddings';
const OPENAI_API_KEY = ''; // Optional: for production use

// Simple in-browser embedding (fallback if no API)
// Note: This is a simplified version. For production, use proper API
let embeddingModel = null;

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    await loadStatistics();
    await loadBooks();

    // Enable search on Enter key
    document.getElementById('searchInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            search();
        }
    });
});

// Load books for filter dropdown
async function loadBooks() {
    try {
        const { data, error } = await supabase
            .from('books')
            .select('title, filename')
            .order('title');

        if (error) throw error;

        const bookFilter = document.getElementById('bookFilter');

        data.forEach(book => {
            const option = document.createElement('option');
            option.value = book.filename;
            option.textContent = book.title;
            bookFilter.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading books:', error);
    }
}

// Load and display statistics
async function loadStatistics() {
    try {
        // Get total chunks
        const { count, error: countError } = await supabase
            .from('document_chunks')
            .select('*', { count: 'exact', head: true });

        if (countError) throw countError;

        // Get book count
        const { data: books, error: booksError } = await supabase
            .from('books')
            .select('id');

        if (booksError) throw booksError;

        // Display stats
        const statsGrid = document.getElementById('statsGrid');
        statsGrid.innerHTML = `
            <div class="stat-item">
                <div class="stat-value">${count?.toLocaleString() || 0}</div>
                <div class="stat-label">Text Chunks</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">${books?.length || 0}</div>
                <div class="stat-label">Books Indexed</div>
            </div>
        `;

        document.getElementById('statsContainer').style.display = 'block';
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Main search function
async function search() {
    const query = document.getElementById('searchInput').value.trim();

    if (!query) {
        alert('Please enter a search query');
        return;
    }

    const resultsContainer = document.getElementById('resultsContainer');
    const searchBtn = document.getElementById('searchBtn');

    // Show loading state
    searchBtn.disabled = true;
    resultsContainer.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Searching through books...</p>
        </div>
    `;

    try {
        // Get embedding for the query
        const queryEmbedding = await getEmbedding(query);

        if (!queryEmbedding) {
            throw new Error('Failed to create embedding');
        }

        // Get filter values
        const bookFilter = document.getElementById('bookFilter').value;
        const resultCount = parseInt(document.getElementById('resultCount').value);

        // Call the match_documents function
        const { data, error } = await supabase.rpc('match_documents', {
            query_embedding: queryEmbedding,
            match_count: resultCount,
            filter_book_name: bookFilter || null
        });

        if (error) throw error;

        // Display results
        displayResults(data, query);

    } catch (error) {
        console.error('Search error:', error);
        resultsContainer.innerHTML = `
            <div class="error">
                <strong>Error:</strong> ${error.message}
                <p style="margin-top: 10px; font-size: 0.9rem;">
                    Make sure you've configured your Supabase credentials in app.js
                </p>
            </div>
        `;
    } finally {
        searchBtn.disabled = false;
    }
}

// Get embedding for text (using OpenAI or fallback)
async function getEmbedding(text) {
    // Option 1: Use OpenAI API (recommended for production)
    if (OPENAI_API_KEY) {
        try {
            const response = await fetch('https://api.openai.com/v1/embeddings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${OPENAI_API_KEY}`
                },
                body: JSON.stringify({
                    model: 'text-embedding-ada-002',
                    input: text
                })
            });

            const data = await response.json();
            return data.data[0].embedding;
        } catch (error) {
            console.error('OpenAI API error:', error);
        }
    }

    // Option 2: Use a proxy backend service (recommended)
    // You would call your own backend that handles embeddings
    try {
        const response = await fetch('/api/embed', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });

        const data = await response.json();
        return data.embedding;
    } catch (error) {
        console.warn('Backend embedding service not available');
    }

    // Option 3: For demo purposes, use random embeddings
    // WARNING: This won't give meaningful results!
    console.warn('Using random embeddings - results will not be meaningful');
    console.warn('Please set up OpenAI API key or embedding backend service');

    // Generate 384-dimensional random vector (matching all-MiniLM-L6-v2)
    const randomEmbedding = Array.from({ length: 384 }, () => Math.random() - 0.5);

    // Normalize
    const norm = Math.sqrt(randomEmbedding.reduce((sum, val) => sum + val * val, 0));
    return randomEmbedding.map(val => val / norm);
}

// Display search results
function displayResults(results, query) {
    const resultsContainer = document.getElementById('resultsContainer');

    if (!results || results.length === 0) {
        resultsContainer.innerHTML = `
            <div class="empty-state">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="11" cy="11" r="8"></circle>
                    <path d="M21 21l-4.35-4.35"></path>
                </svg>
                <h3>No results found</h3>
                <p>Try a different search query or adjust your filters</p>
            </div>
        `;
        return;
    }

    let html = `<h2 style="margin-bottom: 20px; color: #333;">
        Found ${results.length} results for "${query}"
    </h2>`;

    results.forEach((result, index) => {
        const similarityPercent = (result.similarity * 100).toFixed(1);

        html += `
            <div class="result-item">
                <div class="result-header">
                    <div>
                        <div class="result-book">${result.book_name.replace(/_/g, ' ')}</div>
                        <div class="result-meta">
                            <span>📄 Page ${result.page_number || 'N/A'}</span>
                        </div>
                    </div>
                    <div class="similarity-badge">${similarityPercent}% match</div>
                </div>
                <div class="result-text">${highlightText(result.chunk_text, query)}</div>
            </div>
        `;
    });

    resultsContainer.innerHTML = html;
}

// Highlight search terms in text
function highlightText(text, query) {
    // Simple highlighting - can be improved
    const words = query.toLowerCase().split(' ');
    let highlightedText = text;

    words.forEach(word => {
        if (word.length > 3) { // Only highlight words longer than 3 chars
            const regex = new RegExp(`(${word})`, 'gi');
            highlightedText = highlightedText.replace(regex, '<mark>$1</mark>');
        }
    });

    return highlightedText;
}

// Add CSS for highlighting
const style = document.createElement('style');
style.textContent = `
    mark {
        background-color: #ffeb3b;
        padding: 2px 4px;
        border-radius: 3px;
        font-weight: 600;
    }
`;
document.head.appendChild(style);
