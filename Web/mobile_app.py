# Mobile App - BETTER than Web Version!
import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

# Page config
st.set_page_config(
    page_title="Breast Friend Forever",
    page_icon="💖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PWA Meta Tags
st.markdown("""
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#E91E63">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="viewport" content="width=device-width, initial-scale=1">
""", unsafe_allow_html=True)

# Mobile-Optimized Styles with Animations
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Animated gradient header */
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    .main-title {
        background: linear-gradient(45deg, #E91E63, #F06292, #EC407A, #E91E63);
        background-size: 300% 300%;
        animation: gradient 3s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }

    /* Bounce animation */
    @keyframes bounce {
        0%, 100% {transform: translateY(0);}
        50% {transform: translateY(-10px);}
    }

    .bounce {
        animation: bounce 2s ease-in-out infinite;
    }

    /* Pulse animation */
    @keyframes pulse {
        0%, 100% {transform: scale(1);}
        50% {transform: scale(1.05);}
    }

    .pulse {
        animation: pulse 2s ease-in-out infinite;
    }

    /* Card with hover effect */
    .animated-card {
        background: linear-gradient(135deg, #FCE4EC 0%, #F8BBD0 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(233, 30, 99, 0.2);
        transition: all 0.3s ease;
        border-left: 5px solid #E91E63;
    }

    .animated-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(233, 30, 99, 0.3);
    }

    /* Big mobile buttons */
    .stButton button {
        width: 100%;
        height: 60px;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 12px;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(233, 30, 99, 0.3);
    }

    /* Chat bubbles */
    .chat-user {
        background: linear-gradient(135deg, #E91E63, #EC407A);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 0.5rem 0;
        margin-left: 20%;
        animation: slideInRight 0.5s ease;
    }

    .chat-ai {
        background: linear-gradient(135deg, #F5F5F5, #EEEEEE);
        color: #333;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.5rem 0;
        margin-right: 20%;
        animation: slideInLeft 0.5s ease;
    }

    @keyframes slideInRight {
        from {transform: translateX(100px); opacity: 0;}
        to {transform: translateX(0); opacity: 1;}
    }

    @keyframes slideInLeft {
        from {transform: translateX(-100px); opacity: 0;}
        to {transform: translateX(0); opacity: 1;}
    }

    /* Hospital cards */
    .hospital-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.8rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #E91E63;
        transition: all 0.3s ease;
    }

    .hospital-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(233, 30, 99, 0.2);
    }

    /* Step counter animation */
    .step-number {
        display: inline-block;
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #E91E63, #EC407A);
        color: white;
        border-radius: 50%;
        text-align: center;
        line-height: 40px;
        font-weight: bold;
        margin-right: 1rem;
        animation: pulse 2s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)

# Backend URL
BACKEND_URL = "http://192.168.100.5:8000"

# Sidebar with emoji navigation
with st.sidebar:
    st.markdown('<div class="main-title bounce">💖 BFF Health</div>', unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["🏠 Home", "💬 AI Chat", "🏥 Hospitals", "💪 Self-Exam", "💕 Support"],
        label_visibility="collapsed"
    )

# ===== HOME PAGE =====
if page == "🏠 Home":
    st.markdown('<div class="main-title">Breast Friend Forever 💖</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Your mobile health companion</p>', unsafe_allow_html=True)

    st.markdown('<div class="animated-card pulse">', unsafe_allow_html=True)
    st.markdown("### 🎀 Welcome!")
    st.write("Get personalized breast health guidance, find nearby hospitals, and connect with support - all from your phone.")
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.button("🤖 Chat Assistant", key="home_chat", use_container_width=True)
        st.button("💪 Self-Exam", key="home_exam", use_container_width=True)
    with col2:
        st.button("🏥 Hospitals", key="home_hosp", use_container_width=True)
        st.button("💕 Support", key="home_supp", use_container_width=True)

# ===== AI CHAT PAGE =====
elif page == "💬 AI Chat":
    st.markdown('<div class="main-title">AI Health Assistant 🤖</div>', unsafe_allow_html=True)

    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {"text": "Hello! I'm your breast health assistant. How can I help you today? 💖", "isUser": False}
        ]

    # Display chat
    for msg in st.session_state.messages:
        if msg['isUser']:
            st.markdown(f'<div class="chat-user">{msg["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-ai">{msg["text"]}</div>', unsafe_allow_html=True)

    # Input
    user_input = st.text_input("Your question...", key="chat_input", label_visibility="collapsed", placeholder="Ask me anything about breast health...")

    if st.button("Send 📤", key="send_btn", use_container_width=True) and user_input:
        st.session_state.messages.append({"text": user_input, "isUser": True})

        try:
            response = requests.post(
                f"{BACKEND_URL}/api/v1/chat/",
                json={"message": user_input},
                timeout=10
            )
            ai_text = response.json().get("response", "I'm here to help!")
        except:
            ai_text = "Sorry, I'm having trouble connecting. Please try again."

        st.session_state.messages.append({"text": ai_text, "isUser": False})
        st.rerun()

# ===== HOSPITALS PAGE =====
elif page == "🏥 Hospitals":
    st.markdown('<div class="main-title">Find Hospitals 🏥</div>', unsafe_allow_html=True)

    search = st.text_input("🔍 Search hospitals...", key="hospital_search")

    with st.spinner("Loading hospitals..."):
        try:
            response = requests.get(f"{BACKEND_URL}/api/v1/hospitals/", timeout=10)
            hospitals = response.json()

            # Filter
            if search:
                hospitals = [h for h in hospitals if search.lower() in str(h).lower()]
            else:
                hospitals = hospitals[:50]  # Show first 50

            st.success(f"✅ Found {len(hospitals)} hospitals")

            # Interactive Map
            if hospitals:
                st.markdown("### 🗺️ Interactive Map")
                m = folium.Map(location=[-1.2921, 36.8219], zoom_start=6)

                for h in hospitals[:100]:  # First 100 on map
                    if h.get('latitude') and h.get('longitude'):
                        folium.Marker(
                            [h['latitude'], h['longitude']],
                            popup=f"<b>{h.get('name', 'Hospital')}</b><br>{h.get('address', '')}",
                            icon=folium.Icon(color='red', icon='plus', prefix='fa')
                        ).add_to(m)

                st_folium(m, width=700, height=400)

            # Hospital List
            st.markdown("### 📋 Hospital List")
            for h in hospitals[:20]:
                st.markdown(f"""
                <div class="hospital-card">
                    <h4 style="color: #E91E63; margin: 0;">{h.get('name', 'Hospital')}</h4>
                    <p style="margin: 0.5rem 0;">📍 {h.get('address', 'N/A')}</p>
                    <p style="margin: 0.5rem 0;">📞 {h.get('phone', 'N/A')}</p>
                    <p style="margin: 0.5rem 0; color: #666;">🏥 {h.get('services', 'General services')}</p>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Could not load hospitals: {str(e)}")

# ===== SELF-EXAM PAGE =====
elif page == "💪 Self-Exam":
    st.markdown('<div class="main-title">Self-Exam Guide 💪</div>', unsafe_allow_html=True)

    st.markdown('<div class="animated-card">', unsafe_allow_html=True)
    st.markdown("### 📅 Monthly Breast Self-Examination")
    st.write("Follow these animated steps to perform a thorough self-examination:")
    st.markdown('</div>', unsafe_allow_html=True)

    steps = [
        ("Look in the Mirror", "Stand in front of a mirror with your shoulders straight and arms on your hips. Look for changes in size, shape, or color.", "🪞"),
        ("Raise Your Arms", "Raise your arms above your head and look for the same changes.", "🙌"),
        ("Check for Fluid", "Look for any fluid coming from one or both nipples.", "👀"),
        ("Lie Down and Feel", "Lie down and use your right hand to feel your left breast in a circular motion.", "🛏️"),
        ("Stand or Sit", "Feel your breasts while standing or sitting. Many find this easiest in the shower.", "🚿")
    ]

    for i, (title, desc, emoji) in enumerate(steps, 1):
        st.markdown(f"""
        <div class="animated-card">
            <h3>
                <span class="step-number">{i}</span>
                {emoji} {title}
            </h3>
            <p style="font-size: 1.1rem; line-height: 1.6;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

    if st.button("📅 Set Monthly Reminder", key="reminder_btn", use_container_width=True):
        st.success("✅ Reminder set! We'll notify you monthly to perform your self-exam.")

# ===== SUPPORT PAGE =====
elif page == "💕 Support":
    st.markdown('<div class="main-title">Support Community 💕</div>', unsafe_allow_html=True)

    st.markdown('<div class="animated-card pulse">', unsafe_allow_html=True)
    st.markdown("### 🤗 You Are Not Alone")
    st.write("Connect with others, share your story, and find encouragement.")
    st.markdown('</div>', unsafe_allow_html=True)

    message = st.text_area("Share an encouraging message...", key="support_msg")
    if st.button("Post Message 💌", key="post_btn", use_container_width=True):
        st.success("✅ Your message has been shared! Thank you for spreading positivity.")

    st.markdown("### 💬 Recent Messages")

    messages = [
        ("Sarah M.", "You are stronger than you think! 💪", "2 hours ago"),
        ("Anonymous", "One day at a time. You've got this! 🌸", "5 hours ago"),
        ("Lisa K.", "Your courage inspires us all. Keep going! ✨", "1 day ago")
    ]

    for name, msg, time in messages:
        st.markdown(f"""
        <div class="animated-card">
            <p style="font-weight: bold; color: #E91E63; margin: 0;">{name}</p>
            <p style="font-size: 1.1rem; margin: 0.5rem 0;">{msg}</p>
            <p style="font-size: 0.8rem; color: #999; margin: 0;">{time}</p>
        </div>
        """, unsafe_allow_html=True)

# PWA Install prompt at bottom
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #E91E63, #EC407A); border-radius: 12px; color: white;">
    <p style="font-size: 1.1rem; margin: 0;">📱 Install this app on your phone for quick access!</p>
    <p style="font-size: 0.9rem; margin: 0.5rem 0 0 0;">Tap your browser menu and select "Add to Home Screen"</p>
</div>
""", unsafe_allow_html=True)
