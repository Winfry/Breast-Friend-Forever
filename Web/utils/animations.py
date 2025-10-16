# Web/utils/animations.py
import streamlit as st
import requests
import json
from streamlit_lottie import st_lottie

class AnimationManager:
    def __init__(self):
        self.animations = {
            "welcome": "https://assets1.lottiefiles.com/packages/lf20_vybwn7df.json",
            "chat": "https://assets1.lottiefiles.com/packages/lf20_u8jppsed.json",
            "health": "https://assets1.lottiefiles.com/packages/lf20_5tkzkflw.json",
            "support": "https://assets1.lottiefiles.com/packages/lf20_osdxlbqq.json",
            "loading": "https://assets1.lottiefiles.com/packages/lf20_soCRuE.json",
            "success": "https://assets1.lottiefiles.com/packages/lf20_yRZZuC.json",
            "heart": "https://assets1.lottiefiles.com/packages/lf20_5mhapbvh.json"
        }
    
    def load_lottie_url(self, url: str):
        """Load Lottie animation from URL"""
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return r.json()
        except:
            return None
        return None
    
    def load_lottie_file(self, filepath: str):
        """Load Lottie animation from local file"""
        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except:
            return None
    
    def display_animation(self, animation_key: str, height: int = 200, key: str = None):
        """Display Lottie animation"""
        animation_url = self.animations.get(animation_key)
        if animation_url:
            animation_data = self.load_lottie_url(animation_url)
            if animation_data:
                st_lottie(animation_data, height=height, key=key or animation_key)
    
    def loading_animation(self, text: str = "Loading..."):
        """Show loading animation"""
        with st.spinner(text):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                self.display_animation("loading", height=100, key="loading")
    
    def success_animation(self, text: str = "Success!"):
        """Show success animation"""
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            self.display_animation("success", height=150, key="success")
            st.success(text)

# Create global instance
anim_manager = AnimationManager()