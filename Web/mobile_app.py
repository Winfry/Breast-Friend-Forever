# Mobile-Only Streamlit App - Simplified and Better!
import streamlit as st
import streamlit.components.v1 as components
import requests

# Configure page for mobile
st.set_page_config(
    page_title="Breast Friend Forever",
    page_icon="💖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Mobile-First Styles
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Full width on mobile */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 5rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }

    /* Mobile-optimized headers */
    h1 {
        font-size: 1.8rem !important;
        text-align: center;
        color: #E91E63;
    }

    /* Large touch-friendly buttons */
    .stButton button {
        width: 100%;
        height: 60px;
        font-size: 1.2rem;
        border-radius: 12px;
        font-weight: bold;
    }

    /* Bottom Navigation Bar */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        border-top: 1px solid #E0E0E0;
        display: flex;
        justify-content: space-around;
        padding: 0.5rem 0;
        z-index: 999;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
    }

    .nav-item {
        text-align: center;
        padding: 0.5rem;
        cursor: pointer;
        flex: 1;
        color: #666;
        text-decoration: none;
    }

    .nav-item.active {
        color: #E91E63;
    }

    .nav-icon {
        font-size: 1.5rem;
        display: block;
    }

    .nav-label {
        font-size: 0.7rem;
        margin-top: 0.2rem;
    }

    /* Card styles */
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    .card-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #E91E63;
        margin-bottom: 1rem;
    }

    /* Chat bubbles */
    .chat-bubble {
        padding: 1rem;
        border-radius: 18px;
        margin: 0.5rem 0;
        max-width: 85%;
    }

    .chat-user {
        background: #E91E63;
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }

    .chat-ai {
        background: #F0F0F0;
        color: #333;
        margin-right: auto;
        border-bottom-left-radius: 4px;
    }

    /* Input field */
    .stTextInput input {
        border-radius: 25px;
        padding: 0.8rem 1.2rem;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Backend URL
BACKEND_URL = "http://192.168.100.5:8000"

# === HOME PAGE ===
def show_home():
    st.markdown("# Breast Friend Forever 💖")
    st.markdown("### Your mobile health companion")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### Welcome! 👋")
    st.write("Get personalized breast health guidance, find nearby hospitals, and connect with support - all from your phone.")
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🤖 Chat Assistant", use_container_width=True):
            st.session_state.page = 'chat'
            st.rerun()
    with col2:
        if st.button("🏥 Find Hospitals", use_container_width=True):
            st.session_state.page = 'hospitals'
            st.rerun()

    col3, col4 = st.columns(2)
    with col3:
        if st.button("💪 Self-Exam Guide", use_container_width=True):
            st.session_state.page = 'exam'
            st.rerun()
    with col4:
        if st.button("💕 Support", use_container_width=True):
            st.session_state.page = 'support'
            st.rerun()

# === CHAT PAGE ===
def show_chat():
    st.markdown("# AI Chat Assistant 🤖")

    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if msg['isUser']:
                st.markdown(f'<div class="chat-bubble chat-user">{msg["text"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bubble chat-ai">{msg["text"]}</div>', unsafe_allow_html=True)

    # Input area
    user_input = st.text_input("Type your question...", key="chat_input", label_visibility="collapsed")

    col1, col2 = st.columns([4, 1])
    with col2:
        send_clicked = st.button("Send", use_container_width=True)

    if send_clicked and user_input:
        # Add user message
        st.session_state.messages.append({"text": user_input, "isUser": True})

        # Call backend
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/v1/chat/",
                json={"message": user_input},
                timeout=10
            )
            ai_response = response.json().get("response", "I'm here to help!")
        except Exception as e:
            ai_response = "Sorry, I'm having trouble connecting. Please try again."

        # Add AI message
        st.session_state.messages.append({"text": ai_response, "isUser": False})
        st.rerun()

# === HOSPITALS PAGE ===
def show_hospitals():
    st.markdown("# Find Hospitals 🏥")

    with st.spinner("Loading hospitals..."):
        try:
            response = requests.get(f"{BACKEND_URL}/api/v1/hospitals/", timeout=10)
            hospitals = response.json()

            st.success(f"Found {len(hospitals)} hospitals")

            # Filters
            search = st.text_input("🔍 Search by name or location", "")

            # Filter hospitals
            filtered = [h for h in hospitals if search.lower() in str(h).lower()] if search else hospitals[:20]

            # Display hospitals
            for hospital in filtered:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(f'<div class="card-header">{hospital.get("name", "Hospital")}</div>', unsafe_allow_html=True)
                st.write(f"📍 {hospital.get('address', 'N/A')}")
                st.write(f"📞 {hospital.get('phone', 'N/A')}")
                if hospital.get('services'):
                    st.write(f"🏥 {hospital['services']}")
                st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error("Could not load hospitals. Please check your connection.")

# === SELF EXAM PAGE ===
def show_exam():
    st.markdown("# Self-Exam Guide 💪")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">How to Perform a Self-Exam</div>', unsafe_allow_html=True)

    steps = [
        ("Look in the Mirror", "Stand in front of a mirror with your shoulders straight and arms on your hips. Look for changes in size, shape, or color."),
        ("Raise Your Arms", "Raise your arms above your head and look for the same changes."),
        ("Check for Fluid", "Look for any fluid coming from one or both nipples."),
        ("Lie Down and Feel", "Lie down and use your right hand to feel your left breast in a circular motion. Use your left hand for your right breast."),
        ("Stand or Sit", "Finally, feel your breasts while standing or sitting. Many women find this easiest in the shower.")
    ]

    for i, (title, desc) in enumerate(steps, 1):
        st.markdown(f"### Step {i}: {title}")
        st.write(desc)
        st.write("")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("📅 Set Monthly Reminder"):
        st.success("Reminder set! We'll notify you monthly.")

# === SUPPORT PAGE ===
def show_support():
    st.markdown("# Support Community 💕")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">You Are Not Alone</div>', unsafe_allow_html=True)
    st.write("Connect with others, share your story, and find encouragement.")
    st.markdown('</div>', unsafe_allow_html=True)

    message = st.text_area("Share an encouraging message...")
    if st.button("Post Message", use_container_width=True):
        st.success("Your message has been shared! Thank you for spreading positivity.")

    st.markdown("---")
    st.markdown("### Recent Messages")

    messages = [
        "You are stronger than you think! 💪",
        "One day at a time. You've got this! 🌸",
        "Your courage inspires us all. Keep going! ✨"
    ]

    for msg in messages:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write(msg)
        st.markdown('</div>', unsafe_allow_html=True)

# === BOTTOM NAVIGATION ===
def show_bottom_nav():
    components.html(f"""
    <div class="bottom-nav">
        <a href="?page=home" class="nav-item {'active' if st.session_state.page == 'home' else ''}">
            <div class="nav-icon">🏠</div>
            <div class="nav-label">Home</div>
        </a>
        <a href="?page=chat" class="nav-item {'active' if st.session_state.page == 'chat' else ''}">
            <div class="nav-icon">💬</div>
            <div class="nav-label">Chat</div>
        </a>
        <a href="?page=hospitals" class="nav-item {'active' if st.session_state.page == 'hospitals' else ''}">
            <div class="nav-icon">🏥</div>
            <div class="nav-label">Hospitals</div>
        </a>
        <a href="?page=support" class="nav-item {'active' if st.session_state.page == 'support' else ''}">
            <div class="nav-icon">💕</div>
            <div class="nav-label">Support</div>
        </a>
    </div>

    <script>
    // Handle navigation clicks
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const page = new URL(item.href).searchParams.get('page');
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: page}, '*');
        });
    });
    </script>
    """, height=80)

# === MAIN APP ROUTING ===
query_params = st.query_params
if 'page' in query_params:
    st.session_state.page = query_params['page']

# Show current page
if st.session_state.page == 'home':
    show_home()
elif st.session_state.page == 'chat':
    show_chat()
elif st.session_state.page == 'hospitals':
    show_hospitals()
elif st.session_state.page == 'exam':
    show_exam()
elif st.session_state.page == 'support':
    show_support()

# Always show bottom navigation
show_bottom_nav()
