# Web/utils/style_utils.py
import streamlit as st

def apply_custom_styles():
    """Apply enhanced pink theme with animations"""
    st.markdown("""
    <style>
    /* Enhanced pink theme with animations */
    .main-header {
        font-size: 3rem;
        color: #e91e63;
        text-align: center;
        font-weight: bold;
        margin-bottom: 2rem;
        background: linear-gradient(45deg, #e91e63, #f06292);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: fadeIn 2s ease-in;
    }
    
    .sub-header {
        font-size: 2rem;
        color: #e91e63;
        margin: 1rem 0;
        animation: slideIn 1s ease-out;
    }
    
    .pink-card {
        background: linear-gradient(135deg, #fce4ec, #f8bbd9);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #e91e63;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(233, 30, 99, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .pink-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(233, 30, 99, 0.2);
    }
    
    .user-message {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        padding: 1rem;
        border-radius: 20px;
        margin: 0.5rem 0;
        border: 2px solid #90caf9;
        animation: slideInRight 0.5s ease-out;
        max-width: 80%;
        margin-left: auto;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #fce4ec, #f8bbd9);
        padding: 1rem;
        border-radius: 20px;
        margin: 0.5rem 0;
        border: 2px solid #f48fb1;
        animation: slideInLeft 0.5s ease-out;
        max-width: 80%;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 2px solid transparent;
        animation: zoomIn 0.6s ease-out;
    }
    
    .feature-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 15px 40px rgba(233, 30, 99, 0.2);
        border-color: #e91e63;
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    /* Keyframe Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes fadeInUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes slideInRight {
        from { transform: translateX(50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes zoomIn {
        from { transform: scale(0.8); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Custom button styles */
    .stButton > button {
        background: linear-gradient(45deg, #e91e63, #f06292);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(233, 30, 99, 0.4);
    }
    
    /* Custom progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(45deg, #e91e63, #f06292);
    }
    </style>
    """, unsafe_allow_html=True)

def setup_page_config():
    """Setup enhanced page configuration"""
    st.set_page_config(
        page_title="Breast Friend Forever",
        page_icon="💖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def create_feature_card(icon: str, title: str, description: str):
    """Create an animated feature card"""
    st.markdown(f"""
    <div class="feature-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
        <h3 style="color: #e91e63; margin-bottom: 1rem;">{title}</h3>
        <p style="color: #666; line-height: 1.5;">{description}</p>
    </div>
    """, unsafe_allow_html=True)