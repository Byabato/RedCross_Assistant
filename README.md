# Red Cross Assistant

An AI-powered first aid assistant that provides guidance based on official Red Cross training materials using RAG (Retrieval-Augmented Generation).

## 🚀 Quick Links

- **🌍 Live Demo:** https://redcrossassistant-production.up.railway.app *(Deploy your own below)*
- **📖 Deployment:** See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for full walkthrough
- **⚡ Quick Start:** See [QUICK_START.md](./QUICK_START.md) for 10-minute deployment
- **🧪 Testing:** See [TESTING_GUIDE.md](./TESTING_GUIDE.md) for validation procedures
- **📋 Checklist:** See [DEPLOY_CHECKLIST.md](./DEPLOY_CHECKLIST.md) for step-by-step visual guide

## ✨ Features

- **Conversational AI**: Natural, human-like responses powered by LLM
- **Strict Quote Mode**: Direct quotes from source material
- **Web Interface**: Professional, user-friendly UI  
- **CLI Tool**: Command-line interface for quick access
- **Vector Search**: Fast semantic search across Red Cross materials
- **Caching**: Instant startup after first run
- **Free Hosting**: Deploy on Railway (free tier, no payments)

## 🎯 Deploy to Railway in 10 Minutes (FREE!)

This project is **fully configured** for Railway deployment. Follow these 3 steps:

### Step 1: Create Railway Account (3 min)
```bash
1. Go to https://railway.app
2. Sign up with GitHub
3. Authorize Railway
```

### Step 2: Deploy (5 min)
```bash
1. In Railway: "New Project" → "Deploy from GitHub"
2. Select "RedCrossAssistant"  
3. Click "Deploy Now"
4. Wait for green checkmark ✅
```

### Step 3: Test (2 min)
```bash
# Copy the URL from Railway dashboard
# Open: https://your-url/
# Ask a question like "What is first aid?"
# Done! 🎉
```

**See [DEPLOY_CHECKLIST.md](./DEPLOY_CHECKLIST.md) for detailed visual guide**

## 📋 Files for Deployment

Everything needed is already prepared:

- ✅ **Procfile** - Tells Railway how to start the app
- ✅ **runtime.txt** - Specifies Python version
- ✅ **requirements.txt** - All dependencies pinned
- ✅ **.gitignore** - Prevents uploading cache files

## 🔗 API Usage

### Health Check
```bash
GET /health
# Response: {"status":"ok","chunks":150}
```

### Chat API
```bash
curl -X POST https://your-url/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How do I treat a burn?",
    "top_n": 5,
    "strict_quotes": false,
    "debug": false
  }'
```

### Web Interface
```
Open: https://your-url/
```

## 💻 Local Development

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai/) installed and running
- Ollama models: `mistral` and `hf.co/CompendiumLabs/bge-base-en-v1.5-gguf`

### Installation

```bash
# Clone the repository
git clone https://github.com/Byabato/RedCross_Assistant.git
cd RedCrossAssistant

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Pull required Ollama models
ollama pull mistral
ollama pull hf.co/CompendiumLabs/bge-base-en-v1.5-gguf
```

### Usage

**Web Interface** (Recommended):
```bash
python api.py
```
Then open http://localhost:8000

**Command Line**:
```bash
python main.py
```

## 📁 Project Structure

```
RedCrossAssistant/
├── app/
│   └── rag/
│       ├── database.py      # Vector database management
│       ├── retrieval.py     # Semantic search
│       └── generation.py    # Response generation
├── ingestion/
│   └── dataset_loader.py    # Text chunking
├── web/
│   ├── index.html          # Web UI
│   └── favicon.svg         # Red Cross icon
├── data/
│   └── redcross.txt        # Source material
├── api.py                  # FastAPI server
├── main.py                 # CLI interface
├── Procfile                # Railway deployment config
├── runtime.txt             # Python version spec
├── requirements.txt        # Dependencies
├── DEPLOYMENT_GUIDE.md     # Full deployment walkthrough
├── QUICK_START.md          # 10-min quick reference
├── TESTING_GUIDE.md        # Testing procedures
└── README.md               # This file
```

## ⚙️ Configuration

Edit these constants in `api.py` or `main.py`:

- `DATA_FILE`: Path to your source material (default: `data/redcross.txt`)
- `MAX_CHUNK_WORDS`: Chunk size for text splitting (default: `200`)
- `DEFAULT_TOP_N`: Number of chunks to retrieve (default: `5`)
- `DEFAULT_STRICT`: Use strict quotes vs conversational (default: `False`)

## 🧠 How It Works

1. **Ingestion**: Splits Red Cross materials into chunks
2. **Embedding**: Converts chunks to vectors using Ollama BGE model
3. **Storage**: Caches vectors in `vector_db.json`
4. **Retrieval**: Finds relevant chunks via cosine similarity
5. **Generation**: LLM (Mistral) creates natural responses from retrieved chunks

## 🎨 Response Modes

### Conversational (Default)
LLM generates human-friendly explanations while staying grounded in source material.

### Strict Quotes
Returns direct quotes from source materials formatted as numbered points.

### Debug Mode
Shows raw chunks with similarity scores for troubleshooting.

## 🌍 Free Hosting Details

**Railway Free Tier Includes:**
- 5 GB RAM-hours per month
- Persistent file storage
- Unlimited bandwidth
- 99%+ uptime
- Auto-scaling
- **Zero cost!**

**Realistic Usage:**
- 100 queries/day = ~3 GB/month (well within 5 GB limit)

## ⚡ Performance

- **First Request**: 30-90 seconds (AI models loading)
- **Cached Requests**: <2 seconds
- **Memory Usage**: ~400-500 MB stable
- **Concurrent Users**: ~5-10 simultaneously (free tier)

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Build fails on Railway | Check logs, fix `requirements.txt`, `git push` |
| 503 Service Unavailable | Wait 3-5 minutes for startup |
| Slow first response | Normal! AI models loading (1-2 min) |
| Page not loading | Verify Railway deployment status |

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md#part-6-common-issues--fixes) for more troubleshooting.

## 📊 Monitoring

After deployment, monitor your app:

1. **Railway Dashboard**: Go to project → "Metrics"
2. **Health Endpoint**: `https://your-url/health`
3. **Logs**: Railway Dashboard → "Logs" tab

## 🔄 Updates & Redeployment

```bash
# Make changes to code
git add .
git commit -m "Your description"
git push origin main

# Railway auto-redeploys in 1-2 minutes!
```

## 📚 Documentation

| Guide | Purpose | Time |
|-------|---------|------|
| [QUICK_START.md](./QUICK_START.md) | 10-minute deployment | 3 min |
| [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) | Complete walkthrough | 10 min |
| [TESTING_GUIDE.md](./TESTING_GUIDE.md) | Testing & validation | 8 min |
| [DEPLOY_CHECKLIST.md](./DEPLOY_CHECKLIST.md) | Visual step-by-step | 5 min |

## 📜 License

This project is for educational purposes. Red Cross materials are used under fair use for training.

## 🙏 Acknowledgments

- Built with FastAPI, Ollama, and modern RAG techniques
- Red Cross training materials for source content
- Railway for free, reliable hosting

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

---

**Ready to deploy? Start with [DEPLOY_CHECKLIST.md](./DEPLOY_CHECKLIST.md)** ⚡

