import streamlit as st
import requests
import time
from streamlit_lottie import st_lottie
import json

# 🎯 MOBILE-FIRST CONFIG
st.set_page_config(
    page_title="Breast Friend Forever",
    page_icon="💖",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar on mobile
)

# 📱 MOBILE-OPTIMIZED CSS
st.markdown("""
    <style>
    /* MOBILE-FIRST DESIGN */
    :root {
        --primary-color: #FF69B4;
        --secondary-color: #EC4899;
        --accent-color: #10B981;
        --text-color: #374151;
        --light-bg: #FFF0F5;
    }
    
    /* Base mobile styles */
    .main .block-container {
        padding: 1rem !important;
        max-width: 100% !important;
    }
    
    /* Mobile-optimized headers */
    h1 {
        font-size: 1.8rem !important;
        text-align: center;
        margin-bottom: 1rem !important;
    }
    
    h2 {
        font-size: 1.4rem !important;
        margin: 1rem 0 0.5rem 0 !important;
    }
    
    h3 {
        font-size: 1.2rem !important;
    }
    
    /* Touch-friendly buttons */
    .stButton > button {
        width: 100% !important;
        min-height: 50px !important;
        font-size: 1.1rem !important;
        border-radius: 25px !important;
        margin: 0.5rem 0 !important;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
    }
    
    /* Mobile cards */
    .mobile-card {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(255, 105, 180, 0.1);
        border: 2px solid var(--light-bg);
    }
    
    /* Mobile navigation */
    .mobile-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        border-top: 2px solid var(--light-bg);
        padding: 0.5rem;
        z-index: 1000;
        display: flex;
        justify-content: space-around;
    }
    
    .nav-btn {
        flex: 1;
        text-align: center;
        padding: 0.8rem 0.5rem;
        margin: 0 0.2rem;
        border-radius: 15px;
        background: var(--light-bg);
        border: none;
        font-size: 0.9rem;
    }
    
    .nav-btn.active {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
    }
    
    /* Chat bubbles for mobile */
    .mobile-chat-user {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 1rem;
        border-radius: 20px 20px 5px 20px;
        margin: 0.5rem 0;
        max-width: 85%;
        margin-left: auto;
    }
    
    .mobile-chat-bot {
        background: var(--light-bg);
        color: var(--text-color);
        padding: 1rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.5rem 0;
        max-width: 85%;
    }
    
    /* Mobile forms */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        font-size: 16px !important; /* Prevents zoom on iOS */
        min-height: 44px !important;
        border-radius: 15px !important;
        border: 2px solid var(--light-bg) !important;
    }
    
    /* Hide desktop elements on mobile */
    @media (max-width: 768px) {
        .desktop-only { display: none !important; }
        #MainMenu { display: none; }
        footer { display: none; }
        .stAlert { margin: 0.5rem 0 !important; }
    }
    
    /* Show mobile elements */
    .mobile-only { display: block; }
    
    /* Progress indicators */
    .mobile-progress {
        display: flex;
        justify-content: space-between;
        margin: 1rem 0;
    }
    
    .progress-step {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background: var(--light-bg);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
    }
    
    .progress-step.active {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
    }
    
    /* Animation container */
    .mobile-animation {
        text-align: center;
        margin: 1rem 0;
        padding: 1rem;
        background: var(--light-bg);
        border-radius: 15px;
    }
    </style>
    
    <!-- MOBILE META TAGS -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="theme-color" content="#FF69B4">
    
    <!-- PWA MANIFEST -->
    <link rel="manifest" href="/manifest.json">
""", unsafe_allow_html=True)

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        return None

# 🏠 MOBILE HOME PAGE
def show_mobile_home():
    st.markdown("""
        <div style="text-align: center; padding: 2rem 1rem;">
            <h1 style="color: #FF69B4; margin-bottom: 1rem;">💖 Breast Friend Forever</h1>
            <p style="color: #666; font-size: 1.1rem;">
                Your compassionate companion for breast health education and support
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Welcome animation
    heart_anim = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_5njp3vgg.json")
    if heart_anim:
        st_lottie(heart_anim, speed=1, height=200, key="mobile_welcome")
    
    # Quick actions grid
    st.markdown("### 🎯 Quick Access")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💬 **Health Chat**", use_container_width=True):
            st.session_state.current_page = "chat"
            st.rerun()
        
        if st.button("🤗 **Self Exam**", use_container_width=True):
            st.session_state.current_page = "self_exam"
            st.rerun()
    
    with col2:
        if st.button("🏥 **Find Care**", use_container_width=True):
            st.session_state.current_page = "hospitals"
            st.rerun()
        
        if st.button("💕 **Support**", use_container_width=True):
            st.session_state.current_page = "encouragement"
            st.rerun()
    
    # Today's tip
    st.markdown("""
        <div class="mobile-card">
            <h3>💡 Today's Health Tip</h3>
            <p>Perform breast self-exams monthly, about 3-5 days after your period ends. 
            Consistency helps you learn what's normal for you!</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Emergency section
    with st.expander("🚨 Quick Help & Emergency"):
        st.markdown("""
        **If you notice any of these changes, consult a healthcare provider:**
        - New lump in breast or underarm
        - Thickening or swelling of breast
        - Irritation or dimpling of breast skin
        - Redness or flaky skin in nipple area
        - Pulling in of nipple or pain in nipple area
        - Nipple discharge other than breast milk
        - Any change in size or shape of breast
        - Pain in any area of breast
        
        **Emergency Contacts:**
        - Health Emergency: 1199
        - Psychological Support: 1190
        - NHIF Services: 0709 074 000
        """)

# 💬 MOBILE CHAT PAGE
def show_mobile_chat():
    st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <button onclick="window.history.back()" style="background: none; border: none; font-size: 1.5rem; margin-right: 1rem;">←</button>
            <h1 style="margin: 0;">💬 Health Assistant</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize chat history
    if "mobile_messages" not in st.session_state:
        st.session_state.mobile_messages = [
            {"role": "assistant", "content": "Hello! I'm here to provide caring, accurate information about breast health. What would you like to know? 💖"}
        ]
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.mobile_messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="mobile-chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="mobile-chat-bot">{msg["content"]}</div>', unsafe_allow_html=True)
    
    # Quick questions
    st.markdown("**💡 Quick Questions:**")
    quick_cols = st.columns(2)
    questions = [
        "How to self-exam?",
        "Early warning signs?",
        "Reduce cancer risk?",
        "When to get screened?"
    ]
    
    for i, question in enumerate(questions):
        with quick_cols[i % 2]:
            if st.button(question, key=f"q_{i}"):
                st.session_state.mobile_messages.append({"role": "user", "content": question})
                # Simulate AI response
                st.session_state.mobile_messages.append({
                    "role": "assistant", 
                    "content": "I'd be happy to help with that! Let me provide you with accurate, helpful information about breast health. 🌸"
                })
                st.rerun()
    
    # Chat input
    user_input = st.text_input("Type your question...", placeholder="Ask about breast health...", key="mobile_chat_input")
    
    if st.button("Send Message", use_container_width=True):
        if user_input.strip():
            st.session_state.mobile_messages.append({"role": "user", "content": user_input})
            # Simulate AI thinking
            with st.spinner("💭 Thinking..."):
                time.sleep(1)
                st.session_state.mobile_messages.append({
                    "role": "assistant",
                    "content": f"I understand you're asking about: '{user_input}'. This is an important topic! For accurate medical information, I recommend consulting with healthcare professionals while using this app for educational support. 💕"
                })
            st.rerun()

# 🤗 MOBILE SELF-EXAM PAGE
def show_mobile_self_exam():
    st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <button onclick="window.history.back()" style="background: none; border: none; font-size: 1.5rem; margin-right: 1rem;">←</button>
            <h1 style="margin: 0;">🤗 Self Exam Guide</h1>
        </div>
    """, unsafe_allow_html=True)
    
    if "exam_progress" not in st.session_state:
        st.session_state.exam_progress = 0
        st.session_state.current_step = 1
    
    steps = [
        {"id": 1, "title": "Mirror Check", "desc": "Stand before mirror, arms on hips. Look for changes.", "icon": "🪞"},
        {"id": 2, "title": "Arms Up", "desc": "Raise arms overhead. Check for symmetry changes.", "icon": "🙆‍♀️"},
        {"id": 3, "title": "Lie Down", "desc": "Lie down, feel breasts with opposite hand.", "icon": "💆‍♀️"},
        {"id": 4, "title": "Circular Motion", "desc": "Use circular motions to cover entire breast.", "icon": "🌀"},
        {"id": 5, "title": "Shower Check", "desc": "Repeat in shower with soapy hands.", "icon": "🚿"}
    ]
    
    # Progress tracker
    st.markdown("<div class='mobile-progress'>", unsafe_allow_html=True)
    for i, step in enumerate(steps, 1):
        status = "active" if i <= st.session_state.current_step else ""
        st.markdown(f"<div class='progress-step {status}'>{step['icon']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Current step
    current = steps[st.session_state.current_step - 1]
    
    st.markdown(f"""
        <div class="mobile-card">
            <h2>Step {current['id']}: {current['title']}</h2>
            <p>{current['desc']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Step animation
    exam_anim = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_u8mG1R.json")
    if exam_anim:
        st.markdown("<div class='mobile-animation'>", unsafe_allow_html=True)
        st_lottie(exam_anim, speed=1, height=200, key="mobile_exam")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Navigation
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.current_step > 1:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.current_step -= 1
                st.rerun()
    
    with col2:
        if st.session_state.current_step < len(steps):
            if st.button("Next Step ➡️", use_container_width=True):
                st.session_state.current_step += 1
                st.rerun()
        else:
            if st.button("🎉 Complete!", use_container_width=True):
                st.balloons()
                st.success("You've completed the self-exam guide! 🎊")
                st.session_state.current_step = 1
    
    # Quick tips
    st.markdown("""
        <div class="mobile-card">
            <h3>💡 Remember</h3>
            <ul>
            <li>Perform monthly after your period</li>
            <li>Be gentle and thorough</li>
            <li>Learn what's normal for YOU</li>
            <li>Report any changes to your doctor</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# 🏥 MOBILE HOSPITAL FINDER
def show_mobile_hospitals():
    st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <button onclick="window.history.back()" style="background: none; border: none; font-size: 1.5rem; margin-right: 1rem;">←</button>
            <h1 style="margin: 0;">🏥 Find Care</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Search section
    st.markdown("""
        <div class="mobile-card">
            <h3>🔍 Find Healthcare</h3>
        </div>
    """, unsafe_allow_html=True)
    
    county = st.selectbox("Select County", [
        "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Thika", "Other"
    ])
    
    service = st.selectbox("Service Needed", [
        "Mammography", "Breast Ultrasound", "Clinical Exam", "Consultation", "Any"
    ])
    
    if st.button("🔍 Search Facilities", use_container_width=True):
        # Simulate search results
        facilities = [
            {"name": "Nairobi Women's Hospital", "distance": "2.3 km", "services": ["Mammography", "Ultrasound"]},
            {"name": "Aga Khan Hospital", "distance": "3.1 km", "services": ["Mammography", "Consultation"]},
            {"name": "Kenyatta Hospital", "distance": "4.5 km", "services": ["All Services"]}
        ]
        
        st.success(f"Found {len(facilities)} facilities near you")
        
        for facility in facilities:
            with st.container():
                st.markdown(f"""
                    <div class="mobile-card">
                        <h4>{facility['name']}</h4>
                        <p>📍 {facility['distance']} away</p>
                        <p>🩺 Services: {', '.join(facility['services'])}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.button(f"📞 Call", key=f"call_{facility['name']}", use_container_width=True)
                with col2:
                    st.button(f"📍 Directions", key=f"dir_{facility['name']}", use_container_width=True)

# 💕 MOBILE ENCOURAGEMENT PAGE
def show_mobile_encouragement():
    st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <button onclick="window.history.back()" style="background: none; border: none; font-size: 1.5rem; margin-right: 1rem;">←</button>
            <h1 style="margin: 0;">💕 Support Community</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Encouragement messages
    messages = [
        {"text": "You are stronger than you know! Every step matters. 💪", "author": "Sarah"},
        {"text": "Your health journey is unique and beautiful. Keep going! 🌸", "author": "Dr. Elena"},
        {"text": "Remember: You've survived 100% of your hard days so far! 🌟", "author": "Hope Warrior"}
    ]
    
    for msg in messages:
        st.markdown(f"""
            <div class="mobile-card">
                <p>"{msg['text']}"</p>
                <small>— {msg['author']}</small>
            </div>
        """, unsafe_allow_html=True)
    
    # Add your message
    st.markdown("### 💌 Share Hope")
    user_message = st.text_area("Your encouraging message...", height=100)
    
    if st.button("Share Your Light ✨", use_container_width=True):
        if user_message.strip():
            st.success("Thank you for sharing your light with our community! 💖")
        else:
            st.warning("Please write a message to share")
    
    # Daily affirmation
    st.markdown("""
        <div class="mobile-card">
            <h3>💫 Today's Affirmation</h3>
            <p style="font-style: italic; font-size: 1.1rem;">
                "I honor my body with compassion and care. I am worthy of health and happiness."
            </p>
        </div>
    """, unsafe_allow_html=True)

# 📱 MOBILE NAVIGATION
def mobile_navigation():
    st.markdown("""
        <div class="mobile-nav">
            <button class="nav-btn {}" onclick="setPage('home')">🏠</button>
            <button class="nav-btn {}" onclick="setPage('chat')">💬</button>
            <button class="nav-btn {}" onclick="setPage('self_exam')">🤗</button>
            <button class="nav-btn {}" onclick="setPage('hospitals')">🏥</button>
            <button class="nav-btn {}" onclick="setPage('encouragement')">💕</button>
        </div>
        
        <script>
        function setPage(page) {
            window.location.href = window.location.pathname + '?page=' + page;
        }
        
        // Handle back button
        window.onpopstate = function(event) {
            window.location.reload();
        };
        </script>
    """.format(
        "active" if st.session_state.get('current_page') == 'home' else "",
        "active" if st.session_state.get('current_page') == 'chat' else "",
        "active" if st.session_state.get('current_page') == 'self_exam' else "",
        "active" if st.session_state.get('current_page') == 'hospitals' else "",
        "active" if st.session_state.get('current_page') == 'encouragement' else ""
    ), unsafe_allow_html=True)

# 🚀 MAIN APP
def main():
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    
    # Handle page navigation from URL parameters
    query_params = st.experimental_get_query_params()
    if 'page' in query_params:
        st.session_state.current_page = query_params['page'][0]
    
    # Show current page
    if st.session_state.current_page == 'home':
        show_mobile_home()
    elif st.session_state.current_page == 'chat':
        show_mobile_chat()
    elif st.session_state.current_page == 'self_exam':
        show_mobile_self_exam()
    elif st.session_state.current_page == 'hospitals':
        show_mobile_hospitals()
    elif st.session_state.current_page == 'encouragement':
        show_mobile_encouragement()
    
    # Show mobile navigation (except on home page)
    if st.session_state.current_page != 'home':
        mobile_navigation()

if __name__ == "__main__":
    main()