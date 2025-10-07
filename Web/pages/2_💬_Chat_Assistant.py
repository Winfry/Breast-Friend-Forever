import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(page_title="Chat Assistant", page_icon="💬")

# 💬 Chat Initialization Function
def initialize_chat():
    """Sets up the chat session if it doesn't exist"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "Hello! I'm your breast health companion. I'm here to provide caring, accurate information about breast health. What would you like to know? 💖"
            }
        ]
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = f"streamlit_{datetime.now().timestamp()}"

# 📤 Send Message Function  
def send_message():
    """Handles sending messages to the backend API"""
    user_input = st.session_state.user_input
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        try:
            # Call backend API
            response = requests.post(
                "http://localhost:8000/api/v1/chat/message",
                json={
                    "message": user_input,
                    "conversation_id": st.session_state.conversation_id
                }
            )
            ai_response = response.json()["response"]
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        except:
            # Fallback if API fails
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "I'm here to help! Please try again or check your connection. 💕"
            })
        
        # Clear the input field
        st.session_state.user_input = ""

# 🚀 Initialize Chat Session
initialize_chat()

# 🎨 Chat Interface
st.markdown("# 💬 Breast Health Companion")
st.caption("Ask me anything about breast health - I'm here to help! 🌸")

# 💭 Display Chat Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ⌨️ Message Input
st.text_input(
    "Type your message...", 
    key="user_input",
    on_change=send_message,
    placeholder="Ask about self-exams, symptoms, or anything else..."
)

# 💡 Suggested Questions
st.markdown("### 💡 Suggested Questions")
suggestions = [
    "How do I perform a proper breast self-exam?",
    "What are the early signs of breast cancer?", 
    "When should I get my first mammogram?",
    "What lifestyle changes can reduce my risk?"
]

# 🎯 Display suggestions in columns
cols = st.columns(2)
for i, suggestion in enumerate(suggestions):
    with cols[i % 2]:
        if st.button(suggestion, key=f"sugg_{i}"):
            st.session_state.user_input = suggestion
            st.rerun()