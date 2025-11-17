# 📱 Access Your App on Phone

## ✅ Quick Setup (5 minutes)

### **Step 1: Get Your Computer's IP Address**

**On Windows:**
```bash
ipconfig
```

Look for: `IPv4 Address: 192.168.X.XXX`

**Example:** `192.168.1.5` or `192.168.100.10`

---

### **Step 2: Make Sure Phone & Computer are on Same WiFi**

Both devices must be connected to the **same WiFi network**!

---

### **Step 3: Access on Phone**

Open your phone browser and go to:

#### **Streamlit App (PWA):**
```
http://YOUR_IP:8501
```

Example: `http://192.168.1.5:8501`

**Note:** If port 8501 doesn't work, try 8502, 8503, etc. Streamlit automatically increments the port if 8501 is already in use. Check your terminal for the actual port being used (look for "You can now view your Streamlit app in your browser" message).

#### **Backend API (for testing):**
```
http://YOUR_IP:8000
```

Example: `http://192.168.1.5:8000`

---

## 🎯 Test It Works

### **1. Test Backend is Accessible**

On your phone browser, visit:
```
http://YOUR_IP:8000/health
```

You should see:
```json
{
  "status": "healthy",
  "service": "breast-health-api"
}
```

### **2. Test Agentic RAG**

Visit:
```
http://YOUR_IP:8000/docs
```

You'll see the **interactive API documentation** where you can test the agentic chatbot!

### **3. Open Streamlit App**

Visit:
```
http://YOUR_IP:8501
```

Your full Breast Friend Forever app will load! It works as a PWA on mobile.

---

## 💡 Pro Tips

### **Add to Home Screen (Make it feel like an app)**

**On iPhone:**
1. Open in Safari
2. Tap Share button
3. Tap "Add to Home Screen"
4. Now it opens like a real app!

**On Android:**
1. Open in Chrome
2. Tap menu (3 dots)
3. Tap "Add to Home screen"
4. Now it's on your home screen!

---

## 🔧 Troubleshooting

### **Can't Connect?**

1. **Check WiFi:** Both on same network?
2. **Check Firewall:** Windows Firewall might be blocking
3. **Check Servers Running:**
   - Backend: `http://localhost:8000/health`
   - Streamlit: `http://localhost:8501`

### **Firewall Fix (Windows)**

Run this in PowerShell as Administrator:
```powershell
New-NetFirewallRule -DisplayName "Python Dev Server" -Direction Inbound -Program "python.exe" -Action Allow
```

### **Still Not Working?**

**1. Wrong Port?**
Check which port Streamlit is actually using:
- Look for "You can now view your Streamlit app in your browser" in the terminal
- Try `http://YOUR_IP:8502` or `http://YOUR_IP:8503` if 8501 doesn't work

**2. Bind to all network interfaces:**

**Backend:**
```bash
cd Backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Streamlit:**
```bash
cd Web
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

**3. Check if services are accessible locally first:**
- Backend: `http://localhost:8000/health`
- Streamlit: `http://localhost:8501`

**4. Verify your IP is correct:**
```bash
ipconfig
```
Look for `IPv4 Address` under your active WiFi adapter (e.g., `192.168.100.5`)

**5. Both devices on same WiFi?**
- Phone and computer MUST be on the same WiFi network
- Some public WiFi networks block device-to-device communication

---

## 🎉 What Works on Phone

✅ **Full Streamlit App** - All pages accessible
✅ **Chat Assistant** - With Agentic RAG option
✅ **Self Exam Guide** - Visual guides
✅ **Hospital Finder** - Maps with locations
✅ **Resources** - Educational materials
✅ **Encouragement Wall** - Support messages
✅ **Works Offline** - PWA caching
✅ **Install as App** - Add to home screen

---

## 📊 Performance

- **Initial Load:** ~2-3 seconds
- **Agentic RAG Query:** ~3-5 seconds
- **Regular RAG Query:** ~1-2 seconds
- **Page Navigation:** Instant (cached)

---

## 🔒 Security Note

This setup is for **development/local network use only**.

For production:
- Use HTTPS (SSL certificate)
- Deploy to cloud service
- Add authentication
- Use environment variables for secrets

---

**Your app is now accessible on mobile!** 🎉

Just use `http://YOUR_IP:8501` and you're good to go!
