"""
Simple Flask API server to generate embeddings for the frontend.
This handles the embedding generation so you don't need to expose API keys in the browser.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Load the embedding model once at startup
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded!")


@app.route('/api/embed', methods=['POST'])
def generate_embedding():
    """
    Generate embedding for the provided text.

    Request body:
    {
        "text": "What is machine learning?"
    }

    Response:
    {
        "embedding": [0.123, -0.456, ...],
        "dimension": 384
    }
    """
    try:
        data = request.get_json()

        if not data or 'text' not in data:
            return jsonify({'error': 'Missing "text" in request body'}), 400

        text = data['text']

        if not text.strip():
            return jsonify({'error': 'Text cannot be empty'}), 400

        # Generate embedding
        embedding = model.encode([text])[0].tolist()

        return jsonify({
            'embedding': embedding,
            'dimension': len(embedding)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        'status': 'ok',
        'model': 'all-MiniLM-L6-v2',
        'dimension': 384
    })


@app.route('/')
def index():
    """API documentation"""
    return """
    <html>
        <head><title>Embedding API</title></head>
        <body style="font-family: sans-serif; max-width: 800px; margin: 50px auto; padding: 20px;">
            <h1>🤖 Embedding API Server</h1>
            <p>This API generates vector embeddings for text using sentence-transformers.</p>

            <h2>Endpoints</h2>

            <h3>POST /api/embed</h3>
            <p>Generate embedding for text</p>
            <pre style="background: #f5f5f5; padding: 15px; border-radius: 5px;">
{
    "text": "What is machine learning?"
}
            </pre>

            <h3>GET /api/health</h3>
            <p>Check API health status</p>

            <h2>Usage Example</h2>
            <pre style="background: #f5f5f5; padding: 15px; border-radius: 5px;">
fetch('http://localhost:5000/api/embed', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: 'Your query here' })
})
.then(res => res.json())
.then(data => console.log(data.embedding));
            </pre>
        </body>
    </html>
    """


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"\n{'='*60}")
    print(f"🚀 Embedding API Server")
    print(f"{'='*60}")
    print(f"Running on: http://localhost:{port}")
    print(f"Health check: http://localhost:{port}/api/health")
    print(f"{'='*60}\n")

    app.run(host='0.0.0.0', port=port, debug=True)
