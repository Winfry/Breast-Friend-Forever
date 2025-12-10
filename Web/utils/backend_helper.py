# Web/utils/backend_helper.py
import streamlit as st
import time
from utils.api_client import api_client

def check_backend_with_retry(max_retries=3, retry_delay=10):
    """
    Check if backend is available, with retry logic for cold starts.
    Shows friendly messages to users during wake-up.
    
    Returns:
        bool: True if backend is available, False otherwise
    """
    for attempt in range(max_retries):
        if api_client.health_check():
            return True
        
        if attempt < max_retries - 1:
            # Backend is sleeping, show friendly message
            with st.spinner(f"🌙 Waking up the AI assistant... ({retry_delay}s)"):
                time.sleep(retry_delay)
        else:
            # Final attempt failed
            return False
    
    return False

def call_backend_feature(feature_name, api_call_func, *args, **kwargs):
    """
    Wrapper for backend API calls that handles sleep/wake gracefully.
    
    Args:
        feature_name: Name of the feature (e.g., "AI Chat", "Symptom Checker")
        api_call_func: The API function to call
        *args, **kwargs: Arguments to pass to the API function
    
    Returns:
        API response or None if backend unavailable
    """
    # First, check if backend is awake
    if not check_backend_with_retry(max_retries=2, retry_delay=15):
        # Backend is down or sleeping too long
        st.warning(f"""
        🌙 **{feature_name} is currently resting**
        
        This happens when the backend hasn't been used for a while (free hosting limitation).
        
        **What you can do:**
        - ✅ Try again in 30 seconds (it's waking up!)
        - ✅ Use our Self-Exam Guide or Resources (always available)
        - ✅ Come back later when the backend is awake
        
        *For instant access, we'd need paid hosting ($7/month). For now, please be patient! 💖*
        """)
        return None
    
    # Backend is awake, make the API call
    try:
        return api_call_func(*args, **kwargs)
    except Exception as e:
        st.error(f"❌ {feature_name} encountered an error. Please try again.")
        return None

# Example usage in Chat Assistant:
# from utils.backend_helper import call_backend_feature
# 
# response = call_backend_feature(
#     "AI Chat",
#     api_client.send_message,
#     user_message
# )
# 
# if response:
#     st.write(response)
