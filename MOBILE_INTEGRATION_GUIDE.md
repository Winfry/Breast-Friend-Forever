# 📱 Mobile Integration Guide - Agentic RAG in Streamlit PWA

## Overview
Your Streamlit web app works as a PWA on mobile. Here's how to add the Agentic RAG chatbot as an option!

---

## 🎯 What to Add

Add this function to your `Web/pages/2_💬_Chat_Assistant.py` file:

### **Step 1: Add API Call Function** (around line 240, after `get_rag_response`)

```python
def get_agentic_rag_response(user_message):
    """
    Get response from Agentic RAG API endpoint

    This calls your FastAPI backend's agentic chatbot endpoint
    which uses intelligent routing, verification, and multiple tools.
    """
    try:
        import requests

        # Call the agentic RAG API
        response = requests.post(
            "http://localhost:8000/api/v1/chatbot/agentic/message",
            json={
                "message": user_message,
                "conversation_id": st.session_state.get("conversation_id", "streamlit_user")
            },
            timeout=30  # Agentic RAG may take longer
        )

        if response.status_code == 200:
            data = response.json()
            return {
                "response": data["response"],
                "source": f"{data['tool_used']} (confidence: {data['confidence']:.2f})",
                "confidence": data["confidence"],
                "tool_used": data["tool_used"]
            }
        else:
            return None

    except Exception as e:
        print(f"Agentic RAG API Error: {e}")
        return None
```

---

### **Step 2: Update `get_accurate_medical_response`** (around line 241)

Modify the function to try Agentic RAG first:

```python
def get_accurate_medical_response(user_message):
    """Get medical response - tries Agentic RAG, then regular RAG, then fallback"""

    # 1. Try Agentic RAG first (most intelligent)
    if st.session_state.get("use_agentic_rag", True):
        agentic_result = get_agentic_rag_response(user_message)
        if agentic_result and agentic_result["confidence"] > 0.5:
            return agentic_result

    # 2. Try regular RAG system
    rag_result = get_rag_response(user_message)
    if rag_result:
        return rag_result

    # 3. Fallback to predefined responses
    user_lower = user_message.lower()

    if any(word in user_lower for word in ['self exam', 'check', 'examine']):
        return {
            "response": """**🔍 Step-by-Step Breast Self-Examination Guide:**

**1. Visual Inspection (Before Mirror):**
- Stand with arms at your sides - look for changes
- Raise arms overhead - check for same changes
...
""",
            "source": "Medical Guide"
        }
    # ... rest of your fallback responses
```

---

### **Step 3: Add Toggle in Sidebar** (around line 447)

Add this to your sidebar to let users choose:

```python
with st.sidebar:
    st.markdown("## ℹ️ About Our Information")

    # 🤖 NEW: Add Agentic RAG Toggle
    st.markdown("---")
    st.markdown("### 🤖 AI Assistant Mode")

    use_agentic = st.checkbox(
        "Use Agentic RAG (Intelligent AI)",
        value=True,
        help="Uses advanced AI with web search, verification, and intelligent routing"
    )
    st.session_state["use_agentic_rag"] = use_agentic

    if use_agentic:
        st.success("🤖 Using Agentic RAG - Smart routing & verification enabled")
    else:
        st.info("📚 Using Standard RAG - Fast PDF search")

    st.markdown("---")

    # Rest of your existing sidebar content...
```

---

## 🎨 Visual Indicator

Add visual feedback to show which system answered:

```python
# In your message display section (around line 360)
for message in st.session_state.chat_messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="user-message">
            {message["content"]}
            <div class="message-time">{message["timestamp"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # 🤖 NEW: Show which tool was used
        tool_badge = ""
        if "tool_used" in message:
            tool_icons = {
                "rag_search": "📚",
                "web_search": "🌐",
                "direct_answer": "💬"
            }
            icon = tool_icons.get(message["tool_used"], "🤖")
            tool_badge = f'<span style="margin-left:10px">{icon}</span>'

        source_badge = f'<div class="source-badge">📚 {message["source"]}{tool_badge}</div>' if message.get("source") else ''

        st.markdown(f"""
        <div class="bot-message">
            {message["content"]}
            <div class="message-time">{message["timestamp"]}</div>
            {source_badge}
        </div>
        """, unsafe_allow_html=True)
```

---

## 🚀 How It Works

### **User Flow:**

1. User opens your Streamlit web app (works on mobile as PWA)
2. User enables "Use Agentic RAG" in sidebar
3. User asks: "What are the latest breast cancer treatments?"
4. **Agentic RAG**:
   - Router detects "latest" keyword
   - Uses web search tool
   - Verifies answer quality
   - Returns response with sources
5. User sees answer with 🌐 icon showing it came from web search

---

## 📊 Comparison

### **Standard RAG (Current):**
```
User Question → Search PDFs → Answer
Time: ~1-2 seconds
Sources: PDF only
```

### **Agentic RAG (New):**
```
User Question → Router → Choose Tool → Verify → Answer
                    ↓
        [RAG Search | Web Search | Direct Answer]

Time: ~3-5 seconds (more thorough)
Sources: PDFs + Web + AI knowledge
Intelligence: Makes decisions at each step
```

---

## 🎯 Quick Test

After adding the code, test it:

1. Start your backend: `uvicorn app.main:app --reload --port 8000`
2. Start Streamlit: `streamlit run app.py`
3. Go to Chat Assistant page
4. Enable "Use Agentic RAG" in sidebar
5. Ask: "What's the latest breast cancer research in 2024?"
6. You should see:
   - Response with web results
   - 🌐 icon showing it used web search
   - Source showing "web_search (confidence: 0.7)"

---

## 💡 Pro Tips

### **1. Session Management**

Initialize conversation ID once per session:

```python
if "conversation_id" not in st.session_state:
    import uuid
    st.session_state.conversation_id = str(uuid.uuid4())
```

This enables conversation memory across multiple questions!

### **2. Loading Indicator**

The Agentic RAG takes a bit longer, so show progress:

```python
with st.spinner("🤖 Agentic AI is thinking... (checking PDFs, web, and verifying)"):
    ai_result = get_accurate_medical_response(user_input)
```

### **3. Fallback Gracefully**

If agentic RAG fails, automatically fall back to regular RAG:

```python
agentic_result = get_agentic_rag_response(user_message)
if agentic_result and agentic_result["confidence"] > 0.5:
    return agentic_result
else:
    # Automatically try regular RAG
    return get_rag_response(user_message)
```

---

## 🔧 Troubleshooting

### **Backend not responding?**
```bash
# Check backend is running
curl http://localhost:8000/health

# Test agentic endpoint
curl -X POST http://localhost:8000/api/v1/chatbot/agentic/message \
  -H "Content-Type: application/json" \
  -d '{"message":"test","conversation_id":"test"}'
```

### **Slow responses?**
- Normal! Agentic RAG does more work (routing, verification, etc.)
- Typical: 3-5 seconds for medical questions
- Up to 10 seconds for web search queries

### **Low confidence scores?**
- Add more PDFs to your knowledge base
- Questions outside breast cancer scope will have lower confidence
- This is good - it means the system is being honest!

---

## 🎉 Result

Your users now have access to:

✅ **Intelligent Routing** - System decides best tool
✅ **Web Search** - For recent/latest information
✅ **RAG Search** - For medical knowledge from PDFs
✅ **Direct Answers** - For general questions
✅ **Verification** - Ensures quality before responding
✅ **Conversation Memory** - Remembers context
✅ **Works on Mobile** - As PWA on phones!

---

## 📱 Mobile Experience

Your PWA will:
- Work offline (for cached data)
- Show "🤖" icon for agentic responses
- Display which tool was used (RAG/Web/Direct)
- Show confidence scores
- Provide source citations

Perfect for users who need reliable breast health information on-the-go! 🌸

---

**Made with ❤️ for Breast Friend Forever**
