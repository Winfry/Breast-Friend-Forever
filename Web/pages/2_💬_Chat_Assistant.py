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

# Cached RAG system initialization - only runs once per session!
@st.cache_resource(show_spinner="🌸 Loading medical knowledge base...")
def initialize_rag_system():
    """Initialize RAG system once and cache it - prevents reloading PDFs on every page refresh"""
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
                return get_rag_system(), True
    except Exception:
        pass
    return None, False

# Initialize RAG system (cached - only loads PDFs once!)
rag_system, RAG_AVAILABLE = initialize_rag_system()

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

st.set_page_config(page_title="Chat Assistant", page_icon="💬", layout="wide")

# 🎨 PERFECTED CHATGPT-STYLE CSS
st.markdown("""
    <style>
    /* Main chat container - FIXED SPACING */
    .main-chat-container {
        padding: 0.5rem;
        margin-bottom: 100px;
        max-height: 65vh;
        overflow-y: auto;
        scroll-behavior: smooth;
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
    
    /* Input area styling - ALWAYS VISIBLE */
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
        padding: 0.8rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border: 2px solid #FFE4EC;
    }
    
    /* Button styling */
    .stButton button {
        width: 100%;
        border-radius: 10px;
        border: 2px solid #FF69B4;
        background: white;
        color: #FF69B4;
        font-weight: 500;
        transition: all 0.3s ease;
        padding: 0.5rem;
        font-size: 0.9rem;
    }
    
    .stButton button:hover {
        background: #FF69B4;
        color: white;
        transform: translateY(-1px);
    }
    
    /* Text area styling */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #FFB6C1;
        padding: 0.8rem;
        font-size: 0.9rem;
    }
    
    /* Send button styling */
    .send-button {
        background: linear-gradient(135deg, #FF69B4, #EC4899) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        height: 100% !important;
    }
    
    /* Hide ALL streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Reduce spacing in main area */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Auto-scroll to bottom */
    .auto-scroll {
        scroll-behavior: smooth;
    }
    
    /* Compact title area */
    .main-title {
        margin-bottom: 0.5rem !important;
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

def add_message(role, content, source=None, tool_used=None, confidence=None):
    """Add message to chat with timestamp and optional metadata"""
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M")
    }
    if source and source != "Welcome":
        message["source"] = source
    if tool_used:
        message["tool_used"] = tool_used
    if confidence is not None:
        message["confidence"] = confidence
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
    setTimeout(scrollToBottom, 150);
    </script>
    """, unsafe_allow_html=True)

def get_rag_response(user_message):
    """Get response from RAG system - completely silent to user"""
    if not RAG_AVAILABLE or rag_system is None:
        return None

    try:
        relevant_chunks = rag_system.search(user_message, top_k=5)
        if relevant_chunks:
            response = rag_system.get_answer(user_message, relevant_chunks)
            return {
                "response": response,
                "source": "Trusted Medical Sources",
            }
    except Exception:
        pass

    return None

def get_agentic_rag_response(user_message):
    """
    Get response from Agentic RAG API endpoint

    🤖 This uses the intelligent agentic system that:
    - Routes to best tool (RAG search, web search, or direct answer)
    - Verifies answer quality before responding
    - Provides source citations and confidence scores
    """
    try:
        # Generate or get conversation ID
        if "conversation_id" not in st.session_state:
            import uuid
            st.session_state.conversation_id = str(uuid.uuid4())

        # Determine backend URL (works on both computer and phone)
        # Try environment variable first, then default to localhost
        import os
        backend_host = os.getenv("BACKEND_HOST", "localhost")
        backend_url = f"http://{backend_host}:8000/api/v1/chatbot/agentic/message"

        # Call the agentic RAG API
        response = requests.post(
            backend_url,
            json={
                "message": user_message,
                "conversation_id": st.session_state.conversation_id
            },
            timeout=60  # Agentic RAG may take longer, increased to 60s
        )

        if response.status_code == 200:
            data = response.json()

            # Map tool icons
            tool_icons = {
                "rag_search": "📚",
                "web_search": "🌐",
                "direct_answer": "💬"
            }
            icon = tool_icons.get(data.get("tool_used", ""), "🤖")

            return {
                "response": data["response"],
                "source": f"Agentic AI {icon} (confidence: {data['confidence']:.2f})",
                "confidence": data["confidence"],
                "tool_used": data.get("tool_used", "unknown")
            }
        else:
            return None

    except Exception as e:
        print(f"❌ Agentic RAG API Error: {e}")
        print(f"   Backend URL attempted: {backend_url if 'backend_url' in locals() else 'unknown'}")
        import traceback
        traceback.print_exc()
        return None

def get_accurate_medical_response(user_message):
    """Get medical response - tries Agentic RAG first, then regular RAG, then fallback"""

    # 1. Try Agentic RAG first (if enabled)
    if st.session_state.get("use_agentic_rag", True):
        agentic_result = get_agentic_rag_response(user_message)
        if agentic_result and agentic_result.get("confidence", 0) > 0.4:
            return agentic_result

    # 2. Try regular RAG system
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
    
    elif any(word in user_lower for word in ['risk factor', 'what increases risk', 'main risk']):
        return {
            "response": """**📊 Breast Cancer Risk Factors:**

**🔴 Non-Modifiable Risk Factors:**
• **Gender & Age:** Women over 55 are at higher risk
• **Family History:** Especially first-degree relatives
• **Genetics:** BRCA1/BRCA2 mutations
• **Personal History:** Previous breast cancer
• **Race/Ethnicity:** Different risks across populations

**🟡 Modifiable Risk Factors:**
• **Weight:** Obesity increases risk
• **Alcohol:** Each drink increases risk
• **Physical Activity:** Inactivity raises risk
• **Hormone Therapy:** Long-term use increases risk
• **Reproductive History:** Childbearing and breastfeeding patterns

**🌍 For African Women:**
• Know your family history
• Discuss personalized risk with your doctor
• Be aware of screening guidelines for your risk level""",
            "source": "Risk Factors Guide"
        }
    
    else:
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

# 🎯 COMPACT TITLE AREA
st.markdown('<div class="main-title">', unsafe_allow_html=True)
st.title("💬 Breast Health Assistant")
st.markdown("**Your caring companion for breast health information**")
st.markdown('</div>', unsafe_allow_html=True)

# Main chat area - SCROLLABLE CONTAINER
st.markdown('<div class="main-chat-container auto-scroll">', unsafe_allow_html=True)

# Display chat messages
import html
for message in st.session_state.chat_messages:
    # Escape HTML in content to prevent injection and rendering issues
    safe_content = html.escape(str(message["content"]))

    if message["role"] == "user":
        st.markdown(f"""
        <div class="user-message">
            {safe_content}
            <div class="message-time">{message["timestamp"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Add tool-specific icon if available
        tool_icon = ""
        if "tool_used" in message:
            tool_icons = {
                "rag_search": "📚",
                "web_search": "🌐",
                "direct_answer": "💬",
                "error": "⚠️"
            }
            tool_icon = tool_icons.get(message.get("tool_used"), "🤖")

        source_badge = f'<div class="source-badge">{tool_icon} {message["source"]}</div>' if message.get("source") else ''
        st.markdown(f"""
        <div class="bot-message">
            {safe_content}
            <div class="message-time">{message["timestamp"]}</div>
            {source_badge}
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Fixed input area at the bottom - ALWAYS VISIBLE
st.markdown('<div class="input-container">', unsafe_allow_html=True)

# Quick Questions Section
st.markdown("#### 💡 Quick Questions")
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
            # Set flag
            st.session_state.suggestion_clicked = True
            
            # Add user message immediately
            add_message("user", suggestion)
            
            # Get AI response
            with st.spinner("🌸 Finding information for you..."):
                ai_result = get_accurate_medical_response(suggestion)

            # Add assistant message with tool metadata
            add_message(
                "assistant",
                ai_result["response"],
                ai_result.get("source"),
                ai_result.get("tool_used"),
                ai_result.get("confidence")
            )

            st.rerun()

# Message input area - ALWAYS VISIBLE NOW
st.markdown("#### 💭 Your Question")
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_area(
        "Type your question here...",
        value=st.session_state.user_input,
        placeholder="Ask about breast self-exams, symptoms, prevention, screening...",
        label_visibility="collapsed",
        height=70,
        key="user_input_widget"
    )

with col2:
    send_button = st.button("🚀 **Send**", use_container_width=True, key="send_button")

if send_button:
    if st.session_state.user_input_widget.strip():
        user_input = st.session_state.user_input_widget
        
        # Add user message
        add_message("user", user_input)
        
        # Get AI response
        with st.spinner("🌸 Finding information for you..."):
            ai_result = get_accurate_medical_response(user_input)

        # Add assistant message with tool metadata
        add_message(
            "assistant",
            ai_result["response"],
            ai_result.get("source"),
            ai_result.get("tool_used"),
            ai_result.get("confidence")
        )
        
        # Clear input
        st.session_state.user_input = ""
        st.rerun()

# Reset suggestion flag
if st.session_state.get('suggestion_clicked', False):
    st.session_state.suggestion_clicked = False

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

    # 🤖 Agentic RAG Toggle
    st.markdown("### 🤖 AI Assistant Mode")

    use_agentic = st.checkbox(
        "Use Agentic RAG (Intelligent AI)",
        value=True,
        help="Uses advanced AI with intelligent routing, web search, verification, and multi-step reasoning"
    )
    st.session_state["use_agentic_rag"] = use_agentic

    if use_agentic:
        st.success("🤖 **Agentic RAG Enabled**\n- Smart routing & tool selection\n- Web search for latest info\n- Answer verification")
    else:
        st.info("📚 **Standard RAG Mode**\n- Fast PDF knowledge base search")

    st.markdown("---")
    
    if st.button("🔄 Start New Conversation", use_container_width=True):
        st.session_state.chat_messages = []
        st.session_state.user_input = ""
        st.session_state.suggestion_clicked = False
        st.rerun()

# Auto-scroll JavaScript
st.markdown("""
<script>
function scrollToBottom() {
    const container = document.querySelector('.main-chat-container');
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
}
setTimeout(scrollToBottom, 100);
setTimeout(scrollToBottom, 400);
</script>
""", unsafe_allow_html=True)

# 🎨 CLEAN CSS - NO VISIBLE TIME TAGS
st.markdown("""
    <style>
    /* Your existing CSS stays here - DON'T TOUCH */
    .chat-container {
        max-height: 60vh;
        overflow-y: auto;
        padding: 2rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 25px;
        margin: 2rem 0;
        border: 3px solid #FFF0F5;
    }
    
    /* ... ALL YOUR EXISTING CSS ... */
    
    </style>
    
    <!-- 🔽 ADD THIS PWA CODE RIGHT AFTER THE CSS 🔽 -->
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#FF69B4">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
    <script>
    // PWA Installation Handler
    let deferredPrompt;
    const installButton = document.createElement('button');
    
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      deferredPrompt = e;
      
      // Create install button
      installButton.innerHTML = '📱 Install App';
      installButton.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(135deg, #FF69B4, #EC4899);
        color: white;
        border: none;
        padding: 12px 18px;
        border-radius: 25px;
        font-weight: bold;
        font-size: 14px;
        z-index: 1000;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(255, 105, 180, 0.3);
      `;
      
      installButton.onclick = async () => {
        if (!deferredPrompt) return;
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        if (outcome === 'accepted') {
          installButton.style.display = 'none';
        }
        deferredPrompt = null;
      };
      
      document.body.appendChild(installButton);
    });
    
    window.addEventListener('appinstalled', () => {
      installButton.style.display = 'none';
    });
    </script>
    """, unsafe_allow_html=True)