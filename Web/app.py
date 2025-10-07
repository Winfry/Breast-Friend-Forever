import streamlit as st
from utils.style_utils import apply_custom_style

# 🎨 Apply our beautiful pink theme
apply_custom_style()

# ⚙️ Page configuration
st.set_page_config(
    page_title="Breast Friend Forever 💖",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🏠 Main landing page
st.markdown("""
<div style="text-align: center; padding: 3rem 1rem; background: linear-gradient(135deg, #FF69B4, #FFB6C1); border-radius: 20px; margin: 1rem 0;">
    <h1 style="color: white; font-size: 3.5rem; margin-bottom: 0.5rem;">💖 Breast Friend Forever</h1>
    <p style="color: white; font-size: 1.5rem; margin-top: 0;">Your compassionate breast health companion</p>
</div>
""", unsafe_allow_html=True)

# 📊 Quick stats row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Self-Exams Guided", "1,234+")
with col2:
    st.metric("Questions Answered", "5,678+")
with col3:
    st.metric("Resources Shared", "890+")
with col4:
    st.metric("Support Messages", "2,345+")

# 🎯 Feature cards
st.markdown("## 🌸 How We Can Help You Today")

# First row of features
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; border-radius: 15px; background: #FFF0F5; margin: 0.5rem; border: 2px solid #FFB6C1;">
        <div style="font-size: 3rem;">🖐️</div>
        <h3 style="color: #FF69B4;">Self Exam Guide</h3>
        <p>Step-by-step guidance for breast self-examination in the comfort of your home</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start Self Exam", key="exam_btn", use_container_width=True):
        st.switch_page("pages/1_🤗_Self_Exam.py")

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; border-radius: 15px; background: #FFF0F5; margin: 0.5rem; border: 2px solid #FFB6C1;">
        <div style="font-size: 3rem;">💬</div>
        <h3 style="color: #FF69B4;">Chat Assistant</h3>
        <p>Ask questions about breast health anonymously with our AI companion</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Chat Now", key="chat_btn", use_container_width=True):
        st.switch_page("pages/2_💬_Chat_Assistant.py")

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; border-radius: 15px; background: #FFF0F5; margin: 0.5rem; border: 2px solid #FFB6C1;">
        <div style="font-size: 3rem;">📚</div>
        <h3 style="color: #FF69B4;">Resources</h3>
        <p>Educational articles, PDF guides, and trusted external resources</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Learn More", key="resources_btn", use_container_width=True):
        st.switch_page("pages/3_📚_Resources.py")

# Second row of features
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; border-radius: 15px; background: #FFF0F5; margin: 0.5rem; border: 2px solid #FFB6C1;">
        <div style="font-size: 3rem;">🏥</div>
        <h3 style="color: #FF69B4;">Find Screening</h3>
        <p>Locate breast cancer screening centers and healthcare facilities near you</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Find Locations", key="screening_btn", use_container_width=True):
        st.switch_page("pages/4_🏥_Find_Screening.py")

with col5:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; border-radius: 15px; background: #FFF0F5; margin: 0.5rem; border: 2px solid #FFB6C1;">
        <div style="font-size: 3rem;">💕</div>
        <h3 style="color: #FF69B4;">Encouragement Wall</h3>
        <p>Share and read supportive messages from our caring community</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Share Hope", key="encouragement_btn", use_container_width=True):
        st.switch_page("pages/5_💕_Encouragement_Wall.py")

# 💫 Welcome message
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 3rem 1rem;">
    <h2 style="color: #FF69B4;">Welcome to Your Breast Health Journey 🌸</h2>
    <p style="font-size: 1.2rem; line-height: 1.6; max-width: 800px; margin: 0 auto;">
        We're here to provide <strong>compassionate, accurate information</strong> about breast health in a 
        <strong>safe, anonymous space</strong>. Whether you're learning about self-examination, have questions 
        about breast health, or need emotional support, we're with you every step of the way.
    </p>
    <p style="font-style: italic; color: #666; margin-top: 1rem;">
        Remember: You're not alone, and taking care of your health is an act of self-love. 💖
    </p>
</div>
""", unsafe_allow_html=True)

# 🔒 Privacy note
st.markdown("---")
st.info("""
**🔒 Your Privacy Matters:** All interactions are anonymous. We don't store personal information, 
and your conversations are private. This app is for educational purposes and doesn't replace 
professional medical advice.
""")