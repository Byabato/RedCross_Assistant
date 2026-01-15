# 🧪 Testing Guide: Red Cross Assistant

After deploying on Railway, follow this guide to thoroughly test your live application.

---

## Quick Start Tests (3 minutes)

### 1. Health Check ✅
```bash
curl https://your-railway-url/health
```
**Expected:**
```json
{
  "status": "ok",
  "chunks": 150
}
```

### 2. Web UI Load Test
- Open `https://your-railway-url/` in browser
- Wait 2-3 seconds for page load
- Verify you see the Red Cross Assistant interface with:
  - Header: "Red Cross Assistant"
  - Chat input field
  - Settings panel with options

### 3. Simple Query Test
In the web UI:
- Type: "What is first aid?"
- Click "Send"
- Wait up to 30 seconds (first request loads ML models)
- Verify you get a response

---

## Comprehensive API Tests (Using curl/Postman)

### Test 1: Basic Chat Query
```bash
curl -X POST https://your-railway-url/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How do I treat a burn?"
  }'
```

**Expected:** Response object with answer about burns

### Test 2: Strict Quotes Mode
```bash
curl -X POST https://your-railway-url/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What should I do for a cut?",
    "strict_quotes": true
  }'
```

**Expected:** Direct quotes from Red Cross materials (no LLM interpretation)

### Test 3: Debug Mode
```bash
curl -X POST https://your-railway-url/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "CPR instructions",
    "debug": true,
    "top_n": 3
  }'
```

**Expected:** Raw chunks with similarity scores (for debugging)

### Test 4: Custom Top-N Results
```bash
curl -X POST https://your-railway-url/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Choking",
    "top_n": 10
  }'
```

**Expected:** Response using top 10 relevant chunks instead of default 5

### Test 5: Empty Query (Should Fail)
```bash
curl -X POST https://your-railway-url/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": ""
  }'
```

**Expected:** Error 400 with message "Query cannot be empty"

---

## Web UI Functional Tests

### Test 1: Chat Interface
1. Open web UI
2. Type different questions:
   - "What is the recovery position?"
   - "How do I stop bleeding?"
   - "Signs of a heart attack"
3. **Verify:** Each gets a relevant response

### Test 2: Strict Quotes Toggle
1. Ask same question twice
2. Once with "Strict Quotes" ON
3. Once with it OFF
4. **Verify:** Different response formats (quotes vs. conversational)

### Test 3: Debug Mode
1. Check "Debug" checkbox
2. Ask a question
3. **Verify:** See raw chunks with scores

### Test 4: Response Quality
- Responses should be relevant to the question
- Responses should cite Red Cross materials
- Responses should be formatted clearly

---

## Performance Tests

### Test 1: First Request Performance
1. Deploy app
2. Go to `/health` - should be instant
3. Make first `/chat` request - note time (usually 20-60 seconds as models load)
4. Make second `/chat` request - should be <2 seconds (cached)

**Expected:** Second request is significantly faster

### Test 2: Concurrent Requests
Using a tool like Apache Bench:
```bash
ab -n 10 -c 5 https://your-railway-url/health
```

**Expected:** All requests complete successfully (should be instant)

### Test 3: Large Batch Queries
Send 20 queries rapidly in the web UI.

**Expected:** No crashes, all get responses (may queue slightly)

---

## Load & Stability Tests

### Test 1: 24-Hour Uptime
- Deploy in the morning
- Check `/health` every few hours
- Leave browser tab open overnight
- Check again next morning

**Expected:** App still running, no crashes

### Test 2: Multiple Browser Tabs
- Open web UI in 5 different browser tabs
- Send queries simultaneously from each
- **Expected:** All complete without errors

### Test 3: Memory Stability
1. Go to Railway dashboard → "Metrics" tab
2. Send 50 queries over 30 minutes
3. Check memory usage in graph
4. **Expected:** Memory usage remains stable (no continuous growth = no memory leaks)

---

## Edge Cases & Error Handling

### Test 1: Very Long Query
```bash
curl -X POST https://your-railway-url/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum."
  }'
```

**Expected:** Handles gracefully, returns response (or reasonable error)

### Test 2: Special Characters
```bash
curl -X POST https://your-railway-url/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What about émojis? 🚑 & special chars: @#$%^&*()"
  }'
```

**Expected:** Handles special characters correctly

### Test 3: Off-Topic Query
```bash
curl -X POST https://your-railway-url/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the capital of France?"
  }'
```

**Expected:** Responds with "Sorry, I couldn't find relevant information..." or similar

### Test 4: Repeated Identical Queries
Send the same query 5 times.

**Expected:** 
- Same response each time
- Each response should be instant (cached)

---

## Browser Compatibility Tests

Test in different browsers:
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge
- [ ] Mobile Safari (iPhone)
- [ ] Mobile Chrome (Android)

**Expected:** Web UI works in all, responsive on mobile

---

## Logging & Diagnostics

### View Real-Time Logs
1. Go to Railway dashboard
2. Click your project
3. Click "Logs" tab
4. Send a query from web UI
5. **Verify:** See log entries for the request

### Check for Errors
Search logs for:
```
ERROR
Exception
Traceback
```

**Expected:** No error logs during normal operation

---

## Final Checklist

Before considering deployment complete:

- [ ] Health check returns 200 OK
- [ ] Web UI loads and displays correctly
- [ ] Can send chat message and get response
- [ ] Strict quotes mode works
- [ ] Debug mode shows chunks
- [ ] Different questions get different responses
- [ ] First request is slow, subsequent are fast
- [ ] No memory leaks over 24 hours
- [ ] Handles edge cases gracefully
- [ ] Works in multiple browsers
- [ ] No error logs in Railway dashboard

---

## Sample Test Questions

Use these to verify the knowledge base:

1. **"What is CPR?"** - Should describe cardiopulmonary resuscitation
2. **"How do I treat a sprain?"** - Should give RICE protocol or similar
3. **"What are signs of shock?"** - Should list shock symptoms
4. **"Choking procedure"** - Should describe Heimlich or similar
5. **"Unconscious person"** - Should describe recovery position

---

## Performance Benchmarks

For reference, your app should achieve:

- **Health check:** <100ms
- **Cached chat response:** <500ms
- **First chat response:** 20-90 seconds (model loading)
- **Web page load:** 1-2 seconds
- **Concurrent requests:** Handle 10+ simultaneous
- **Memory usage:** <500MB at idle, <800MB under load

---

## Troubleshooting During Tests

| Problem | Solution |
|---------|----------|
| 503 Service Unavailable | Wait 2-3 min for Railway startup |
| Empty response | Check logs in Railway dashboard |
| Slow first request | Normal - ML models loading |
| Page doesn't load | Check Railway deployment status |
| Connection refused | Verify Railway URL is correct |
| JSON parsing error | Check quotes and formatting in curl |

---

## Success Criteria

Your deployment is successful when:
✅ All tests pass
✅ App responds to all query types
✅ No crashes or errors in logs
✅ Performance is acceptable
✅ Team can access and use it

---

**Happy testing! 🚀**
