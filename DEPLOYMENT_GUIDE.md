# Deployment Guide - Make Your Search Public!

This guide shows you how to deploy your semantic search application so others can use it.

---

## 📋 What We're Deploying

1. **Frontend** (HTML/CSS/JS) - The search interface
2. **Backend API** (Flask) - Generates embeddings
3. **Database** (Supabase) - Already set up!

---

## 🎯 Quick Deployment Options

### Option 1: Simple & Free (Recommended for Beginners)
- **Frontend**: Netlify or Vercel (free)
- **Backend**: Railway or Render (free tier)
- **Database**: Supabase (already set up)

### Option 2: All-in-One
- **Full Stack**: Heroku or Railway
- **Database**: Supabase (already set up)

### Option 3: Self-Hosted
- **Your own server**: DigitalOcean, AWS, etc.

---

## 🚀 Option 1: Deploy Frontend (Netlify)

### Step 1: Prepare Frontend Files

1. Open `frontend/app.js`
2. Update these lines with your Supabase credentials:

```javascript
const SUPABASE_URL = 'https://your-project.supabase.co';
const SUPABASE_ANON_KEY = 'your-anon-key-here';
```

3. Save the file

### Step 2: Create GitHub Repository

```bash
cd "/Users/basilsuhail/folders/Data Sets/Data_Science_Interview_Questions"

# If not already a git repo
git init
git add frontend/
git commit -m "Add frontend for deployment"

# Push to GitHub
git remote add origin https://github.com/BasilSuhail/Data_Science_Interview_Questions.git
git push -u origin main
```

### Step 3: Deploy to Netlify

1. Go to https://netlify.com
2. Sign up/login with GitHub
3. Click **"Add new site"** → **"Import an existing project"**
4. Connect to GitHub
5. Select your `Data_Science_Interview_Questions` repository
6. Configure:
   - **Base directory**: `frontend`
   - **Build command**: (leave empty)
   - **Publish directory**: `.` (dot)
7. Click **"Deploy site"**

### Step 4: Get Your URL

After deployment (1-2 minutes):
- You'll get a URL like: `https://your-site-name.netlify.app`
- Test it!

⚠️ **Note**: Without the backend API, search will use random embeddings (not meaningful results). Continue to deploy the backend API below.

---

## 🔧 Option 1: Deploy Backend API (Railway)

### Step 1: Prepare Backend

Create a `requirements.txt` file:

```bash
cd "/Users/basilsuhail/folders/Data Sets/Data_Science_Interview_Questions/frontend"

# Create requirements.txt
cat > requirements.txt << EOF
flask==3.0.0
flask-cors==4.0.0
sentence-transformers==2.2.2
gunicorn==21.2.0
EOF
```

### Step 2: Create Procfile

```bash
cat > Procfile << EOF
web: gunicorn api_server:app
EOF
```

### Step 3: Deploy to Railway

1. Go to https://railway.app
2. Sign up/login with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Select your repository
6. Railway will auto-detect Python
7. Set environment variables:
   - Click on your service
   - Go to **"Variables"**
   - Add: `PORT` = `5000`
8. Click **"Deploy"**

### Step 4: Get Your API URL

After deployment:
- Click **"Settings"** → **"Domains"**
- You'll get: `https://your-app.railway.app`
- Test: `https://your-app.railway.app/api/health`

### Step 5: Update Frontend

Go back to Netlify:
1. Open your site settings
2. Go to **"Environment variables"**
3. Add: `API_URL` = `https://your-app.railway.app`
4. Redeploy

**OR** update `frontend/app.js`:

```javascript
// Change this line:
const response = await fetch('/api/embed', {

// To this:
const response = await fetch('https://your-app.railway.app/api/embed', {
```

---

## 🎨 Customization

### Change Site Name

**Netlify:**
1. Site settings → **"Change site name"**
2. Pick something like: `ds-interview-search`
3. Your URL becomes: `https://ds-interview-search.netlify.app`

### Add Custom Domain

1. Buy a domain (Namecheap, Google Domains, etc.)
2. In Netlify: **"Domain settings"** → **"Add custom domain"**
3. Follow DNS setup instructions

---

## 🔒 Security & Performance

### 1. Secure Your API

Add rate limiting to `api_server.py`:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/embed', methods=['POST'])
@limiter.limit("10 per minute")
def generate_embedding():
    # ... existing code
```

Install:
```bash
pip install flask-limiter
```

### 2. Enable Caching

Update `api_server.py`:

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/embed', methods=['POST'])
@cache.memoize(timeout=3600)  # Cache for 1 hour
def generate_embedding():
    # ... existing code
```

### 3. Add Analytics

In `frontend/index.html`, add before `</head>`:

```html
<!-- Google Analytics (optional) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-GA-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR-GA-ID');
</script>
```

---

## 📊 Monitor Your Deployment

### Check Supabase Usage

1. Supabase Dashboard → **"Usage"**
2. Monitor:
   - Database size
   - API requests
   - Bandwidth

Free tier limits:
- 500MB database
- 2GB bandwidth
- 50,000 monthly active users

### Check Railway Logs

1. Railway Dashboard → Your service
2. Click **"Logs"**
3. Monitor for errors

### Check Netlify Analytics

1. Netlify Dashboard → Your site
2. **"Analytics"** tab
3. See visitor stats

---

## 🐛 Troubleshooting

### Frontend shows "Failed to create embedding"

**Problem**: Backend API not configured
**Solution**:
1. Make sure backend is deployed
2. Update API URL in frontend
3. Check CORS settings in `api_server.py`

### Search returns no results

**Problem**: No data in Supabase
**Solution**:
1. Run `python upload_to_supabase.py`
2. Verify data in Supabase Table Editor

### Backend API times out

**Problem**: Model loading takes too long
**Solution**:
1. Railway free tier has limits
2. Consider upgrading to paid tier
3. Or use serverless functions (see below)

### CORS errors in browser console

**Problem**: Frontend can't access backend
**Solution**: Update `api_server.py`:

```python
CORS(app, origins=[
    'https://your-netlify-site.netlify.app',
    'http://localhost:*'  # For local testing
])
```

---

## ⚡ Advanced: Serverless Deployment

### Using Vercel Serverless Functions

Create `api/embed.py`:

```python
from http.server import BaseHTTPRequestHandler
import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        text = data.get('text', '')
        embedding = model.encode([text])[0].tolist()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        response = json.dumps({'embedding': embedding})
        self.wfile.write(response.encode())
```

Create `vercel.json`:

```json
{
  "functions": {
    "api/embed.py": {
      "memory": 1024,
      "maxDuration": 10
    }
  }
}
```

Deploy:
```bash
npm install -g vercel
vercel
```

---

## 📱 Mobile-Friendly

The frontend is already responsive, but you can improve:

### Add PWA Support

Create `manifest.json`:

```json
{
  "name": "DS Interview Search",
  "short_name": "DS Search",
  "description": "Semantic search for data science interview questions",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#667eea",
  "theme_color": "#667eea",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    }
  ]
}
```

Add to `index.html`:

```html
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#667eea">
```

---

## 💰 Cost Estimates

### Free Tier (Perfect for Starting)
- Supabase: Free (500MB, 2GB bandwidth)
- Netlify: Free (100GB bandwidth)
- Railway: Free ($5 credit/month)
- **Total: $0/month**

### Paid Tier (For Growth)
- Supabase Pro: $25/month (8GB, 100GB bandwidth)
- Railway Hobby: $5/month (500 hours)
- Netlify: Still free!
- **Total: ~$30/month**

### Production Scale
- Supabase Pro: $25/month
- Railway Pro: $20/month (more resources)
- Custom domain: $12/year
- **Total: ~$45/month + domain**

---

## 🎉 You're Live!

After completing these steps:

1. ✅ Frontend is live on Netlify
2. ✅ Backend API is running on Railway
3. ✅ Database is on Supabase
4. ✅ Anyone can search your data!

### Share Your Links

```
🌐 Website: https://your-site.netlify.app
🔍 API: https://your-api.railway.app
💾 Database: Supabase (private)
📂 GitHub: https://github.com/BasilSuhail/Data_Science_Interview_Questions
```

---

## 📚 Next Steps

1. **Add more data**: Keep uploading more books
2. **Improve search**: Fine-tune the search algorithm
3. **Add features**:
   - Question bookmarking
   - User accounts
   - Question voting
   - Export functionality
4. **Get feedback**: Share with friends, get their input
5. **Iterate**: Keep improving!

---

## 🆘 Need Help?

- **Netlify Docs**: https://docs.netlify.com
- **Railway Docs**: https://docs.railway.app
- **Supabase Docs**: https://supabase.com/docs
- **Flask Docs**: https://flask.palletsprojects.com

---

Congratulations! Your semantic search engine is now public! 🚀
