# Web/app.py
import streamlit as st
import time
from utils.style_utils import setup_page_config, apply_custom_styles, create_feature_card
from utils.animations import anim_manager
from utils.api_client import api_client
from pwa_install_prompt import show_install_prompt

# Setup page
setup_page_config()
apply_custom_styles()

# Show PWA install prompt on mobile
show_install_prompt()

# Main header with animation
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown('<div class="main-header">Breast Friend Forever 💖</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem; color: #666;">Your compassionate animated guide to breast health</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    anim_manager.display_animation("welcome", height=200)

# Backend connection with animation
connection_container = st.container()
with connection_container:
    if api_client.health_check():
        # Backend connected - logged silently
        pass
    else:
        st.error("❌ Backend Connection Failed")

# Animated welcome section
st.markdown("""
<div class="pink-card pulse-animation">
    <h2>🎀 Welcome to Your Breast Health Companion</h2>
    <p>Your compassionate, animated guide to breast health education, support, and resources. 
    Every interaction is designed with care and understanding.</p>
</div>
""", unsafe_allow_html=True)

# Animated features grid
st.markdown("### ✨ Explore Our Features")
cols = st.columns(4)

with cols[0]:
    create_feature_card(
        "🤗", 
        "Self-Exam Guide", 
        "Interactive step-by-step instructions with visual guides"
    )

with cols[1]:
    create_feature_card(
        "💬", 
        "AI Assistant", 
        "Animated chatbot with compassionate responses"
    )

with cols[2]:
    create_feature_card(
        "🏥", 
        "Find Help", 
        "Locate screening facilities with interactive maps"
    )

with cols[3]:
    create_feature_card(
        "💕", 
        "Support Community", 
        "Share and receive encouragement with animations"
    )

# Interactive getting started section
with st.expander("🚀 **Quick Start Guide**", expanded=True):
    st.write("""
    **1.** 🤗 **Self-Exam Guide** - Learn breast self-examination with animated steps  
    **2.** 💬 **Chat Assistant** - Ask questions and get animated responses  
    **3.** 🏥 **Find Screening** - Locate facilities with interactive search  
    **4.** 💕 **Support Wall** - Share encouragement with heart animations  
    **5.** 📚 **Resources** - Access educational content with smooth transitions
    """)
    
    if st.button("🎯 Start Your Journey", type="primary"):
        with st.spinner("Loading your personalized experience..."):
            time.sleep(2)
            st.success("Ready to explore! Use the sidebar to navigate.")

# Footer with animation
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns([2, 1, 2])
with footer_col2:
    anim_manager.display_animation("heart", height=100)
    st.markdown("""
    <div style="text-align: center;">
        <p style="color: #e91e63; font-weight: bold;">Made with 💖 for your health journey</p>
    </div>
    """, unsafe_allow_html=True)