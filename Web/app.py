import streamlit as st

# 🎨 Page Configuration - Sets up the browser tab
st.set_page_config(
    page_title="Breast Friend Forever",
    page_icon="💖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 💅 Custom CSS Styling - Makes it pretty and pink!
st.markdown("""
    <style>
    .main {
        background-color: #FFFFFF;
    }
    .stButton button {
        background-color: #FF69B4;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 500;
    }
    .stButton button:hover {
        background-color: #FF1493;
        color: white;
    }
    h1, h2, h3 {
        color: #FF69B4;
    }
    </style>
    """, unsafe_allow_html=True)

# 🏠 Main Landing Page Content
st.title("💖 Breast Friend Forever")
st.subheader("Your compassionate breast health companion")

st.markdown("---")

# 🎯 Feature Cards - Like a dashboard with 5 main options
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🖐️ Self-Exam Guide")
    st.write("Step-by-step guidance for breast self-examination")
    if st.button("Start Self-Exam", key="exam"):
        st.switch_page("pages/1_🤗_Self_Exam.py")

with col2:
    st.markdown("### 💬 Chat Assistant")
    st.write("Ask questions about breast health anonymously")
    if st.button("Chat Now", key="chat"):
        st.switch_page("pages/2_💬_Chat_Assistant.py")

with col3:
    st.markdown("### 📚 Resources")
    st.write("Educational articles and information")
    if st.button("Learn More", key="resources"):
        st.switch_page("pages/3_📚_Resources.py")

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("### 🏥 Find Screening")
    st.write("Locate breast cancer screening centers")
    if st.button("Find Locations", key="screening"):
        st.switch_page("pages/4_🏥_Find_Screening.py")

with col5:
    st.markdown("### 💕 Encouragement Wall")
    st.write("Share and read supportive messages")
    if st.button("Share Hope", key="encouragement"):
        st.switch_page("pages/5_💕_Encouragement_Wall.py")

st.markdown("---")

# 🌸 Welcome Message - Sets compassionate tone
st.markdown("""
    ### 🌸 Welcome to Your Breast Health Journey

    We're here to provide compassionate, accurate information about breast health in a safe, anonymous space.

    **Remember:** You're not alone, and taking care of your health is an act of self-love.
""")