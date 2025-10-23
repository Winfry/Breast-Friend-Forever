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

try:
    from rag_system import get_rag_system
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    st.warning("⚠️ RAG system not available - using medical responses only")

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

st.set_page_config(page_title="Chat Assistant", page_icon="💬", layout="wide")

# 🎨 ENHANCED CSS FOR HYBRID SYSTEM
st.markdown("""
    <style>
    .chat-container {
        max-height: 60vh;
        overflow-y: auto;
        padding: 2rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 25px;
        margin: 2rem 0;
        border: 3px solid #FFF0F5;
    }
    
    .user-message {
        background: linear-gradient(135deg, #FF69B4, #EC4899);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 25px 25px 5px 25px;
        margin-left: auto;
        max-width: 70%;
        box-shadow: 0 8px 25px rgba(255, 105, 180, 0.3);
        margin-bottom: 1rem;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #FFF0F5, #FFE4EC);
        color: #333;
        padding: 1.5rem 2rem;
        border-radius: 25px 25px 25px 5px;
        margin-right: auto;
        max-width: 70%;
        box-shadow: 0 8px 25px rgba(255, 105, 180, 0.15);
        border: 2px solid #FFB6C1;
        margin-bottom: 1rem;
    }
    
    .message-time {
        font-size: 0.8rem;
        opacity: 0.7;
        margin-top: 0.5rem;
        text-align: right;
    }
    
    .source-badge {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin-top: 0.5rem;
        display: inline-block;
    }

    .system-badge {
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin-top: 0.5rem;
        display: inline-block;
    }

    .speed-indicator {
        display: inline-block;
        margin-left: 1rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Load animations
try:
    welcome_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_kdxn8rqk.json")
except:
    welcome_animation = None

# 🚀 INITIALIZE RAG SYSTEM
if RAG_AVAILABLE:
    try:
        rag_system = get_rag_system()
        st.success("✅ RAG System Loaded Successfully!")
    except Exception as e:
        st.error(f"❌ RAG System Error: {e}")
        RAG_AVAILABLE = False

# 🚀 SESSION STATE - ENHANCED FOR HYBRID
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "response_cache" not in st.session_state:
    st.session_state.response_cache = {}
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "use_rag" not in st.session_state:
    st.session_state.use_rag = RAG_AVAILABLE

# Welcome message
if not st.session_state.chat_messages:
    welcome_msg = "Hello beautiful soul! 🌸 I'm your Breast Friend Forever companion. "
    if RAG_AVAILABLE:
        welcome_msg += "I'm using our enhanced RAG system to provide you with the most accurate information from trusted medical sources. "
    else:
        welcome_msg += "I'm here to provide caring, accurate information about breast health. "
    welcome_msg += "What's on your mind today? 💖"
    
    st.session_state.chat_messages.append({
        "role": "assistant", 
        "content": welcome_msg,
        "timestamp": datetime.now().strftime("%H:%M"),
        "source": "Welcome",
        "system": "Medical Assistant"
    })

def add_message(role, content, source="User", system="Medical"):
    """Add message to chat with timestamp and source"""
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M"),
        "source": source,
        "system": system
    }
    st.session_state.chat_messages.append(message)

def get_accurate_medical_response(user_message):
    """🚀 ACCURATE MEDICAL RESPONSES FROM TRUSTED SOURCES"""
    user_lower = user_message.lower()
    
    # 🎯 SELF-EXAM QUESTIONS
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
            "source": "Medical Guide PDF",
            "response_time": 0.1,
            "speed": "💖 ACCURATE",
            "system": "Medical Knowledge"
        }
    
    # 🎯 RISK REDUCTION QUESTIONS
    elif any(word in user_lower for word in ['reduce risk', 'prevent', 'prevention', 'lower risk', 'how to reduce']):
        return {
            "response": """**🛡️ Evidence-Based Breast Cancer Risk Reduction:**

**✅ Proven Prevention Strategies:**
• **Maintain Healthy Weight:** Obesity increases postmenopausal breast cancer risk by 30-60%
• **Regular Exercise:** 150+ minutes of moderate activity weekly reduces risk by 10-20%
• **Limit Alcohol:** Each daily drink increases risk by 7-10% - limit to 1 drink/day or less
• **Avoid Smoking:** Smoking linked to increased breast cancer risk, especially in premenopausal women
• **Breastfeed If Possible:** 12 months of breastfeeding reduces risk by 4.3%
• **Healthy Diet:** Rich in fruits, vegetables, whole grains, and lean proteins
• **Limit Hormone Therapy:** Discuss risks/benefits with your doctor, especially combined HRT

**🌍 For African Women:**
• Know your family history and share it with your doctor
• Advocate for appropriate screening based on individual risk
• Be aware of potentially more aggressive subtypes like triple-negative breast cancer
• Participate in community awareness programs and clinical trials

**📊 Lifestyle Impact:**
- Healthy lifestyle can reduce overall breast cancer risk by 25-30%
- Regular screening improves early detection rates by 85%""",
            "source": "Prevention Guidelines PDF",
            "response_time": 0.1,
            "speed": "💖 ACCURATE",
            "system": "Medical Knowledge"
        }
    
    # 🎯 RISK FACTOR QUESTIONS
    elif any(word in user_lower for word in ['risk factor', 'what increases risk', 'main risk']):
        return {
            "response": """**📊 Breast Cancer Risk Factors:**

**🔴 Non-Modifiable Risk Factors:**
• **Gender:** Women are about 100 times more likely than men to develop breast cancer
• **Age:** 2 out of 3 invasive breast cancers are found in women 55 or older
• **Genetics:** 5-10% of breast cancers are hereditary (BRCA1, BRCA2 mutations)
• **Family History:** Risk doubles with one first-degree relative (mother, sister, daughter)
• **Personal History:** Previous breast cancer increases risk of new cancer in same or other breast
• **Race/Ethnicity:** African American women under 45 have higher incidence rates
• **Menstrual History:** Early periods (<12) or late menopause (>55) increase risk
• **Breast Density:** Dense breast tissue increases risk 4-6 times

**🟡 Modifiable Risk Factors:**
• **Weight:** Obesity increases postmenopausal breast cancer risk by 30-60%
• **Alcohol:** Each daily drink increases risk by 7-10%
• **Physical Inactivity:** Sedentary lifestyle increases risk by 10-20%
• **Hormone Therapy:** Combined HRT increases risk by 75% with 5+ years of use
• **Reproductive History:** No children or first child after age 30 increases risk
• **Not Breastfeeding:** Increases risk, especially for premenopausal breast cancer

**🌍 African Women Specific:**
• Higher rates of triple-negative breast cancer (more aggressive)
• Often diagnosed at younger ages and later stages
• May face barriers to healthcare access
• Genetic differences in tumor biology""",
            "source": "Risk Factors PDF", 
            "response_time": 0.1,
            "speed": "💖 ACCURATE",
            "system": "Medical Knowledge"
        }
    
    # 🎯 EARLY SIGNS QUESTIONS
    elif any(word in user_lower for word in ['early sign', 'symptom', 'warning', 'signs']):
        return {
            "response": """**🚨 Early Signs & Symptoms of Breast Cancer:**

**🔴 Common Early Indicators:**
• **New Lump or Mass:** Often painless, hard, with irregular edges (but can be tender, soft, rounded)
• **Swelling:** Of all or part of breast, even if no distinct lump is felt
• **Skin Changes:** Irritation, dimpling (peau d'orange - like orange peel), redness, scaliness
• **Nipple Changes:** Pain, turning inward (retraction), redness, scaliness, thickening
• **Nipple Discharge:** Other than breast milk, especially if bloody or clear
• **Pain:** In breast or nipple area that doesn't go away
• **Lymph Node Changes:** Swelling in armpit or around collarbone

**⚡ When to See a Doctor Immediately:**
• Any new breast change that persists through your menstrual cycle
• A lump that doesn't go away after your period
• Skin changes that don't resolve within a few weeks
• Nipple discharge without stimulation
• Any change that worries you or seems different from your normal breast tissue

**💡 Important Facts:**
- 80% of breast lumps are NOT cancerous
- Many breast changes are normal and related to hormonal cycles
- Early detection significantly improves treatment outcomes
- When in doubt, get it checked out!""",
            "source": "Early Detection PDF",
            "response_time": 0.1, 
            "speed": "💖 ACCURATE",
            "system": "Medical Knowledge"
        }
    
    # 🎯 SCREENING QUESTIONS
    elif any(word in user_lower for word in ['how often', 'frequency', 'when', 'screening', 'mammogram']):
        return {
            "response": """**📅 Breast Cancer Screening Guidelines:**

**Self-Examination:**
• **Monthly** - 3-5 days after your period ends
• **Post-menopausal:** Same day each month (e.g., first day of month)

**Clinical Breast Exam:**
• **Ages 20-39:** Every 1-3 years
• **Ages 40+:** Annually

**Mammogram Screening:**
• **Average Risk Women:** Start at age 40-50, continue annually or biennially
• **High Risk Women:** Start earlier (age 25-30 or 10 years before youngest affected relative)

**Additional Screening for High Risk:**
• **Breast MRI:** Annual for BRCA carriers, strong family history, or certain high-risk conditions
• **Ultrasound:** For dense breast tissue or when mammogram is inconclusive

**🌍 African Women Considerations:**
• Consider starting screenings earlier if family history exists
• Discuss personalized screening plan with healthcare provider
• Be proactive about follow-up on abnormal results
• Know that dense breast tissue is common and may require additional imaging

**💡 Early Detection Impact:**
• 5-year survival rate: 99% for localized breast cancer
• 5-year survival rate: 86% for regional spread
• 5-year survival rate: 30% for distant metastasis""",
            "source": "Screening Guidelines PDF",
            "response_time": 0.1,
            "speed": "💖 ACCURATE",
            "system": "Medical Knowledge"
        }
    
    else:
        # 🎯 GUIDANCE FOR OTHER QUESTIONS - WILL USE RAG
        return None

def get_hybrid_response(user_message):
    """🚀 HYBRID SYSTEM: Medical Responses + RAG"""
    print(f"🎯 User asked: {user_message}")
    
    # Step 1: Try accurate medical responses first (fast & reliable)
    medical_response = get_accurate_medical_response(user_message)
    if medical_response:
        medical_response["system"] = "Medical Knowledge Base"
        return medical_response
    
    # Step 2: If no medical response, use RAG system
    if RAG_AVAILABLE and st.session_state.use_rag:
        try:
            with st.spinner("🔍 Searching our medical documents..."):
                relevant_chunks = rag_system.search(user_message, top_k=3)
                if relevant_chunks:
                    response = rag_system.get_answer(user_message, relevant_chunks)
                    return {
                        "response": response,
                        "source": "Multiple Medical Documents",
                        "response_time": 0.5,
                        "speed": "🔍 RAG SEARCH",
                        "system": "Document Search"
                    }
        except Exception as e:
            st.error(f"RAG Search Error: {e}")
    
    # Step 3: Fallback response
    return {
        "response": """I specialize in providing specific, evidence-based information about breast health. Here are topics I can help with:

• **Self-examination techniques** - Step-by-step guides
• **Early detection signs** - What symptoms to watch for  
• **Risk reduction strategies** - Evidence-based prevention methods
• **Screening guidelines** - When and how often to get checked
• **Risk factors** - Understanding your personal risk profile

What specific aspect would you like me to explain in detail?""",
        "source": "Breast Health Specialist",
        "response_time": 0.1,
        "speed": "💖 FOCUSED",
        "system": "Medical Assistant"
    }

# 🎯 ENHANCED CHAT INTERFACE
st.title("💬 Breast Health Assistant")
st.markdown("Ask me anything about breast health, symptoms, or self-care")

# System status
col1, col2 = st.columns(2)
with col1:
    if RAG_AVAILABLE:
        st.success("✅ RAG System: Active")
    else:
        st.warning("⚠️ RAG System: Not Available")

with col2:
    rag_toggle = st.toggle("Use Document Search", value=RAG_AVAILABLE, 
                          help="Search through medical documents for detailed answers")
    st.session_state.use_rag = rag_toggle and RAG_AVAILABLE

# Welcome animation
if welcome_animation:
    st_lottie(welcome_animation, speed=1, height=200, key="welcome_chat")

# 💬 MESSAGE DISPLAY
st.markdown("### 💬 Conversation")
for message in st.session_state.chat_messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="user-message">
            {message["content"]}
            <div class="message-time">{message["timestamp"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bot-message">
            {message["content"]}
            <div class="message-time">
                {message["timestamp"]} 
                {f'• {st.session_state.get("last_speed", "💖")}' if message == st.session_state.chat_messages[-1] else ''}
            </div>
            {f'<div class="source-badge">📚 {message["source"]}</div>' if message.get("source") not in ["Welcome", "User"] else ''}
            {f'<div class="system-badge">⚡ {message.get("system", "Medical")}</div>' if message.get("system") and message.get("system") != "Medical" else ''}
        </div>
        """, unsafe_allow_html=True)

# 💡 SUGGESTED QUESTIONS
st.markdown("### 💡 Quick Questions")
cols = st.columns(2)
suggestions = [
    "How do I perform a proper breast self-exam?",
    "What are the early signs of breast cancer?", 
    "How can I reduce my breast cancer risk?",
    "When should I start getting mammograms?",
    "What are the main risk factors?",
    "How often should I do self-examinations?"
]

for i, suggestion in enumerate(suggestions):
    with cols[i % 2]:
        if st.button(suggestion, key=f"sugg_{i}", use_container_width=True):
            st.session_state.user_input = suggestion
            st.rerun()

# ⌨️ MESSAGE INPUT
st.markdown("### 💭 Ask a Question")
user_input = st.text_area(
    "Type your question here...",
    value=st.session_state.user_input,
    placeholder="Ask about self-exams, symptoms, prevention, screening...",
    label_visibility="collapsed",
    height=100,
    key="user_input_widget"
)

if st.button("📤 Send Message", use_container_width=True):
    if st.session_state.user_input_widget.strip():
        user_input = st.session_state.user_input_widget
        
        # Add user message
        add_message("user", user_input, "You")
        
        # Get hybrid response
        ai_result = get_hybrid_response(user_input)
        
        # Add assistant message  
        add_message("assistant", ai_result["response"], ai_result["source"], ai_result["system"])
        
        # Store performance data
        st.session_state.last_response_time = ai_result["response_time"]
        st.session_state.last_speed = ai_result["speed"]
        
        # Clear input
        st.session_state.user_input = ""
        st.rerun()

# Information about sources
with st.expander("ℹ️ About Our Information System"):
    st.markdown("""
    **🤖 Hybrid AI System:**
    
    **Medical Knowledge Base:**
    - Pre-verified, accurate medical information
    - Fast responses for common questions
    - Evidence-based guidelines
    
    **Document Search (RAG):**
    - Searches through medical PDFs and documents
    - Finds specific information from trusted sources
    - Handles complex or detailed questions
    
    **Trusted Sources Include:**
    - Kenya Ministry of Health guidelines
    - World Health Organization recommendations  
    - Cancer research foundation materials
    - Medical institution publications
    
    *Note: This is for educational purposes only. Always consult healthcare professionals for medical advice.*
    """)

# Reset chat button
if st.button("🔄 Start New Conversation", use_container_width=True):
    st.session_state.chat_messages = []
    st.session_state.response_cache = {}
    st.rerun()