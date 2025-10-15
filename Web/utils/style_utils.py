# Web/utils/style_utils.py
import streamlit as st

def set_page_config():
    st.set_page_config(
        page_title="Breast Friend Forever",
        page_icon="💖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def apply_custom_styles():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #e75480;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #e75480;
    }
    .chat-message-user {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .chat-message-bot {
        background-color: #e75480;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)