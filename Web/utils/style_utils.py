# Web/utils/style_utils.py
import streamlit as st

def apply_custom_styles():
    """Apply consistent pink theme styling"""
    st.markdown("""
    <style>
    /* Main pink theme */
    .main-header {
        font-size: 3rem;
        color: #e91e63;
        text-align: center;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 2rem;
        color: #e91e63;
        margin: 1rem 0;
    }
    .pink-card {
        background-color: #fce4ec;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #e91e63;
        margin: 1rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border: 1px solid #bbdefb;
    }
    .bot-message {
        background-color: #fce4ec;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border: 1px solid #f8bbd9;
    }
    .success-message {
        background-color: #e8f5e8;
        color: #2e7d32;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def setup_page_config():
    """Setup consistent page configuration"""
    st.set_page_config(
        page_title="Breast Friend Forever",
        page_icon="💖",
        layout="wide",
        initial_sidebar_state="expanded"
    )