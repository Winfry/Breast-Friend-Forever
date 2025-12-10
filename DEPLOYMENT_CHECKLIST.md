# 🚀 Deployment Checklist - Step by Step

Follow these steps in order. Each should take 5-10 minutes.

---

## ✅ Step 1: Integrate `backend_helper.py` (5 minutes)

### What This Does:
Makes your app handle backend sleep gracefully with friendly messages.

### Instructions:

**1.1 Update Chat Assistant to use the helper:**

Open `Web/pages/2_💬_Chat_Assistant.py` and add at the top:
```python
from utils.backend_helper import call_backend_feature
```

Find where you call the backend (around line 310-320), replace:
```python
# OLD CODE
agentic_result = get_agentic_rag_response(user_message)
```

With:
```python
# NEW CODE
agentic_result = call_backend_feature(
    "AI Chat Assistant",
    get_agentic_rag_response,
    user_message
)
```

**1.2 Update Symptom Checker:**

Open `Web/pages/1_🔍_Symptom_Checker.py`, add at top:
```python
from utils.backend_helper import call_backend_feature
```

Find the API call (around line 80-90), wrap it:
```python
# NEW CODE
result = call_backend_feature(
    "Symptom Checker",
    api_client.analyze_symptoms,
    symptom_data
)
```

**1.3 Test locally:**
```bash
# Stop your backend (Ctrl+C)
# Try using the app - you should see friendly "waking up" messages
```

---

## ✅ Step 2: Deploy Backend to Render (10 minutes)

### 2.1 Create Render Account
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (easiest)

### 2.2 Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub account
3. Select your `Breast-Friend-Forever` repository
4. Click "Connect"

### 2.3 Configure Service
Fill in these settings:

| Field | Value |
|-------|-------|
| **Name** | `bff-backend` |
| **Region** | Choose closest to you |
| **Branch** | `main` |
| **Root Directory** | `Backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free` |

### 2.4 Add Environment Variables (IMPORTANT!)
Click "Advanced" → "Add Environment Variable":

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.10.0` |
| `OLLAMA_HOST` | `http://localhost:11434` (or leave blank for now) |

### 2.5 Deploy!
1. Click "Create Web Service"
2. Wait 5-10 minutes for first deploy
3. You'll see logs - wait for "Application startup complete"
4. Copy your URL: `https://bff-backend-xxxx.onrender.com`

### 2.6 Test Backend
Visit: `https://bff-backend-xxxx.onrender.com/health`

You should see:
```json
{"status": "healthy", "service": "breast-health-api"}
```

✅ **Backend is live!**

---

## ✅ Step 3: Deploy Frontend to Streamlit Cloud (10 minutes)

### 3.1 Create Streamlit Account
1. Go to https://share.streamlit.io
2. Click "Sign up" → Use GitHub

### 3.2 Create New App
1. Click "New app"
2. Select your repository: `Breast-Friend-Forever`
3. **Main file path**: `Web/app.py`
4. **Branch**: `main`

### 3.3 Advanced Settings
Click "Advanced settings" → Add environment variables:

| Key | Value |
|-----|-------|
| `BACKEND_HOST` | `https://bff-backend-xxxx.onrender.com` (YOUR Render URL) |

### 3.4 Deploy!
1. Click "Deploy!"
2. Wait 3-5 minutes
3. Your app URL: `https://breast-friend-forever.streamlit.app`

### 3.5 Test Frontend
1. Visit your Streamlit URL
2. Try the AI Chat - first message may take 30s (backend waking up)
3. Subsequent messages should be fast!

✅ **Frontend is live!**

---

## ✅ Step 4: Set Up UptimeRobot (5 minutes)

### What This Does:
Pings your backend every 5 minutes to keep it awake (reduces cold starts).

### 4.1 Create Account
1. Go to https://uptimerobot.com
2. Sign up (free account)

### 4.2 Add Monitor
1. Click "Add New Monitor"
2. Fill in:

| Field | Value |
|-------|-------|
| **Monitor Type** | `HTTP(s)` |
| **Friendly Name** | `BFF Backend Health Check` |
| **URL** | `https://bff-backend-xxxx.onrender.com/health` (YOUR URL) |
| **Monitoring Interval** | `5 minutes` |

3. Click "Create Monitor"

### 4.3 Verify
- You should see "Up" status within 1 minute
- UptimeRobot will now ping every 5 minutes
- This keeps your backend awake during active hours

✅ **Auto-wake is set up!**

---

## ✅ Step 5: Test with Friends (5 minutes)

### 5.1 Share Your Link
Send to 3-5 friends:
```
Hey! Check out my new health app: 
https://breast-friend-forever.streamlit.app

Try the AI Chat and Symptom Checker!
```

### 5.2 What to Tell Them
"If it's the first time in a while, the AI might take 30 seconds to wake up. After that, it's instant!"

### 5.3 Monitor Usage
- Check Render dashboard for traffic
- Check Streamlit analytics for page views
- Watch for any errors in logs

---

## 🎉 You're Live!

Your app is now accessible from:
- ✅ Any phone
- ✅ Any laptop
- ✅ Anywhere in the world

**Your URLs:**
- Frontend: `https://breast-friend-forever.streamlit.app`
- Backend: `https://bff-backend-xxxx.onrender.com`

---

## 🔧 Troubleshooting

### "Backend Connection Failed"
1. Check Render logs - is backend running?
2. Verify `BACKEND_HOST` in Streamlit settings
3. Test backend directly: `https://your-backend.onrender.com/health`

### "App is slow"
- First request after 15 min idle = 30s (normal for free tier)
- Subsequent requests = fast
- UptimeRobot reduces this by keeping backend awake

### "AI Chat doesn't work"
- Ollama won't work on Render free tier (needs GPU)
- Options:
  1. Disable AI features for now
  2. Use OpenAI API instead (requires API key)
  3. Deploy Ollama separately (advanced)

---

## 📊 Free Tier Limits

**Render Free:**
- 750 hours/month (enough for 24/7 with UptimeRobot)
- 512MB RAM
- Sleeps after 15 min idle

**Streamlit Cloud Free:**
- Unlimited apps
- 1GB RAM per app
- Community support

**UptimeRobot Free:**
- 50 monitors
- 5-minute intervals
- Email alerts

---

## 💰 When to Upgrade?

Upgrade to paid ($7/month) when:
- ✅ You have 50+ daily users
- ✅ Cold starts annoy users
- ✅ You want professional reliability

Until then, free tier works great! 🎉

---

## 🆘 Need Help?

If you get stuck:
1. Check Render logs (click "Logs" tab)
2. Check Streamlit logs (click "Manage app" → "Logs")
3. Test backend health endpoint
4. Ask me for help!

**Next Step:** Share your live app link in your Medium article! 🚀
