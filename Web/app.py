import streamlit as st
from streamlit_lottie import st_lottie
import requests
import json
import time

# Function to load Lottie animations
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Function to load local Lottie files
def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except:
        return None

# 🎨 ULTIMATE ANIMATION CSS
st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(255, 105, 180, 0.3); }
        50% { box-shadow: 0 0 40px rgba(255, 105, 180, 0.6); }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-100px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInRight {
        from { transform: translateX(100px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .main-header {
        animation: fadeIn 1s ease-out, glow 3s infinite;
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #FF69B4, #FF1493, #DB2777);
        color: white;
        border-radius: 25px;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: rotate 6s linear infinite;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #FFF0F5, #FFE4EC);
        border-radius: 25px;
        padding: 2.5rem 2rem;
        margin: 1.5rem 0;
        border: 3px solid transparent;
        background-clip: padding-box;
        position: relative;
        overflow: hidden;
        animation: fadeIn 0.8s ease-out;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.6s;
    }
    
    .feature-card:hover {
        transform: translateY(-10px) scale(1.02);
        border-color: #FF69B4;
        box-shadow: 0 20px 40px rgba(255, 105, 180, 0.3);
    }
    
    .feature-card:hover::before {
        left: 100%;
    }
    
    .floating-element {
        animation: float 4s ease-in-out infinite;
    }
    
    .pulse-element {
        animation: pulse 2s infinite;
    }
    
    .bounce-element {
        animation: bounce 2s infinite;
    }
    
    .animated-button {
        background: linear-gradient(135deg, #FF69B4, #FF1493);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        animation: pulse 2s infinite;
        position: relative;
        overflow: hidden;
    }
    
    .animated-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.5s;
    }
    
    .animated-button:hover::before {
        left: 100%;
    }
    
    .animated-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(255, 105, 180, 0.4);
    }
    
    .welcome-message {
        animation: slideInLeft 1s ease-out;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .welcome-message::after {
        content: '🌸';
        position: absolute;
        top: -20px;
        right: -20px;
        font-size: 8rem;
        opacity: 0.1;
        animation: rotate 20s linear infinite;
    }
    
    .stats-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
        animation: fadeIn 0.8s ease-out;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .stats-card:hover {
        transform: translateY(-5px);
        border-color: #FF69B4;
        box-shadow: 0 15px 35px rgba(255, 105, 180, 0.2);
    }
    
    .typing-animation {
        display: inline-block;
        overflow: hidden;
        border-right: 3px solid #FF69B4;
        white-space: nowrap;
        animation: typing 3.5s steps(40, end), blink-caret 0.75s step-end infinite;
    }
    
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    
    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: #FF69B4; }
    }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(
    page_title="Breast Friend Forever 💖",
    page_icon="💖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🌟 Load Lottie Animations
try:
    heart_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_5njp3vgg.json")
    chat_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_u8mG1R.json")
    book_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_sgn7zqbs.json")
    location_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_0fhgwtli.json")
    community_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_5tt2Th.json")
    welcome_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_ukwacdcs.json")
except:
    heart_animation = chat_animation = book_animation = location_animation = community_animation = welcome_animation = None

# 🎊 ANIMATED HEADER
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
        <div class="main-header">
            <h1 style="margin: 0; font-size: 3.5rem;">💖 Breast Friend Forever</h1>
            <p style="font-size: 1.4rem; margin: 1rem 0 0 0; opacity: 0.9;">
                Your <span class="typing-animation">compassionate breast health companion</span>
            </p>
        </div>
    """, unsafe_allow_html=True)

# 🎭 Welcome Animation
if welcome_animation:
    st_lottie(welcome_animation, speed=1, height=300, key="welcome")

# 🌈 ANIMATED FEATURE CARDS
st.markdown("""
    <div style="text-align: center; margin: 3rem 0;">
        <h2 style="color: #FF69B4; font-size: 2.5rem;" class="bounce-element">
            🌸 How Can We Support You Today?
        </h2>
    </div>
    """, unsafe_allow_html=True)

features = [
    {"animation": heart_animation, "title": "🖐️ Self-Exam Guide", "desc": "Step-by-step guidance with love and care", "page": "pages/1_🤗_Self_Exam.py", "color": "#FF69B4"},
    {"animation": chat_animation, "title": "💬 Chat Assistant", "desc": "Ask anything, no judgment - we're here for you", "page": "pages/2_💬_Chat_Assistant.py", "color": "#EC4899"},
    {"animation": book_animation, "title": "📚 Resources", "desc": "Learn at your own pace with beautiful materials", "page": "pages/3_📚_Resources.py", "color": "#DB2777"},
    {"animation": location_animation, "title": "🏥 Find Screening", "desc": "Locate caring professionals near you", "page": "pages/4_🏥_Find_Screening.py", "color": "#BE185D"},
    {"animation": community_animation, "title": "💕 Encouragement Wall", "desc": "Share hope and strength with our community", "page": "pages/5_💕_Encouragement_Wall.py", "color": "#9D174D"},
]

# Display features in an animated grid
cols = st.columns(3)
for i, feature in enumerate(features):
    with cols[i % 3]:
        # Feature card with animation delay
        animation_delay = f"animation-delay: {i * 0.2}s;"
        
        st.markdown(f"""
            <div class="feature-card" style="{animation_delay} border-color: {feature['color']};">
                <div style="text-align: center;">
                    <h3 style="color: {feature['color']}; margin-bottom: 1rem;">{feature['title']}</h3>
                    <p style="color: #666; line-height: 1.6; margin-bottom: 1.5rem;">{feature['desc']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Lottie animation
        if feature['animation']:
            st_lottie(
                feature['animation'],
                speed=1,
                reverse=False,
                loop=True,
                quality="low",
                height=120,
                width=120,
                key=f"feature_anim_{i}"
            )
        
        # Animated button
        if st.button(f"Explore →", key=f"btn_{i}", use_container_width=True):
            st.switch_page(feature['page'])

# 🎯 INTERACTIVE WELCOME SECTION
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="welcome-message">
            <h2 style="color: white; margin-bottom: 1rem;">🌈 Welcome, Beautiful Soul!</h2>
            <p style="color: white; font-size: 1.1rem; line-height: 1.6;">
                We're so glad you're here. This is your safe space for breast health education 
                and support. No judgment, just compassion and care.
            </p>
            <div style="display: flex; gap: 1rem; margin-top: 1.5rem;">
                <span class="pulse-element">💖</span>
                <span class="pulse-element" style="animation-delay: 0.5s;">🌟</span>
                <span class="pulse-element" style="animation-delay: 1s;">🌸</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    # Interactive mood selector
    st.markdown("### 🎯 Quick Vibe Check")
    mood = st.selectbox(
        "How are you feeling today?",
        ["✨ Choose your vibe...", "😊 Hopeful & Positive", "🤔 Curious & Learning", "💪 Strong & Empowered", "🌸 Calm & Peaceful", "🌈 Supported & Connected"],
        key="mood_main"
    )
    
    if mood != "✨ Choose your vibe...":
        mood_messages = {
            "😊 Hopeful & Positive": "Your positivity is contagious! Hope is a powerful companion. 🌟",
            "🤔 Curious & Learning": "Curiosity leads to empowerment! Every question is important. 🧠",
            "💪 Strong & Empowered": "Your strength inspires others! You're capable of amazing things. 💪",
            "🌸 Calm & Peaceful": "Peaceful energy is healing. Trust your journey. 🍃",
            "🌈 Supported & Connected": "You've got a whole community behind you! We're in this together. 💕"
        }
        
        st.success(f"**{mood_messages[mood]}**")
        
        # Celebrate mood selection
        if st.button("🎉 Celebrate This Vibe!"):
            st.balloons()
            st.success("🎊 Yay! Celebrating your amazing energy! 💫")

# 📊 ANIMATED STATISTICS
st.markdown("---")
st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h2 style="color: #FF69B4;" class="pulse-element">📈 Our Community Impact</h2>
    </div>
    """, unsafe_allow_html=True)

stats_cols = st.columns(4)
stats_data = [
    {"number": "1,234+", "label": "Lives Touched", "emoji": "💖"},
    {"number": "567+", "label": "Self-Exams Guided", "emoji": "🖐️"},
    {"number": "89+", "label": "Questions Answered", "emoji": "💬"},
    {"number": "100%", "label": "Love & Support", "emoji": "🌈"},
]

for i, stat in enumerate(stats_data):
    with stats_cols[i]:
        st.markdown(f"""
            <div class="stats-card">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;" class="bounce-element">
                    {stat['emoji']}
                </div>
                <h3 style="color: #FF69B4; margin: 0.5rem 0; font-size: 1.8rem;">{stat['number']}</h3>
                <p style="color: #666; margin: 0; font-weight: 500;">{stat['label']}</p>
            </div>
            """, unsafe_allow_html=True)

# 🎨 INTERACTIVE ELEMENTS
st.markdown("---")
st.markdown("""
    <div style="text-align: center; margin: 3rem 0;">
        <h2 style="color: #FF69B4;" class="floating-element">🎨 Quick Self-Care Check</h2>
        <p style="color: #666; font-size: 1.1rem;">Take a moment for yourself - you deserve it! 💫</p>
    </div>
    """, unsafe_allow_html=True)

self_care_cols = st.columns(3)

with self_care_cols[0]:
    if st.button("🌬️ Take a Deep Breath", use_container_width=True):
        with st.spinner("Breathing in... and out... 💨"):
            time.sleep(3)
        st.success("Ahhh... feels better, doesn't it? 😌")

with self_care_cols[1]:
    if st.button("💝 Give Yourself Credit", use_container_width=True):
        st.balloons()
        st.success("You're doing amazing! Give yourself a hug! 🤗")

with self_care_cols[2]:
    if st.button("🌟 Positive Affirmation", use_container_width=True):
        affirmations = [
            "You are strong, capable, and worthy of care! 💪",
            "Your health journey matters, and so do you! 🌸",
            "Every step you take for yourself is powerful! 🎯",
            "You're not alone - we're here with you! 💕"
        ]
        import random
        st.info(f"**{random.choice(affirmations)}**")

# 🎊 FINAL INSPIRATION
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #FFF0F5, #FFE4EC); border-radius: 25px; margin: 2rem 0;">
        <div class="floating-element" style="font-size: 4rem; margin-bottom: 1rem;">💫</div>
        <h2 style="color: #FF69B4; margin-bottom: 1rem;">Remember This Always...</h2>
        <p style="font-size: 1.2rem; color: #666; line-height: 1.6;">
            Your health journey is unique, beautiful, and worthy of celebration. 
            Every question you ask, every step you take, every moment of self-care - 
            it all matters. <strong>You matter.</strong>
        </p>
        <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 2rem;">
            <span class="pulse-element">🌸</span>
            <span class="pulse-element" style="animation-delay: 0.3s;">💖</span>
            <span class="pulse-element" style="animation-delay: 0.6s;">✨</span>
            <span class="pulse-element" style="animation-delay: 0.9s;">🌟</span>
            <span class="pulse-element" style="animation-delay: 1.2s;">🌈</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 🎵 FUN EASTER EGG
with st.expander("🎵 Secret Celebration Zone"):
    st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h3 style="color: #FF69B4;">🎊 You Found the Celebration Zone! 🎊</h3>
            <p>Because you deserve to celebrate being amazing!</p>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("🎉 Launch Celebration!"):
        st.balloons()
        st.snow()
        st.success("🎊 Hooray! Celebrating YOU! 💫")
        
        # Fun confetti effect with emojis
        st.markdown("""
            <div style="text-align: center; font-size: 2rem; margin: 2rem 0;">
                <span class="bounce-element">🎉</span>
                <span class="bounce-element" style="animation-delay: 0.2s;">✨</span>
                <span class="bounce-element" style="animation-delay: 0.4s;">🌟</span>
                <span class="bounce-element" style="animation-delay: 0.6s;">💖</span>
                <span class="bounce-element" style="animation-delay: 0.8s;">🌸</span>
            </div>
            """, unsafe_allow_html=True)