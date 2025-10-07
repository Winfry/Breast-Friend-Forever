import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Encouragement Wall", page_icon="💕")

st.markdown("# 💕 Encouragement Wall")
st.caption("A safe space to share hope, strength, and support")

# 💌 Sample Messages (in real app, from backend)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "id": 1,
            "message": "You are stronger than you think, and you're not alone in this journey. 💖",
            "type": "💖 General Support", 
            "author": "Anonymous Friend",
            "timestamp": "2024-01-15T10:30:00"
        },
        {
            "id": 2,
            "message": "Regular self-checks gave me peace of mind. You've got this! 🌟",
            "type": "🌟 Personal Story",
            "author": "Anonymous Friend", 
            "timestamp": "2024-01-14T15:45:00"
        }
    ]

# ✨ Message Submission Form
st.markdown("### ✨ Share Your Message of Hope")
with st.form("encouragement_form"):
    message = st.text_area(
        "Your message of encouragement",
        placeholder="Share a positive thought, personal experience, or words of support...",
        height=100
    )
    message_type = st.selectbox(
        "Message type",
        ["💖 General Support", "🌟 Personal Story", "💪 Strength", "🤗 Comfort", "🎉 Celebration"]
    )
    submitted = st.form_submit_button("Post Message 💫")
    
    if submitted and message.strip():
        # Create new message
        new_message = {
            "id": len(st.session_state.messages) + 1,
            "message": message,
            "type": message_type, 
            "author": "Anonymous Friend",
            "timestamp": datetime.now().isoformat()
        }
        
        # Add to messages and show success
        st.session_state.messages.insert(0, new_message)
        st.success("Thank you for sharing your message of hope! 💖")
        st.rerun()

# 🌈 Display Community Messages
st.markdown("### 🌈 Messages from Our Community")
for message in st.session_state.messages:
    # Different background colors based on message type
    bg_color = "#FFF0F5"
    
    st.markdown(f"""
    <div style="background-color: {bg_color}; padding: 1.5rem; border-radius: 15px; margin: 1rem 0; border-left: 5px solid #FF69B4;">
        <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 0.5rem;">
            <span style="font-weight: bold; color: #FF69B4;">{message['type']}</span>
            <span style="font-size: 0.8rem; color: #666;">{message['timestamp'].split('T')[0]}</span>
        </div>
        <p style="margin: 0; font-size: 1.1rem; line-height: 1.5;">{message['message']}</p>
        <div style="text-align: right; margin-top: 0.5rem;">
            <span style="font-style: italic; color: #888;">- {message['author']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 💫 Inspiration Section
st.markdown("---")
st.info("**💫 Today's Inspiration:** Your strength is greater than any challenge.")

# 📊 Community Statistics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Messages Shared", len(st.session_state.messages))
with col2:
    st.metric("Support Types", 5)
with col3:
    st.metric("Community Impact", "Growing 💖")