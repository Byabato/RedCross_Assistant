# ⚡ QUICK START: Deploy to Railway in 10 Minutes

## The 3 Essential Files (Already Created)
✅ `Procfile` - Tells Railway to run: `python api.py`
✅ `runtime.txt` - Specifies Python 3.10.13
✅ `requirements.txt` - All dependencies with versions

## The 3 Steps to Go Live

### Step 1: Verify GitHub Repo (30 seconds)
```bash
# Check your code is pushed
git status  # Should show "nothing to commit"
git log --oneline -n 3  # See recent commits
```

### Step 2: Create Railway Project (3 minutes)
1. Go to [railway.app](https://railway.app)
2. Login with GitHub
3. Click "New Project" → "Deploy from GitHub"
4. Select "RedCrossAssistant"
5. Click "Deploy Now"

### Step 3: Get Your Live URL (5 minutes)
- Wait for green checkmark ✅
- Copy the URL from Railway dashboard
- Test it: Open `https://your-url/health` in browser
- You should see: `{"status":"ok","chunks":150}`

**That's it! You're live! 🎉**

---

## Immediate Testing

### Test 1: Web Interface (30 seconds)
```
Visit: https://your-url/
You should see: Red Cross Assistant chat interface
```

### Test 2: Ask a Question (1 minute)
```
In web UI, type: "What is CPR?"
You should get: A response about CPR
Note: First response takes 30-60 seconds (model loading)
```

### Test 3: API Call (30 seconds)
```bash
curl -X POST https://your-url/chat \
  -H "Content-Type: application/json" \
  -d '{"query":"How do I treat a burn?"}'
```

---

## Troubleshooting Quick Fixes

| Issue | Fix |
|-------|-----|
| 503 Service Unavailable | Wait 3-5 minutes for startup |
| Page won't load | Check Railway dashboard for red X |
| Build failed | Railway logs show the error - fix and push |
| Slow first response | Normal! ML models loading (up to 2 min) |
| Updated code not live | Changes auto-deploy when you `git push` |

---

## Make Changes & Redeploy (Instant!)

```bash
# Make code changes locally
# Then:
git add .
git commit -m "Your change description"
git push

# Railway auto-redeploys in 1-2 minutes!
```

---

## Share Your Live Link!

```
Your Red Cross Assistant is now live at:
https://[your-railway-url]

Send this to stakeholders, team members, or end users!
```

---

## What's Running on Railway?

- **Framework:** FastAPI (Python web server)
- **AI Model:** Ollama (Open-source LLM)
- **Interface:** HTML/CSS/JavaScript (in browser)
- **Database:** Vector database (JSON file)
- **Storage:** Persistent across restarts

---

## Free Tier Limits (Plenty for You!)

- **Monthly quota:** 5 GB RAM hours
- **Concurrent users:** ~5-10 simultaneously
- **Uptime:** 99%+ reliable
- **Auto-scaling:** Included
- **Cost:** $0 forever (free tier)

---

## Next Steps (Optional)

### Add Custom Domain (Free)
1. Railway Settings → Domain
2. Add your domain (if you have one)
3. Update DNS records

### Monitor Performance
- Railway Dashboard → "Metrics" tab
- See CPU, memory, requests in real-time

### View Logs
- Railway Dashboard → "Logs" tab
- Troubleshoot any issues

### Scale Up (If Needed)
- Railway → Project Settings
- Increase RAM/CPU (still within free tier)

---

## Support Resources

- **Railway Docs:** https://docs.railway.app/
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Your Project Files:**
  - [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - Full guide
  - [TESTING_GUIDE.md](./TESTING_GUIDE.md) - Test procedures

---

**Your Red Cross Assistant is now live and accessible worldwide! 🌍🚀**

Questions? Check the detailed guides in your repo.
