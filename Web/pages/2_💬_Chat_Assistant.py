import streamlit as st
import time
import requests
import json
import random
from streamlit_lottie import st_lottie
from datetime import datetime

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

st.set_page_config(page_title="Chat Assistant", page_icon="💬", layout="wide")

# 🎨 ADVANCED CHAT ANIMATIONS CSS
st.markdown("""
    <style>
    @keyframes messageSlideIn {
        0% {
            opacity: 0;
            transform: translateY(20px) scale(0.95);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    @keyframes typingDots {
        0%, 60%, 100% {
            transform: translateY(0);
            opacity: 0.4;
        }
        30% {
            transform: translateY(-10px);
            opacity: 1;
        }
    }
    
    @keyframes chatPulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 105, 180, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(255, 105, 180, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 105, 180, 0); }
    }
    
    @keyframes floatUp {
        0% {
            transform: translateY(100px) rotate(0deg);
            opacity: 0;
        }
        100% {
            transform: translateY(0) rotate(360deg);
            opacity: 1;
        }
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
    </style>
    """, unsafe_allow_html=True)

# Load animations
try:
    chat_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_u8mG1R.json")
    typing_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_ukwacdcs.json")
    welcome_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_kdxn8rqk.json")
except:
    chat_animation = typing_animation = welcome_animation = None

# Initialize chat session
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "is_typing" not in st.session_state:
    st.session_state.is_typing = False
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = f"chat_{int(time.time())}"

# Welcome message
if not st.session_state.chat_messages:
    welcome_message = {
        "role": "assistant",
        "content": "Hello beautiful soul! 🌸 I'm your Breast Friend Forever companion. I'm here to provide caring, accurate information about breast health in a safe, supportive space. What's on your mind today? 💖",
        "timestamp": datetime.now().strftime("%H:%M")
    }
    st.session_state.chat_messages.append(welcome_message)

def add_message(role, content):
    """Add message to chat with timestamp"""
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M")
    }
    st.session_state.chat_messages.append(message)

def simulate_ai_thinking():
    """Show typing indicator and simulate thinking"""
    st.session_state.is_typing = True
    st.rerun()
    
    # Simulate AI processing time
    time.sleep(2)
    
    st.session_state.is_typing = False

def get_ai_response(user_message):
    """Get response from backend or use fallback"""
    try:
        # Try to get response from backend
        response = requests.post(
            "http://localhost:8000/api/v1/chat/message",
            json={
                "message": user_message,
                "conversation_id": st.session_state.conversation_id
            },
            timeout=10
        )
        if response.status_code == 200:
            return response.json()["response"]
    except:
        pass
    
    # Fallback responses
    fallback_responses = [
        "I'm here to help with breast health information! 💖 Remember to consult healthcare professionals for medical advice. What specific aspect of breast health would you like to know more about?",
        "That's a great question! 🌟 While I connect to our knowledge base, remember that regular self-exams are an important part of breast health awareness. Would you like me to explain the proper technique?",
        "I appreciate you asking about breast health! 🌸 For personalized medical advice, it's always best to consult with healthcare professionals. What general information can I provide about self-examination or breast awareness?",
        "Your health questions are important! 💪 I'm here to provide educational information about breast health. For specific concerns, healthcare providers can offer the best guidance. What would you like to learn about today?"
    ]
    return random.choice(fallback_responses)

def send_message():
    """Handle sending messages"""
    user_input = st.session_state.get("user_input", "").strip()
    if user_input:
        # Add user message
        add_message("user", user_input)
        st.session_state.user_input = ""
        
        # Show typing indicator
        simulate_ai_thinking()
        
        # Get AI response
        ai_response = get_ai_response(user_input)
        
        # Add AI response
        add_message("assistant", ai_response)
        st.rerun()

# 🎨 CHAT INTERFACE
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

# 💬 CHAT MESSAGES DISPLAY
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for i, message in enumerate(st.session_state.chat_messages):
    message_class = "user-message" if message["role"] == "user" else "bot-message"
    animation_delay = f"animation-delay: {i * 0.1}s;"
    
    st.markdown(f"""
        <div class="message-wrapper" style="{animation_delay}">
            <div class="{message_class}">
                {message["content"]}
                <div class="message-time">{message["timestamp"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Typing indicator
if st.session_state.is_typing:
    st.markdown("""
        <div class="message-wrapper">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <span style="color: #FF69B4; margin-left: 1rem;">Thinking...</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 💡 SUGGESTED QUESTIONS
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
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# ⌨️ MESSAGE INPUT AREA
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
    if st.button("➤", help="Send message", use_container_width=True):
        send_message()

st.markdown('</div>', unsafe_allow_html=True)

# 🌟 CHAT FEATURES & TIPS
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    with st.expander("💖 Chat Features", expanded=True):
        st.markdown("""
            <div style="padding: 1rem;">
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <span style="font-size: 2rem; margin-right: 1rem;">🔒</span>
                    <div>
                        <strong>Private & Anonymous</strong>
                        <p style="margin: 0; color: #666;">No personal data stored</p>
                    </div>
                </div>
                
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <span style="font-size: 2rem; margin-right: 1rem;">🌐</span>
                    <div>
                        <strong>Educational Focus</strong>
                        <p style="margin: 0; color: #666;">Information & support</p>
                    </div>
                </div>
                
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 2rem; margin-right: 1rem;">💫</span>
                    <div>
                        <strong>Compassionate AI</strong>
                        <p style="margin: 0; color: #666;">Caring, non-judgmental</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

with col2:
    with st.expander("🌟 Conversation Tips", expanded=True):
        st.markdown("""
            <div style="padding: 1rem;">
                <div style="background: #FFF0F5; padding: 1rem; border-radius: 15px; margin-bottom: 1rem;">
                    <strong>🎯 Be Specific</strong>
                    <p style="margin: 0.5rem 0 0 0; color: #666;">Ask detailed questions for better answers</p>
                </div>
                
                <div style="background: #FFF0F5; padding: 1rem; border-radius: 15px; margin-bottom: 1rem;">
                    <strong>💡 Use Suggestions</strong>
                    <p style="margin: 0.5rem 0 0 0; color: #666;">Click quick questions to start</p>
                </div>
                
                <div style="background: #FFF0F5; padding: 1rem; border-radius: 15px;">
                    <strong>🩺 Medical Advice</strong>
                    <p style="margin: 0.5rem 0 0 0; color: #666;">Always consult professionals for diagnoses</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

# 🎊 INTERACTIVE CHAT STATS
st.markdown("---")

if len(st.session_state.chat_messages) > 1:
    st.markdown("### 📊 Your Conversation Stats")
    
    user_msgs = len([m for m in st.session_state.chat_messages if m["role"] == "user"])
    bot_msgs = len([m for m in st.session_state.chat_messages if m["role"] == "assistant"])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Messages Sent", user_msgs)
    with col2:
        st.metric("Responses Received", bot_msgs)
    with col3:
        st.metric("Conversation Length", f"{len(st.session_state.chat_messages)}")
    with col4:
        st.metric("Your Engagement", "Active 🌟")

# 🎨 FUN INTERACTIVE ELEMENTS
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

# 🎉 CHAT COMPLETION CELEBRATION
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
    st.session_state.is_typing = False
    st.rerun()