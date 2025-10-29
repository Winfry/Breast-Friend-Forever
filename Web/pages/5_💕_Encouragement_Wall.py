import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
import json
import time
from datetime import datetime, timedelta
import random
import html

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

st.set_page_config(page_title="Encouragement Wall", page_icon="💕", layout="wide")

# 🎨 ENCOURAGEMENT ANIMATION CSS
st.markdown("""
    <style>
    @keyframes messageFloat {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        25% { transform: translateY(-10px) rotate(1deg); }
        50% { transform: translateY(-5px) rotate(-1deg); }
        75% { transform: translateY(-8px) rotate(0.5deg); }
    }
    
    @keyframes heartBeat {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    @keyframes sparkle {
        0%, 100% { opacity: 0; transform: scale(0); }
        50% { opacity: 1; transform: scale(1); }
    }
    
    .message-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 3px solid transparent;
        box-shadow: 0 8px 25px rgba(255, 182, 193, 0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: messageFloat 6s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }
    
    .message-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transition: left 0.6s;
    }
    
    .message-card:hover::before {
        left: 100%;
    }
    
    .message-card:hover {
        animation: messageFloat 3s ease-in-out infinite;
        box-shadow: 0 15px 35px rgba(255, 182, 193, 0.3);
    }
    
    .hope-message {
        border-color: #FF69B4;
        background: linear-gradient(135deg, #FFF0F5, #FFE4EC);
    }
    
    .strength-message {
        border-color: #EC4899;
        background: linear-gradient(135deg, #FFE4EC, #FCE7F3);
    }
    
    .love-message {
        border-color: #DB2777;
        background: linear-gradient(135deg, #FCE7F3, #FBCFE8);
    }
    
    .courage-message {
        border-color: #BE185D;
        background: linear-gradient(135deg, #FBCFE8, #F9A8D4);
    }
    
    .encouragement-btn {
        background: linear-gradient(135deg, #FF69B4, #EC4899);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .encouragement-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transition: left 0.5s;
    }
    
    .encouragement-btn:hover::before {
        left: 100%;
    }
    
    .encouragement-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(255, 105, 180, 0.4);
    }
    
    .community-wall {
        background: linear-gradient(135deg, #FFF0F5, #FFE4EC);
        border-radius: 25px;
        padding: 3rem;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .community-wall::before {
        content: '💖🌟✨';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        font-size: 4rem;
        opacity: 0.1;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .reaction-stats {
        display: flex;
        gap: 1rem;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .reaction-count {
        display: flex;
        align-items: center;
        gap: 0.3rem;
        font-weight: 600;
    }
    
    .user-avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #FF69B4, #EC4899);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 1.2rem;
        margin-right: 1rem;
    }
    
    .sparkle {
        position: absolute;
        font-size: 1.5rem;
        animation: sparkle 2s infinite;
    }
    
    .reaction-buttons-container {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    
    /* Fix for message display */
    .message-content {
        color: #374151;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
        font-style: italic;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    </style>
    """, unsafe_allow_html=True)

# Load animations
try:
    heart_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_5njp3vgg.json")
    community_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_5tt2Th.json")
    celebration_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_ukwacdcs.json")
except:
    heart_animation = community_animation = celebration_animation = None

# Initialize session state with real-time capabilities
if 'messages' not in st.session_state:
    # Sample encouraging messages
    st.session_state.messages = [
        {
            "id": 1,
            "user": "Sarah M.",
            "avatar": "SM",
            "message": "You are stronger than you know, braver than you believe, and more capable than you imagine. Every step forward counts! 💪",
            "timestamp": datetime.now() - timedelta(hours=2),
            "category": "strength",
            "reactions": {"hearts": 15, "sparks": 8, "rainbows": 12},
            "user_reactions": set()
        },
        {
            "id": 2,
            "user": "Dr. Elena Rodriguez",
            "avatar": "ER",
            "message": "As a healthcare provider, I see courage every day. Your commitment to your health is inspiring and powerful. Keep shining! 🌟",
            "timestamp": datetime.now() - timedelta(days=1),
            "category": "courage",
            "reactions": {"hearts": 23, "sparks": 15, "rainbows": 18},
            "user_reactions": set()
        },
        {
            "id": 3,
            "user": "Hope Warrior",
            "avatar": "HW",
            "message": "Remember: You've survived 100% of your hardest days so far. That's a perfect track record! You've got this! 💝",
            "timestamp": datetime.now() - timedelta(days=3),
            "category": "hope",
            "reactions": {"hearts": 34, "sparks": 22, "rainbows": 27},
            "user_reactions": set()
        },
        {
            "id": 4,
            "user": "Community Caregiver",
            "avatar": "CC",
            "message": "Your journey matters. Your feelings are valid. Your strength is seen. We're walking this path with you. 🤝",
            "timestamp": datetime.now() - timedelta(days=5),
            "category": "love",
            "reactions": {"hearts": 28, "sparks": 19, "rainbows": 24},
            "user_reactions": set()
        }
    ]

if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

# Function to handle reactions
def handle_reaction(message_id, reaction_type):
    for message in st.session_state.messages:
        if message["id"] == message_id:
            if reaction_type not in message["user_reactions"]:
                message["reactions"][reaction_type] += 1
                message["user_reactions"].add(reaction_type)
                st.session_state.last_update = datetime.now()
                return True
    return False

# Function to escape HTML and preserve emojis
# Function to escape HTML and preserve emojis - FIXED VERSION
def safe_message_display(text):
    """Escape HTML but preserve emojis and basic formatting"""
    if not text:
        return ""
    # First escape HTML to prevent XSS
    safe_text = html.escape(text)
    # Convert escaped quotes back to normal quotes for display
    safe_text = safe_text.replace('&quot;', '"').replace('&#x27;', "'")
    # Allow some safe HTML tags and emojis
    safe_text = safe_text.replace('&lt;br&gt;', '<br>')
    safe_text = safe_text.replace('&lt;b&gt;', '<b>').replace('&lt;/b&gt;', '</b>')
    safe_text = safe_text.replace('&lt;i&gt;', '<i>').replace('&lt;/i&gt;', '</i>')
    return safe_text

# 📝 DISPLAY ENCOURAGING MESSAGES - FIXED VERSION
st.markdown("### 📝 Wall of Hope & Strength")

# Sort and filter messages
display_messages = st.session_state.messages.copy()

if category_filter != "All Messages":
    display_messages = [msg for msg in display_messages if msg["category"] == category_filter.lower()]

if sort_by == "Newest First":
    display_messages.sort(key=lambda x: x["timestamp"], reverse=True)
elif sort_by == "Oldest First":
    display_messages.sort(key=lambda x: x["timestamp"])
elif sort_by == "Most Loved":
    display_messages.sort(key=lambda x: sum(x["reactions"].values()), reverse=True)

for message in display_messages:
    # Determine card style based on category
    category_styles = {
        "hope": "hope-message",
        "love": "love-message", 
        "strength": "strength-message",
        "courage": "courage-message",
        "inspiration": "hope-message",
        "support": "love-message",
        "celebration": "courage-message"
    }
    
    card_class = f"message-card {category_styles.get(message['category'], 'hope-message')}"
    
    # Time display
    time_diff = datetime.now() - message['timestamp']
    if time_diff.days > 0:
        time_display = f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
    elif time_diff.seconds // 3600 > 0:
        time_display = f"{time_diff.seconds // 3600} hour{'s' if time_diff.seconds // 3600 > 1 else ''} ago"
    else:
        time_display = "Just now"
    
    # Safe message display - FIXED
    safe_message = safe_message_display(message['message'])
    
    # Display message card using a cleaner approach - FIXED
    st.markdown(f"""
        <div class="{card_class}">
            <div style="display: flex; align-items: flex-start; margin-bottom: 1.5rem;">
                <div class="user-avatar">
                    {message['avatar']}
                </div>
                <div style="flex: 1;">
                    <h4 style="margin: 0 0 0.5rem 0; color: #1F2937;">{message['user']}</h4>
                    <p style="margin: 0; color: #6B7280; font-size: 0.9rem;">{time_display}</p>
                </div>
            </div>
            
            <div class="message-content">
                {safe_message}
            </div>
            
            <div class="reaction-stats">
                <div class="reaction-count" style="color: #EF4444;">
                    💖 {message['reactions']['hearts']}
                </div>
                <div class="reaction-count" style="color: #F59E0B;">
                    🌟 {message['reactions']['sparks']}
                </div>
                <div class="reaction-count" style="color: #8B5CF6;">
                    🌈 {message['reactions']['rainbows']}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Welcome animation
if heart_animation:
    st_lottie(heart_animation, speed=1, height=200, key="encouragement_welcome")

# 🌟 COMMUNITY WALL INTRODUCTION
st.markdown("""
    <div class="community-wall">
        <h2 style="color: #DB2777; text-align: center; margin-bottom: 1rem;">
            🌈 Welcome to Our Circle of Support
        </h2>
        <p style="color: #666; text-align: center; font-size: 1.1rem; line-height: 1.6;">
            This is your safe space to share hope, find strength, and connect with others who understand. 
            Every message here is a beacon of light for someone who needs it. ✨
        </p>
        <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 2rem;">
            <span style="animation: heartBeat 2s infinite;">💖</span>
            <span style="animation: heartBeat 2s infinite; animation-delay: 0.3s;">🌟</span>
            <span style="animation: heartBeat 2s infinite; animation-delay: 0.6s;">🤝</span>
            <span style="animation: heartBeat 2s infinite; animation-delay: 0.9s;">🌈</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 👤 USER INTRODUCTION
st.markdown("### 👋 Join Our Community")

col1, col2 = st.columns(2)

with col1:
    st.session_state.user_name = st.text_input(
        "What should we call you?",
        placeholder="Your name or nickname...",
        value=st.session_state.user_name
    )

with col2:
    user_mood = st.selectbox(
        "How are you feeling today?",
        ["✨ Choose your vibe...", "💪 Strong", "🤗 Hopeful", "🌱 Growing", "🌈 Grateful", "🌟 Inspired"],
        key="mood_encouragement"
    )

# 💌 SHARE ENCOURAGEMENT
st.markdown("### 💌 Share Your Light")

with st.form("encouragement_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        message_category = st.selectbox(
            "Message Type",
            ["💖 Hope & Love", "💪 Strength & Courage", "🌟 Inspiration", "🤝 Support", "🎉 Celebration"]
        )
    
    with col2:
        anonymity = st.checkbox("Share anonymously", value=True)
    
    user_message = st.text_area(
        "Your encouraging message...",
        placeholder="Share your words of hope, strength, or inspiration...",
        height=100
    )
    
    submitted = st.form_submit_button("✨ Share Your Light", use_container_width=True)
    
    if submitted and user_message.strip():
        if not st.session_state.user_name:
            st.warning("Please tell us what to call you first! 👆")
        else:
            # Add new message
            new_message = {
                "id": len(st.session_state.messages) + 1,
                "user": "Anonymous" if anonymity else st.session_state.user_name,
                "avatar": "AN" if anonymity else st.session_state.user_name[:2].upper(),
                "message": user_message,
                "timestamp": datetime.now(),
                "category": message_category.lower().split(" ")[1],
                "reactions": {"hearts": 0, "sparks": 0, "rainbows": 0},
                "user_reactions": set()
            }
            
            st.session_state.messages.insert(0, new_message)
            st.session_state.last_update = datetime.now()
            st.success("🎉 Your beautiful message has been added to the wall! Thank you for sharing your light. 💫")
            st.balloons()
            
            # Show celebration animation
            if celebration_animation:
                st_lottie(celebration_animation, speed=1, height=200, key="celebration")
            time.sleep(2)
            st.rerun()

# 🎯 MESSAGE FILTERS
st.markdown("### 🎯 Browse Encouragement")

filter_cols = st.columns(4)

with filter_cols[0]:
    sort_by = st.selectbox("Sort by", ["Newest First", "Most Loved", "Oldest First"])

with filter_cols[1]:
    category_filter = st.selectbox("Category", ["All Messages", "Hope", "Strength", "Love", "Courage", "Inspiration", "Support", "Celebration"])

with filter_cols[2]:
    show_community = st.checkbox("Show Community Messages", value=True)

with filter_cols[3]:
    if st.button("🔄 Refresh Wall", use_container_width=True):
        st.session_state.last_update = datetime.now()
        st.rerun()

# 📝 DISPLAY ENCOURAGING MESSAGES - FIXED VERSION
st.markdown("### 📝 Wall of Hope & Strength")

# Sort and filter messages
display_messages = st.session_state.messages.copy()

if category_filter != "All Messages":
    display_messages = [msg for msg in display_messages if msg["category"] == category_filter.lower()]

if sort_by == "Newest First":
    display_messages.sort(key=lambda x: x["timestamp"], reverse=True)
elif sort_by == "Oldest First":
    display_messages.sort(key=lambda x: x["timestamp"])
elif sort_by == "Most Loved":
    display_messages.sort(key=lambda x: sum(x["reactions"].values()), reverse=True)

for message in display_messages:
    # Determine card style based on category
    category_styles = {
        "hope": "hope-message",
        "love": "love-message", 
        "strength": "strength-message",
        "courage": "courage-message",
        "inspiration": "hope-message",
        "support": "love-message",
        "celebration": "courage-message"
    }
    
    card_class = f"message-card {category_styles.get(message['category'], 'hope-message')}"
    
    # Time display
    time_diff = datetime.now() - message['timestamp']
    if time_diff.days > 0:
        time_display = f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
    elif time_diff.seconds // 3600 > 0:
        time_display = f"{time_diff.seconds // 3600} hour{'s' if time_diff.seconds // 3600 > 1 else ''} ago"
    else:
        time_display = "Just now"
    
    # Safe message display
    safe_message = safe_message_display(message['message'])
    
    # Display message card using a cleaner approach
    st.markdown(f"""
        <div class="{card_class}">
            <div style="display: flex; align-items: flex-start; margin-bottom: 1.5rem;">
                <div class="user-avatar">
                    {message['avatar']}
                </div>
                <div style="flex: 1;">
                    <h4 style="margin: 0 0 0.5rem 0; color: #1F2937;">{message['user']}</h4>
                    <p style="margin: 0; color: #6B7280; font-size: 0.9rem;">{time_display}</p>
                </div>
            </div>
            
            <div class="message-content">
                "{safe_message}"
            </div>
            
            <div class="reaction-stats">
                <div class="reaction-count" style="color: #EF4444;">
                    💖 {message['reactions']['hearts']}
                </div>
                <div class="reaction-count" style="color: #F59E0B;">
                    🌟 {message['reactions']['sparks']}
                </div>
                <div class="reaction-count" style="color: #8B5CF6;">
                    🌈 {message['reactions']['rainbows']}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Reaction buttons using Streamlit components
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(f"💖 Send Love", key=f"heart_{message['id']}", use_container_width=True):
            if handle_reaction(message["id"], "hearts"):
                st.success("💖 Love sent! Your support means the world.")
                time.sleep(1)
                st.rerun()
            else:
                st.info("💖 You've already sent love to this message!")
    
    with col2:
        if st.button(f"🌟 Spark Joy", key=f"spark_{message['id']}", use_container_width=True):
            if handle_reaction(message["id"], "sparks"):
                st.success("🌟 Joy sparked! You're spreading positivity.")
                time.sleep(1)
                st.rerun()
            else:
                st.info("🌟 You've already sparked joy for this message!")
    
    with col3:
        if st.button(f"🌈 Rainbow Connection", key=f"rainbow_{message['id']}", use_container_width=True):
            if handle_reaction(message["id"], "rainbows"):
                st.success("🌈 Connection made! Your support creates beautiful ripples.")
                time.sleep(1)
                st.rerun()
            else:
                st.info("🌈 You've already connected with this message!")
    
    st.markdown("---")

# 🎨 INTERACTIVE ENCOURAGEMENT ACTIVITIES
st.markdown("### 🎨 Boost Your Spirits")

activity_cols = st.columns(3)

with activity_cols[0]:
    if st.button("🎯 Daily Affirmation", use_container_width=True):
        affirmations = [
            "I am strong, capable, and worthy of care!",
            "My health journey is unique and beautiful!",
            "I choose hope and healing today!",
            "I am surrounded by love and support!",
            "Every step I take matters!",
            "I honor my body with compassion!"
        ]
        st.info(f"**💫 {random.choice(affirmations)}**")

with activity_cols[1]:
    if st.button("🌈 Gratitude Moment", use_container_width=True):
        gratitude_prompts = [
            "What made you smile today?",
            "What strength did you discover in yourself recently?",
            "Who supported you this week?",
            "What progress have you made, no matter how small?",
            "What beauty did you notice around you?"
        ]
        st.info(f"**🤔 {random.choice(gratitude_prompts)}**")

with activity_cols[2]:
    if st.button("🌟 Inspire Others", use_container_width=True):
        st.info("**✨ Your story matters! Share your journey to inspire others.**")

# 📊 COMMUNITY STATISTICS
st.markdown("### 📊 Community Impact")

stats_data = {
    "total_messages": len(st.session_state.messages),
    "total_reactions": sum(sum(msg["reactions"].values()) for msg in st.session_state.messages),
    "active_users": len(set(msg["user"] for msg in st.session_state.messages)),
    "hope_messages": len([msg for msg in st.session_state.messages if msg["category"] == "hope"])
}

cols = st.columns(4)
for i, (key, value) in enumerate(stats_data.items()):
    with cols[i]:
        icons = ["💌", "💖", "👥", "🌟"]
        labels = ["Messages Shared", "Hearts Given", "Community Members", "Hope Moments"]
        st.markdown(f"""
            <div class="message-card" style="text-align: center; padding: 1.5rem;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">{icons[i]}</div>
                <h3 style="color: #FF69B4; margin: 0; font-size: 2rem;">{value}</h3>
                <p style="color: #666; margin: 0.5rem 0 0 0; font-weight: 500;">{labels[i]}</p>
            </div>
            """, unsafe_allow_html=True)

# 🎊 COMMUNITY CELEBRATION
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #FFE4EC, #FCE7F3); border-radius: 25px; margin: 2rem 0;">
        <h2 style="color: #DB2777; margin-bottom: 1rem;">🎉 You Are Never Alone</h2>
        <p style="color: #666; font-size: 1.1rem; line-height: 1.6;">
            Every message shared, every heart given, every moment of courage - 
            it all creates ripples of hope throughout our community. 
            <strong>You are part of something beautiful.</strong> 🌈
        </p>
        <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 2rem;">
            <span style="animation: messageFloat 4s ease-in-out infinite;">💝</span>
            <span style="animation: messageFloat 4s ease-in-out infinite; animation-delay: 0.5s;">🌟</span>
            <span style="animation: messageFloat 4s ease-in-out infinite; animation-delay: 1s;">🤗</span>
            <span style="animation: messageFloat 4s ease-in-out infinite; animation-delay: 1.5s;">🌈</span>
            <span style="animation: messageFloat 4s ease-in-out infinite; animation-delay: 2s;">✨</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Real-time status
st.sidebar.markdown("### 🔄 Live Updates")
st.sidebar.info(f"**Last update:** {st.session_state.last_update.strftime('%H:%M:%S')}")
st.sidebar.progress((datetime.now() - st.session_state.last_update).seconds / 30, text="Next refresh")

# Auto-refresh toggle
auto_refresh = st.sidebar.checkbox("🔄 Enable auto-refresh", value=True)
if auto_refresh:
    st.sidebar.write("Page refreshes every 30 seconds")
    time_since_update = (datetime.now() - st.session_state.last_update).seconds
    if time_since_update >= 30:
        st.session_state.last_update = datetime.now()
        st.rerun()

# 🎵 SECRET CELEBRATION ZONE
with st.expander("🎵 Community Celebration Zone"):
    st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h3 style="color: #FF69B4;">🎊 You Found Our Celebration Space! 🎊</h3>
            <p>Take a moment to celebrate being part of this amazing community!</p>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("🎉 Launch Community Celebration!"):
        st.balloons()
        st.snow()
        st.success("🎊 Celebrating our wonderful community! 💫")
        
        # Community celebration animation
        if community_animation:
            st_lottie(community_animation, speed=1, height=300, key="community_celebration")

# 🔄 RESET OPTIONS
with st.expander("🔄 Management Options"):
    if st.button("🗑️ Clear All Messages", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_update = datetime.now()
        st.success("🧹 All messages cleared! The wall is fresh and ready for new inspiration.")
        time.sleep(2)
        st.rerun()
    
    if st.button("📊 Export Community Data", use_container_width=True):
        # Create a simple data export
        community_data = {
            "Total Messages": len(st.session_state.messages),
            "Total Reactions": sum(sum(msg["reactions"].values()) for msg in st.session_state.messages),
            "Most Active User": max(set(msg["user"] for msg in st.session_state.messages), 
                                  key=lambda x: sum(1 for msg in st.session_state.messages if msg["user"] == x)) if st.session_state.messages else "N/A",
            "Most Loved Message": max(st.session_state.messages, 
                                    key=lambda x: sum(x["reactions"].values()))["message"][:50] + "..." if st.session_state.messages else "N/A"
        }
        
        st.info("**Community Snapshot:**")
        for key, value in community_data.items():
            st.write(f"**{key}:** {value}")