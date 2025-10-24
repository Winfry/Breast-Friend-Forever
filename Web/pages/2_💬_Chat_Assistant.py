import streamlit as st
import time
import requests
import json
import random
from datetime import datetime
import sys
import os

# Add the backend to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'Backend', 'app'))

# Silently try to load RAG system
RAG_AVAILABLE = False
rag_system = None

try:
    backend_app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Backend', 'app'))
    rag_file = os.path.join(backend_app_path, 'rag_system.py')
    if os.path.exists(rag_file):
        import importlib.util
        spec = importlib.util.spec_from_file_location("rag_system", rag_file)
        rag_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(rag_module)
        get_rag_system = getattr(rag_module, "get_rag_system", None)
        if callable(get_rag_system):
            rag_system = get_rag_system()
            RAG_AVAILABLE = True
            print("✅ RAG system loaded in chat assistant")
except Exception as e:
    print(f"❌ RAG system loading failed: {e}")
    pass

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

st.set_page_config(page_title="Chat Assistant", page_icon="💬", layout="wide")

# 🎨 CHATGPT-STYLE CSS WITH AUTO-SCROLL
st.markdown("""
    <style>
    /* Main chat container with auto-scroll */
    .main-chat-container {
        padding: 1rem;
        margin-bottom: 120px;
        height: 65vh;
        overflow-y: auto;
        scroll-behavior: smooth;
    }
    
    /* Ensure new messages appear at bottom */
    .main-chat-container > div {
        display: flex;
        flex-direction: column;
    }
    
    /* User message styling */
    .user-message {
        background: linear-gradient(135deg, #FF69B4, #EC4899);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 18px 18px 4px 18px;
        margin-left: auto;
        max-width: 80%;
        box-shadow: 0 4px 15px rgba(255, 105, 180, 0.3);
        margin-bottom: 1rem;
        position: relative;
        border: 2px solid #FF1493;
    }
    
    /* Bot message styling */
    .bot-message {
        background: linear-gradient(135deg, #FFF0F5, #FFE4EC);
        color: #333;
        padding: 1rem 1.5rem;
        border-radius: 18px 18px 18px 4px;
        margin-right: auto;
        max-width: 80%;
        box-shadow: 0 4px 15px rgba(255, 105, 180, 0.15);
        border: 2px solid #FFB6C1;
        margin-bottom: 1rem;
        position: relative;
    }
    
    /* Message time */
    .message-time {
        font-size: 0.7rem;
        opacity: 0.6;
        margin-top: 0.5rem;
        text-align: right;
    }
    
    /* Source badge */
    .source-badge {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.65rem;
        margin-top: 0.5rem;
        display: inline-block;
    }
    
    /* Input area styling */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 1rem;
        border-top: 2px solid #FFE4EC;
        box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.1);
        z-index: 1000;
    }
    
    /* Quick questions styling */
    .quick-questions {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 2px solid #FFE4EC;
    }
    
    /* Hide streamlit elements */
    .stButton button {
        width: 100%;
        border-radius: 12px;
        border: 2px solid #FF69B4;
        background: white;
        color: #FF69B4;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background: #FF69B4;
        color: white;
        transform: translateY(-2px);
    }
    
    /* Text area styling */
    .stTextArea textarea {
        border-radius: 15px;
        border: 2px solid #FFB6C1;
        padding: 1rem;
    }
    
    /* Send button styling */
    .send-button {
        background: linear-gradient(135deg, #FF69B4, #EC4899) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
    }
    
    .send-button:hover {
        background: linear-gradient(135deg, #EC4899, #FF1493) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Auto-scroll to bottom */
    .auto-scroll {
        scroll-behavior: smooth;
    }
    </style>
    """, unsafe_allow_html=True)

# 🚀 SESSION STATE
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "suggestion_clicked" not in st.session_state:
    st.session_state.suggestion_clicked = False

# Welcome message
if not st.session_state.chat_messages:
    st.session_state.chat_messages.append({
        "role": "assistant", 
        "content": "Hello! 🌸 I'm your Breast Friend Forever companion. I'm here to provide caring, accurate information about breast health in a safe, supportive space. What would you like to know today? 💖",
        "timestamp": datetime.now().strftime("%H:%M")
    })

def add_message(role, content, source=None):
    """Add message to chat with timestamp"""
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M")
    }
    if source and source != "Welcome":
        message["source"] = source
    st.session_state.chat_messages.append(message)
    
    # Auto-scroll to bottom after adding message
    st.markdown("""
    <script>
    function scrollToBottom() {
        const container = document.querySelector('.main-chat-container');
        if (container) {
            container.scrollTop = container.scrollHeight;
        }
    }
    // Wait a bit for the message to render then scroll
    setTimeout(scrollToBottom, 100);
    </script>
    """, unsafe_allow_html=True)

def get_rag_response(user_message):
    """Get response from RAG system with proper error handling"""
    if not RAG_AVAILABLE or rag_system is None:
        return None
    
    try:
        relevant_chunks = rag_system.search(user_message, top_k=5)
        if relevant_chunks:
            response = rag_system.get_answer(user_message, relevant_chunks)
            return {
                "response": response,
                "source": "Medical Resources",
                "response_time": 0.5,
                "speed": "searching"
            }
    except Exception as e:
        print(f"RAG search error: {e}")
    
    return None

def get_accurate_medical_response(user_message):
    """🚀 IMPROVED: Use RAG first, then fallback to predefined responses"""
    
    # Try RAG system first
    rag_result = get_rag_response(user_message)
    if rag_result:
        return rag_result
    
    user_lower = user_message.lower()
    
    # Fallback to predefined responses only if RAG fails
    if any(word in user_lower for word in ['self exam', 'check', 'examine', 'how to check', 'self-exam']):
        return {
            "response": """**🔍 Step-by-Step Breast Self-Examination Guide:**

**1. Visual Inspection (Before Mirror):**
- Stand with arms at your sides - look for changes in size, shape, contour
- Raise arms overhead - check for same changes
- Look for: skin dimpling, redness, rash, nipple changes, swelling

**2. Manual Examination (Lying Down):**
- Lie down with pillow under right shoulder, right arm behind head
- Use left hand fingers (finger pads) to feel right breast
- Use small circular motions - cover entire breast area
- Apply light, medium, and firm pressure
- Repeat on left side

**3. Manual Examination (Standing/Shower):**
- Repeat same process while standing
- Many women find wet, soapy skin makes examination easier

**📅 When to Examine:** Monthly, 3-5 days after your period ends
**🎯 What to Look For:** New lumps, thickening, swelling, dimpling, pain, nipple changes, discharge

**💡 Important:** This complements but doesn't replace clinical exams!""",
            "source": "Medical Guide"
        }
    
    elif any(word in user_lower for word in ['reduce risk', 'prevent', 'prevention', 'lower risk', 'how to reduce']):
        return {
            "response": """**🛡️ Evidence-Based Breast Cancer Risk Reduction:**

**✅ Proven Prevention Strategies:**
• **Maintain Healthy Weight:** Obesity increases postmenopausal breast cancer risk
• **Regular Exercise:** 150+ minutes of moderate activity weekly reduces risk
• **Limit Alcohol:** Each daily drink increases risk - limit to 1 drink/day or less
• **Avoid Smoking:** Smoking linked to increased breast cancer risk
• **Breastfeed If Possible:** Reduces breast cancer risk
• **Healthy Diet:** Rich in fruits, vegetables, whole grains, and lean proteins
• **Limit Hormone Therapy:** Discuss risks/benefits with your doctor

**🌍 For African Women:**
• Know your family history and share it with your doctor
• Advocate for appropriate screening based on individual risk
• Be aware of potentially more aggressive subtypes
• Participate in community awareness programs

**📊 Lifestyle Impact:** Healthy lifestyle can significantly reduce overall breast cancer risk""",
            "source": "Prevention Guidelines"
        }
    
    else:
        # Final fallback
        return {
            "response": """I specialize in providing specific, evidence-based information about breast health. Here are topics I can help with:

• **Self-examination techniques** - Step-by-step guides
• **Early detection signs** - What symptoms to watch for  
• **Risk reduction strategies** - Evidence-based prevention methods
• **Screening guidelines** - When and how often to get checked
• **Risk factors** - Understanding your personal risk profile

What specific aspect would you like me to explain in detail?""",
            "source": "Breast Health Guide"
        }

# 🎯 CHATGPT-STYLE LAYOUT
st.title("💬 Breast Health Assistant")
st.markdown("*Your caring companion for breast health information*")

# Main chat area - SCROLLABLE CONTAINER
st.markdown('<div class="main-chat-container auto-scroll">', unsafe_allow_html=True)

# Display chat messages in reverse order (newest at bottom)
for message in st.session_state.chat_messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="user-message">
            {message["content"]}
            <div class="message-time">{message["timestamp"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        source_badge = f'<div class="source-badge">📚 {message["source"]}</div>' if message.get("source") else ''
        st.markdown(f"""
        <div class="bot-message">
            {message["content"]}
            <div class="message-time">{message["timestamp"]}</div>
            {source_badge}
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Fixed input area at the bottom (like ChatGPT)
st.markdown('<div class="input-container">', unsafe_allow_html=True)

# Quick Questions Section
st.markdown("### 💡 Quick Questions")
cols = st.columns(3)
suggestions = [
    "How do I perform a breast self-exam?",
    "What are early signs of breast cancer?", 
    "How can I reduce my breast cancer risk?",
    "When should I start mammograms?",
    "What are the main risk factors?",
    "How often should I do self-exams?"
]

# Handle suggestion clicks
for i, suggestion in enumerate(suggestions):
    with cols[i % 3]:
        if st.button(suggestion, key=f"sugg_{i}"):
            # Set flag and clear any previous input
            st.session_state.suggestion_clicked = True
            st.session_state.user_input = ""
            
            # Add user message immediately
            add_message("user", suggestion)
            
            # Get AI response
            with st.spinner("🔍 Finding the best medical information..."):
                ai_result = get_accurate_medical_response(suggestion)
            
            # Add assistant message  
            add_message("assistant", ai_result["response"], ai_result.get("source"))
            
            st.rerun()

# Only show input area if no suggestion was just clicked
if not st.session_state.get('suggestion_clicked', False):
    # Message input area
    st.markdown("### 💭 Your Question")
    col1, col2 = st.columns([4, 1])

    with col1:
        user_input = st.text_area(
            "Type your question here...",
            value=st.session_state.user_input,
            placeholder="Ask about breast self-exams, symptoms, prevention, screening...",
            label_visibility="collapsed",
            height=80,
            key="user_input_widget"
        )

    with col2:
        # Changed send icon to 🚀
        send_button = st.button("🚀 **Send**", use_container_width=True, key="send_button")

    if send_button:
        if st.session_state.user_input_widget.strip():
            user_input = st.session_state.user_input_widget
            
            # Add user message
            add_message("user", user_input)
            
            # Get AI response
            with st.spinner("🔍 Finding the best medical information..."):
                ai_result = get_accurate_medical_response(user_input)
            
            # Add assistant message  
            add_message("assistant", ai_result["response"], ai_result.get("source"))
            
            # Clear input
            st.session_state.user_input = ""
            st.rerun()

# Reset suggestion flag after processing
if st.session_state.get('suggestion_clicked', False):
    st.session_state.suggestion_clicked = False
    # Small delay to ensure the UI updates
    time.sleep(0.1)

st.markdown('</div>', unsafe_allow_html=True)

# Sidebar for additional information
with st.sidebar:
    st.markdown("## ℹ️ About Our Information")
    st.markdown("""
    **Trusted Medical Sources:**
    
    Our responses are based on verified medical information from:
    - Kenya Ministry of Health guidelines
    - World Health Organization recommendations  
    - Cancer research foundations
    - Medical institution publications
    
    *Note: This information is for educational purposes. Always consult healthcare professionals for medical advice and diagnosis.*
    """)
    
    st.markdown("---")
    
    if st.button("🔄 Start New Conversation", use_container_width=True):
        st.session_state.chat_messages = []
        st.session_state.user_input = ""
        st.session_state.suggestion_clicked = False
        st.rerun()
    
    # Display RAG status (for debugging, can be removed)
    if RAG_AVAILABLE:
        st.success("✅ Medical database loaded")
    else:
        st.info("🔍 Using general medical knowledge")

# Add some space at the bottom to account for fixed input
st.markdown("<br><br><br>", unsafe_allow_html=True)

# Auto-scroll JavaScript (runs on every render)
st.markdown("""
<script>
function scrollToBottom() {
    const container = document.querySelector('.main-chat-container');
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
}
// Scroll on page load and after short delay
setTimeout(scrollToBottom, 100);
setTimeout(scrollToBottom, 500);
</script>
""", unsafe_allow_html=True)