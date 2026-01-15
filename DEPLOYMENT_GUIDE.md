# 🚀 Deployment Guide: Red Cross Assistant on Railway

## Part 1: Prerequisites & Setup

### ✅ What You Need (ALL FREE):
- GitHub account (free)
- Railway account (free tier, 5GB/month)
- Git installed on your computer
- About 10 minutes

---

## Part 2: Prepare Your Project

### Step 1: Verify Project Files are Committed
Your repo should already have been pushed to GitHub. Check:
```bash
cd d:\projects2026\RedCrossAssistant
git status
```
If there are uncommitted changes, commit them:
```bash
git add .
git commit -m "Prepare for Railway deployment"
git push -u origin main
```

### Step 2: Verify Deployment Files Exist
These should be in your root directory:
- ✅ `Procfile` - Tells Railway how to start the app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `.gitignore` - Prevents uploading unnecessary files
- ✅ `requirements.txt` - Updated with pinned versions

**Verify:**
```bash
ls -la Procfile runtime.txt .gitignore requirements.txt
```

---

## Part 3: Deploy on Railway (The Easy Part!)

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Click "Login" → "Sign up with GitHub"
3. Authorize Railway to access your GitHub
4. Skip any setup wizards

### Step 2: Create New Project
1. Click **"New Project"** button
2. Click **"Deploy from GitHub repo"**
3. Search for **"RedCrossAssistant"**
4. Click to select it
5. Click **"Deploy Now"**

Railway will:
- ✅ Clone your repo
- ✅ Detect Python from `runtime.txt`
- ✅ Install dependencies from `requirements.txt`
- ✅ Start the app using `Procfile`

### Step 3: Monitor Deployment
You'll see logs appear in real-time. Wait for:
```
✓ Build Complete
✓ Starting Service...
```

---

## Part 4: Get Your Live Link

### Step 1: Find Your URL
Once deployed:
1. In Railway dashboard, go to your project
2. Click on **"Deployments"** tab
3. Your live URL will be at the top like: `https://redcrossassistant-production.up.railway.app`

### Step 2: Test It's Working
Open your browser:
```
https://your-url-here/health
```
You should see:
```json
{
  "status": "ok",
  "chunks": 150
}
```

### Step 3: Test the Full Web Interface
Go to:
```
https://your-url-here/
```
You should see the Red Cross Assistant UI with the chat interface.

---

## Part 5: Testing & Validation

### Test 1: Health Check
```bash
curl https://your-url-here/health
```
Expected: `{"status":"ok","chunks":150}`

### Test 2: Chat API
```bash
curl -X POST https://your-url-here/chat \
  -H "Content-Type: application/json" \
  -d '{"query":"How do I treat a burn?"}'
```
Expected: A helpful response about burn treatment

### Test 3: Web UI
- Go to the URL in your browser
- Type a question like "What is CPR?"
- Verify you get a response
- Try different options (strict mode, debug mode)

### Test 4: Load Testing
The app has built-in caching, so responses should be instant. Try:
- Reload the page (should be fast)
- Ask similar questions (should process in <1 second)

---

## Part 6: Common Issues & Fixes

### Issue 1: "Build Failed"
**Symptom:** Deployment shows red X and build errors
**Solution:**
1. Check Railway logs for error message
2. Usually it's a missing dependency
3. Fix in `requirements.txt` and push:
   ```bash
   git add requirements.txt
   git commit -m "Fix dependencies"
   git push
   ```
4. Railway auto-redeploys on push

### Issue 2: "503 Service Unavailable"
**Symptom:** Get 503 error when accessing the app
**Solution:**
1. Wait 2-3 minutes (startup takes time with ML models)
2. Check Rails logs for startup errors
3. Verify `data/redcross.txt` exists and was pushed to repo

### Issue 3: Responses Are Slow
**Symptom:** First query takes 30+ seconds
**Solution:**
1. This is **normal** - Ollama models are being loaded
2. Subsequent requests will be fast (cached)
3. First request on app startup can take 1-2 minutes

### Issue 4: "Port Already in Use"
**Symptom:** Deployment fails with port error
**Solution:** Railway auto-assigns ports - the fix is already in `api.py`:
```python
port = int(os.environ.get("PORT", 8000))
```

---

## Part 7: Monitor & Maintain

### View Logs
1. Go to Railway dashboard
2. Click your project
3. Click **"Logs"** tab
4. See real-time activity

### Check Performance
1. Click **"Metrics"** tab
2. View CPU, memory, request counts

### Scale Up (if needed)
1. Click **"Settings"** 
2. Increase resources (within free tier limits)

### Force Redeploy
If you make code changes:
```bash
git add .
git commit -m "Update: [describe change]"
git push
```
Railway auto-redeploys within 1-2 minutes.

---

## Part 8: What's Included in Your Deployment

✅ **Backend:** FastAPI server
✅ **Frontend:** HTML/CSS/JS chat interface
✅ **AI Model:** Ollama (mistral + bge embeddings)
✅ **Database:** Vector database (in-memory cache)
✅ **Storage:** JSON file persistence
✅ **Auto-restart:** If app crashes

---

## Part 9: Share Your Link!

Your live assistant is now available at:
```
https://your-url-here
```

Share it with:
- Team members
- Stakeholders
- End users
- Anyone who needs first aid guidance!

---

## Part 10: Advanced: Environment Variables

You can set environment variables in Railway:

1. Go to project **Settings**
2. Under **Variables**, click **Add**
3. Examples you can set:
   ```
   DEBUG=false
   TOP_N=5
   STRICT_QUOTES=false
   ```

---

## Quick Reference Checklist

- [ ] Project pushed to GitHub
- [ ] `Procfile` exists and has `web: python api.py`
- [ ] `runtime.txt` exists with Python version
- [ ] `requirements.txt` has pinned versions
- [ ] Railway account created
- [ ] Project deployed on Railway
- [ ] Live URL obtained
- [ ] /health endpoint responds with 200 OK
- [ ] /chat endpoint returns responses
- [ ] Web UI loads and works
- [ ] Multiple queries tested successfully

---

## Support & Next Steps

If something doesn't work:
1. Check Railway logs for errors
2. Verify all deployment files exist locally
3. Try redeploying: `git push`
4. For Ollama issues, Railway may need more time on first startup

---

**Your app is now live! 🎉**

Visit: `https://your-railway-url.up.railway.app`
