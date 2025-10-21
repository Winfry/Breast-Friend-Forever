# Web/pages/2_💬_Chat_Assistant.py
import streamlit as st
import time
import requests
import json
import random
from datetime import datetime
from utils.api_client import api_client  # Your fast backend connection

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

st.set_page_config(page_title="Chat Assistant", page_icon="💬", layout="wide")

# 🎨 YOUR BEAUTIFUL ANIMATIONS CSS (KEEP ALL OF IT!)
st.markdown("""
    <style>
    @keyframes messageSlideIn {
        0% { opacity: 0; transform: translateY(20px) scale(0.95); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }
    
    @keyframes typingDots {
        0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
        30% { transform: translateY(-10px); opacity: 1; }
    }
    
    @keyframes chatPulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 105, 180, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(255, 105, 180, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 105, 180, 0); }
    }
    
    @keyframes floatUp {
        0% { transform: translateY(100px) rotate(0deg); opacity: 0; }
        100% { transform: translateY(0) rotate(360deg); opacity: 1; }
    }
    
    @keyframes glowText {
        0%, 100% { text-shadow: 0 0 5px rgba(255, 105, 180, 0.5); }
        50% { text-shadow: 0 0 20px rgba(255, 105, 180, 0.8), 0 0 30px rgba(255, 105, 180, 0.6); }
    }
    
    .chat-container {
        max-height: 60vh;
        overflow-y: auto;
        padding: 2rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 25px;
        margin: 2rem 0;
        border: 3px solid #FFF0F5;
    }
    
    .message-wrapper {
        animation: messageSlideIn 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        margin: 1.5rem 0;
    }
    
    .user-message {
        background: linear-gradient(135deg, #FF69B4, #EC4899);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 25px 25px 5px 25px;
        margin-left: auto;
        max-width: 70%;
        box-shadow: 0 8px 25px rgba(255, 105, 180, 0.3);
        position: relative;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .user-message::after {
        content: '';
        position: absolute;
        bottom: -8px;
        right: 10px;
        width: 20px;
        height: 20px;
        background: #FF69B4;
        transform: rotate(45deg);
        border-radius: 5px;
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
        position: relative;
    }
    
    .bot-message::before {
        content: '🤖';
        position: absolute;
        left: -50px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 2rem;
        animation: floatUp 2s ease-out;
    }
    
    .typing-indicator {
        background: linear-gradient(135deg, #FFF0F5, #FFE4EC);
        padding: 1.5rem 2rem;
        border-radius: 25px 25px 25px 5px;
        margin-right: auto;
        max-width: 200px;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        animation: chatPulse 2s infinite;
    }
    
    .typing-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: linear-gradient(135deg, #FF69B4, #EC4899);
        animation: typingDots 1.4s infinite;
    }
    
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    
    .suggestion-chip {
        display: inline-block;
        background: linear-gradient(135deg, #FFF0F5, #FFE4EC);
        padding: 1rem 1.5rem;
        border-radius: 50px;
        margin: 0.5rem;
        border: 2px solid #FFB6C1;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        font-weight: 500;
        color: #FF69B4;
        animation: messageSlideIn 0.6s ease-out;
    }
    
    .suggestion-chip:hover {
        background: linear-gradient(135deg, #FF69B4, #EC4899);
        color: white;
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 10px 25px rgba(255, 105, 180, 0.4);
        border-color: #FF69B4;
    }
    
    .chat-input-container {
        background: white;
        padding: 2rem;
        border-radius: 25px;
        box-shadow: 0 -5px 25px rgba(0, 0, 0, 0.1);
        margin-top: 2rem;
        border: 3px solid #FFF0F5;
    }
    
    .send-button {
        background: linear-gradient(135deg, #FF69B4, #EC4899);
        color: white;
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 1.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        animation: chatPulse 2s infinite;
    }
    
    .send-button:hover {
        transform: scale(1.1) rotate(10deg);
        box-shadow: 0 10px 25px rgba(255, 105, 180, 0.5);
    }
    
    .welcome-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 30px;
        text-align: center;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
        animation: floatUp 1.5s ease-out;
    }
    
    .welcome-bubble::before {
        content: '✨🌟💫';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        font-size: 4rem;
        opacity: 0.1;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .message-time {
        font-size: 0.8rem;
        opacity: 0.7;
        margin-top: 0.5rem;
        text-align: right;
    }
    
    .glow-title {
        animation: glowText 3s ease-in-out infinite;
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

    .speed-indicator {
        display: inline-block;
        margin-left: 1rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Load animations
try:
    chat_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_u8mG1R.json")
    typing_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_ukwacdcs.json")
    welcome_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_kdxn8rqk.json")
except:
    chat_animation = typing_animation = welcome_animation = None

# 🚀 MY FAST CACHING SYSTEM + YOUR INTERACTIVE SESSION STATE
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "response_cache" not in st.session_state:
    st.session_state.response_cache = {}
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = f"chat_{int(time.time())}"
if "message_submitted" not in st.session_state:
    st.session_state.message_submitted = None

# Welcome message
if not st.session_state.chat_messages:
    welcome_message = {
        "role": "assistant",
        "content": "Hello beautiful soul! 🌸 I'm your Breast Friend Forever companion. I'm here to provide caring, accurate information about breast health in a safe, supportive space. What's on your mind today? 💖",
        "timestamp": datetime.now().strftime("%H:%M"),
        "source": "Welcome"
    }
    st.session_state.chat_messages.append(welcome_message)

def add_message(role, content, source="User"):
    """Add message to chat with timestamp and source"""
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M"),
        "source": source
    }
    st.session_state.chat_messages.append(message)

def get_cached_response(message):
    """🚀 FAST CACHE: Get cached response to avoid duplicate API calls"""
    message_hash = hash(message)
    return st.session_state.response_cache.get(message_hash)

def cache_response(message, response_data):
    """🚀 FAST CACHE: Cache the response for instant future access"""
    message_hash = hash(message)
    st.session_state.response_cache[message_hash] = response_data

def get_ai_response(user_message):
    """🚀 HYBRID: Fast backend + fallback with performance tracking"""
    start_time = time.time()
    
    # First check cache (INSTANT)
    cached = get_cached_response(user_message)
    if cached:
        return {
            "response": cached["response"],
            "source": cached["source"],
            "response_time": 0.01,  # Instant from cache
            "speed": "⚡ INSTANT"
        }
    
    try:
        # Try fast backend API
        result = api_client.send_message(user_message)
        response_time = time.time() - start_time
        
        # Determine speed indicator
        if response_time < 0.5:
            speed = "⚡ LIGHTNING"
        elif response_time < 1.5:
            speed = "🚀 FAST"
        elif response_time < 3:
            speed = "🐢 SLOW"
        else:
            speed = "🐌 VERY SLOW"
        
        return {
            "response": result.get("response", "I'm here to help with breast health information."),
            "source": result.get("source", "AI Assistant"),
            "response_time": response_time,
            "speed": speed
        }
        
    except Exception as e:
        # Fallback responses (YOUR COMPASSIONATE STYLE)
        fallback_responses = [
            "I'm here to help with breast health information! 💖 Remember to consult healthcare professionals for medical advice. What specific aspect of breast health would you like to know more about?",
            "That's a great question! 🌟 While I connect to our knowledge base, remember that regular self-exams are an important part of breast health awareness. Would you like me to explain the proper technique?",
            "I appreciate you asking about breast health! 🌸 For personalized medical advice, it's always best to consult with healthcare professionals. What general information can I provide about self-examination or breast awareness?"
        ]
        
        return {
            "response": random.choice(fallback_responses),
            "source": "Compassionate Assistant",
            "response_time": time.time() - start_time,
            "speed": "💖 IMMEDIATE"
        }

def send_message_callback():
    """Handle message sending with your interactive flow"""
    if st.session_state.user_input:
        st.session_state.message_submitted = st.session_state.user_input
        st.session_state.user_input = ""
        st.rerun()

# Handle submitted messages
if st.session_state.get("message_submitted"):
    user_input = st.session_state.message_submitted
    st.session_state.message_submitted = None
    
    # Add user message immediately
    add_message("user", user_input, "You")
    
    # Get AI response with performance tracking
    with st.spinner("🔍 Searching our medical knowledge base..."):
        ai_result = get_ai_response(user_input)
    
    # Cache the response for future instant access
    cache_response(user_input, {
        "response": ai_result["response"],
        "source": ai_result["source"]
    })
    
    # Add assistant message
    add_message("assistant", ai_result["response"], ai_result["source"])
    
    # Store performance data
    st.session_state.last_response_time = ai_result["response_time"]
    st.session_state.last_speed = ai_result["speed"]
    
    st.rerun()

# 🎨 YOUR BEAUTIFUL CHAT INTERFACE (KEEP ALL OF IT!)
st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 class="glow-title" style="color: #FF69B4; font-size: 3rem; margin-bottom: 1rem;">
            💬 Your Caring Companion
        </h1>
        <p style="font-size: 1.3rem; color: #666;">
            No question is too small - ask away! 🌈
        </p>
    </div>
    """, unsafe_allow_html=True)

# Welcome animation
if welcome_animation:
    st_lottie(welcome_animation, speed=1, height=200, key="welcome_chat")

# 💬 CHAT MESSAGES DISPLAY (ENHANCED WITH SOURCE BADGES)
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for i, message in enumerate(st.session_state.chat_messages):
    message_class = "user-message" if message["role"] == "user" else "bot-message"
    animation_delay = f"animation-delay: {i * 0.1}s;"
    
    message_html = f"""
        <div class="message-wrapper" style="{animation_delay}">
            <div class="{message_class}">
                {message["content"]}
                <div class="message-time">
                    {message["timestamp"]}
                    {'' if message["role"] == 'user' else f'<span class="speed-indicator">• {st.session_state.get("last_speed", "💖")}</span>' if i == len(st.session_state.chat_messages)-1 and message["role"] == "assistant" else ''}
                </div>
                {'' if message["role"] == 'user' else f'<div class="source-badge">📚 {message.get("source", "AI Assistant")}</div>' if message.get("source") not in ["User", "Welcome"] else ''}
            </div>
        </div>
    """
    
    st.markdown(message_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 💡 YOUR SUGGESTED QUESTIONS (WITH CACHING)
st.markdown("### 💡 Quick Questions to Get Started")

suggestions = [
    "How do I perform a proper breast self-exam?",
    "What are the early signs of breast cancer?",
    "When should I start getting mammograms?",
    "What lifestyle changes support breast health?",
    "Can you explain different screening methods?",
    "How often should I do self-examinations?",
    "What are normal breast changes to expect?",
    "How can I reduce my breast cancer risk?"
]

# Create animated suggestion chips
st.markdown('<div style="text-align: center; margin: 2rem 0;">', unsafe_allow_html=True)
cols = st.columns(4)
for i, suggestion in enumerate(suggestions):
    with cols[i % 4]:
        if st.button(
            suggestion, 
            key=f"sugg_{i}", 
            use_container_width=True,
            type="secondary"
        ):
            st.session_state.user_input = suggestion
            send_message_callback()
st.markdown('</div>', unsafe_allow_html=True)

# ⌨️ YOUR MESSAGE INPUT AREA
st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)

col1, col2 = st.columns([6, 1])

with col1:
    st.text_area(
        "Type your message here... 💭",
        key="user_input",
        placeholder="Ask me anything about breast health, self-care, symptoms, or concerns...",
        label_visibility="collapsed",
        height=100
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("➤", help="Send message", use_container_width=True, on_click=send_message_callback)

st.markdown('</div>', unsafe_allow_html=True)

# 🌟 YOUR CHAT FEATURES & TIPS (ENHANCED WITH PERFORMANCE INFO)
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    with st.expander("💖 Chat Features", expanded=True):
        st.markdown("""
            <div style="padding: 1rem;">
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <span style="font-size: 2rem; margin-right: 1rem;">⚡</span>
                    <div>
                        <strong>Instant Caching</strong>
                        <p style="margin: 0; color: #666;">Repeated questions answered instantly</p>
                    </div>
                </div>
                
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <span style="font-size: 2rem; margin-right: 1rem;">🔒</span>
                    <div>
                        <strong>Private & Anonymous</strong>
                        <p style="margin: 0; color: #666;">No personal data stored</p>
                    </div>
                </div>
                
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <span style="font-size: 2rem; margin-right: 1rem;">📚</span>
                    <div>
                        <strong>PDF-Powered</strong>
                        <p style="margin: 0; color: #666;">Medical knowledge from trusted sources</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

with col2:
    with st.expander("🌟 Performance Info", expanded=True):
        if st.session_state.get('last_response_time'):
            st.metric("Last Response Time", f"{st.session_state.last_response_time:.2f}s")
            st.metric("Speed", st.session_state.get('last_speed', '💖'))
        else:
            st.info("Ask a question to see performance metrics!")
        
        st.progress(len(st.session_state.response_cache) / 50, text=f"Cached: {len(st.session_state.response_cache)}/50")

# 🎊 YOUR INTERACTIVE CHAT STATS (ENHANCED)
st.markdown("---")

if len(st.session_state.chat_messages) > 1:
    st.markdown("### 📊 Your Conversation Stats")
    
    user_msgs = len([m for m in st.session_state.chat_messages if m["role"] == "user"])
    bot_msgs = len([m for m in st.session_state.chat_messages if m["role"] == "assistant"])
    cached_responses = len(st.session_state.response_cache)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Messages Sent", user_msgs)
    with col2:
        st.metric("Responses Received", bot_msgs)
    with col3:
        st.metric("Cached Answers", cached_responses)
    with col4:
        efficiency = "⚡ High" if cached_responses > user_msgs * 0.3 else "🚀 Good" if cached_responses > 0 else "💖 New"
        st.metric("Cache Efficiency", efficiency)

# 🎨 YOUR FUN INTERACTIVE ELEMENTS (KEEP ALL!)
with st.expander("🎨 Fun Chat Tools"):
    tab1, tab2, tab3 = st.tabs(["Mood Check", "Quick Affirmation", "Breath Exercise"])
    
    with tab1:
        mood = st.selectbox(
            "How are you feeling about this conversation?",
            ["😊 Hopeful and informed", "🤔 Curious and learning", "💪 Empowered and strong", "🌸 Calm and reassured"],
            key="chat_mood"
        )
        if mood:
            mood_responses = {
                "😊 Hopeful and informed": "That's wonderful! Knowledge brings hope and power. 🌟",
                "🤔 Curious and learning": "Curiosity is the first step to empowerment! 🧠",
                "💪 Empowered and strong": "Your strength in seeking knowledge is inspiring! 💪",
                "🌸 Calm and reassured": "Peace and reassurance are powerful allies in health. 🍃"
            }
            st.success(f"**{mood_responses[mood]}**")
    
    with tab2:
        if st.button("💝 Get Positive Affirmation"):
            affirmations = [
                "You are taking powerful steps for your health! 💪",
                "Your questions show self-care and wisdom! 🌸",
                "Learning about your health is an act of self-love! 💖",
                "You're building a better relationship with your body! 🌟"
            ]
            st.info(f"**{random.choice(affirmations)}**")
    
    with tab3:
        if st.button("🌬️ Take a Breathing Break"):
            with st.spinner("Breathing in... and out... 💨"):
                for i in range(3):
                    st.write(f"Breathe {i+1}...")
                    time.sleep(1)
            st.success("Ahhh... refreshed and ready to continue! 😌")

# 🎉 YOUR CHAT COMPLETION CELEBRATION
if len(st.session_state.chat_messages) >= 10:
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #FF69B4, #EC4899); color: white; border-radius: 25px;">
            <h3>🎊 Conversation Champion! 🎊</h3>
            <p>You've had a meaningful conversation about breast health! Keep learning and asking questions! 🌟</p>
        </div>
        """, unsafe_allow_html=True)

# Reset chat button
if st.button("🔄 Start New Conversation", use_container_width=True):
    st.session_state.chat_messages = []
    st.session_state.response_cache = {}
    st.session_state.conversation_id = f"chat_{int(time.time())}"
    st.rerun()