import streamlit as st
from streamlit_lottie import st_lottie
import json

# Function to load Lottie animation
def load_lottie_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

st.set_page_config(
    page_title="Breast Friend Forever",
    page_icon="💖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Lottie animations for the main page
lottie_heart = load_lottie_json("assets/animations/heart-beat.json")
lottie_chat = load_lottie_json("assets/animations/chat-bubble.json")
lottie_book = load_lottie_json("assets/animations/book-open.json")
lottie_location = load_lottie_json("assets/animations/location-pin.json")
lottie_community = load_lottie_json("assets/animations/community.json")

# ... rest of the CSS and setup

st.title("💖 Breast Friend Forever")
st.subheader("Your compassionate breast health companion")

st.markdown("---")

# Feature cards with Lottie animations
col1, col2, col3 = st.columns(3)

with col1:
    st_lottie(lottie_heart, speed=1, width=100, height=100)
    st.markdown("### 🖐️ Self-Exam Guide")
    st.write("Step-by-step guidance for breast self-examination")
    if st.button("Start Self-Exam", key="exam"):
        st.switch_page("pages/1_🤗_Self_Exam.py")

with col2:
    st_lottie(lottie_chat, speed=1, width=100, height=100)
    st.markdown("### 💬 Chat Assistant")
    st.write("Ask questions about breast health anonymously")
    if st.button("Chat Now", key="chat"):
        st.switch_page("pages/2_💬_Chat_Assistant.py")

with col3:
    st_lottie(lottie_book, speed=1, width=100, height=100)
    st.markdown("### 📚 Resources")
    st.write("Educational articles and information")
    if st.button("Learn More", key="resources"):
        st.switch_page("pages/3_📚_Resources.py")

col4, col5, col6 = st.columns(3)

with col4:
    st_lottie(lottie_location, speed=1, width=100, height=100)
    st.markdown("### 🏥 Find Screening")
    st.write("Locate breast cancer screening centers")
    if st.button("Find Locations", key="screening"):
        st.switch_page("pages/4_🏥_Find_Screening.py")

with col5:
    st_lottie(lottie_community, speed=1, width=100, height=100)
    st.markdown("### 💕 Encouragement Wall")
    st.write("Share and read supportive messages")
    if st.button("Share Hope", key="encouragement"):
        st.switch_page("pages/5_💕_Encouragement_Wall.py")

st.markdown("---")
st.markdown("© 2025 Breast Friend Forever. All rights reserved.")