# Web/utils/chat_utils.py
import streamlit as st
from utils.api_client import api_client

def initialize_chat_session():
    """Initialize chat session state"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = f"streamlit_{id(st.session_state)}"
    
    # Load greeting if first time
    if not st.session_state.chat_history:
        greeting = api_client.get_chat_greeting()
        st.session_state.chat_history.append({
            "role": "bot",
            "message": greeting.get("message", "Hello! How can I help you today? 💖"),
            "timestamp": "now"
        })
        st.session_state.suggested_questions = greeting.get("suggested_questions", [])

def display_chat_history():
    """Display chat conversation"""
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <strong>You:</strong> {chat["message"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bot-message">
                <strong>Breast Friend:</strong> {chat["message"]}
            </div>
            """, unsafe_allow_html=True)

def send_user_message(message):
    """Send user message and get bot response"""
    # Add user message to history
    st.session_state.chat_history.append({
        "role": "user",
        "message": message,
        "timestamp": "now"
    })
    
    # Get bot response
    response = api_client.send_chat_message(
        message, 
        st.session_state.conversation_id
    )
    
    # Add bot response to history
    st.session_state.chat_history.append({
        "role": "bot",
        "message": response.get("response", "I'm here to help! 💖"),
        "timestamp": "now"
    })