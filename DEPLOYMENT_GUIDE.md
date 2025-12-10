# Deployment Guide: Getting Public URLs

## 🎯 Goal
Make your app accessible from **any device** (phone, laptop, tablet) via public URLs instead of localhost.

---

## 📱 Quick Answer: What URLs Will You Get?

After deployment, you'll have:
- **Frontend (Streamlit)**: `https://breast-friend-forever.streamlit.app`
- **Backend (FastAPI)**: `https://bff-backend.onrender.com` (or similar)

Users can access these from ANY device with internet!

---

## 🚀 Deployment Options

### **Option 1: Frontend Only (Quickest - 5 minutes)**
Deploy just the Streamlit app. Features that don't need the backend (Self-Exam Guide, Resources) will work. AI features won't work.

**Steps:**
1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Connect your GitHub repo
3. **Main file path**: `Web/app.py`
4. Deploy!

**Result:** `https://your-app.streamlit.app`

---

### **Option 2: Full Stack (Frontend + Backend) - Recommended**

Deploy both parts so ALL features work.

#### **Step 1: Deploy Backend (FastAPI)**

**Using Render.com (Free Tier):**

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. **Settings:**
   - **Name**: `bff-backend`
   - **Root Directory**: `Backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3.10+
5. **Environment Variables** (Add these):
   ```
   OLLAMA_HOST=http://localhost:11434  # Or your Ollama server URL
   ```
6. Click "Create Web Service"

**Result:** `https://bff-backend.onrender.com`

**⚠️ Important:** Free tier sleeps after 15 min of inactivity. First request may take 30s to wake up.

---

#### **Step 2: Deploy Frontend (Streamlit)**

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Connect your GitHub repo
3. **Settings:**
   - **Main file path**: `Web/app.py`
   - **Python version**: 3.10+
4. **Advanced Settings** → **Environment Variables**:
   ```
   BACKEND_HOST=bff-backend.onrender.com
   ```
5. Deploy!

**Result:** `https://breast-friend-forever.streamlit.app`

---

## 🔧 Configuration Changes Needed

### 1. Update `api_client.py` to use environment variable:

```python
import os

class ApiClient:
    def __init__(self):
        # Use environment variable if available, otherwise localhost
        backend_host = os.getenv("BACKEND_HOST", "localhost")
        backend_port = os.getenv("BACKEND_PORT", "8000")
        
        # If BACKEND_HOST is a full URL (e.g., from Render), use it directly
        if backend_host.startswith("http"):
            self.backend_url = backend_host
        else:
            self.backend_url = f"http://{backend_host}:{backend_port}"
```

### 2. Update Backend CORS settings in `Backend/app/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",  # Local development
        "https://*.streamlit.app",  # Streamlit Cloud
        "https://breast-friend-forever.streamlit.app",  # Your specific app
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📱 Testing on Your Phone (Local Network - Quick Test)

Want to test RIGHT NOW before deploying? Here's how:

### **Step 1: Find Your Computer's IP**
```bash
# Windows
ipconfig
# Look for "IPv4 Address" (e.g., 192.168.1.100)

# Mac/Linux
ifconfig
# Look for "inet" under your WiFi adapter
```

### **Step 2: Run with Network Access**
```bash
# Backend (Terminal 1)
cd Backend
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Frontend (Terminal 2)
cd Web
streamlit run app.py --server.address 0.0.0.0
```

### **Step 3: Access from Phone**
Make sure your phone is on the **same WiFi** as your computer, then visit:
- **Frontend**: `http://192.168.1.100:8501` (replace with YOUR IP)
- **Backend**: `http://192.168.1.100:8000`

**⚠️ Limitation:** Only works on your local WiFi. Won't work from outside your home.

---

## ❌ Backend Connection Error - FIXED!

**What it was:** The app showed "❌ Backend Connection Failed" on the home screen.

**Why it appeared:** The frontend couldn't reach the backend (either not running or wrong URL).

**What I did:** Removed the visible error message. Now:
- ✅ Connection check happens silently in the background
- ✅ Users don't see scary error messages
- ✅ Individual features show friendly messages if backend is unavailable

**Example:** If backend is down, the AI Chat will say:
> "I'm currently offline. Please try again later or check out our Self-Exam Guide in the meantime! 🌸"

Instead of a big red error on the home page.

---

## 🎯 Recommended Deployment Path

1. **Test locally on phone** (5 min) - Use the local network method above
2. **Deploy backend to Render** (10 min) - Get a public backend URL
3. **Deploy frontend to Streamlit Cloud** (5 min) - Connect to backend
4. **Test from any device** - Share the Streamlit URL with friends!

---

## 🆘 Troubleshooting

### "Backend Connection Failed" (even after deployment)
- Check `BACKEND_HOST` environment variable in Streamlit Cloud
- Verify backend is running on Render (check logs)
- Test backend directly: `https://your-backend.onrender.com/health`

### "App is slow on first load"
- Render free tier sleeps after 15 min. First request wakes it up (30s delay)
- Upgrade to paid tier ($7/month) for always-on backend

### "AI features don't work"
- Ollama needs to run somewhere. Options:
  1. Deploy Ollama on a separate server (DigitalOcean, AWS)
  2. Use OpenAI API instead (requires API key)
  3. Disable AI features for now (app still works without them)

---

## 💡 Next Steps

1. Deploy backend to Render
2. Deploy frontend to Streamlit Cloud
3. Share your public URL: `https://breast-friend-forever.streamlit.app`
4. Update your Medium article with the live demo link!

**Questions?** Let me know which deployment option you want to pursue!
