import streamlit as st
from streamlit_lottie import st_lottie
import json
import time

# Function to load Lottie animation from JSON file
def load_lottie_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# 🎯 Page Setup
st.set_page_config(page_title="Self-Exam Guide", page_icon="🖐️")

st.markdown("# 🖐️ Breast Self-Examination Guide")
st.caption("Your step-by-step companion for breast health awareness")

# 📋 Self-Exam Steps Data
steps = [
    {
        "title": "Step 1: Visual Inspection",
        "description": "Stand in front of a mirror with your shoulders straight and arms on your hips. Look for any changes in size, shape, or color of your breasts.",
        "tip": "💡 Look for any dimpling, puckering, or changes in the nipple."
    },
    {
        "title": "Step 2: Raise Your Arms", 
        "description": "Raise your arms and look for the same changes. Check for any fluid coming out of one or both nipples.",
        "tip": "💡 Take your time and be thorough."
    },
    {
        "title": "Step 3: Lie Down Comfortably",
        "description": "Lie down and feel your breasts using your right hand to feel your left breast and then your left hand to feel your right breast.",
        "tip": "💡 Use a pillow under your shoulder for comfort."
    },
    {
        "title": "Step 4: Use Your Fingertips",
        "description": "Use the pads of your fingers, keeping them flat and together. Use a circular motion, about the size of a quarter.",
        "tip": "💡 Don't rush - cover all areas systematically."
    },
    {
        "title": "Step 5: Cover Entire Breast",
        "description": "Cover the entire breast from top to bottom, side to side — from your collarbone to the top of your abdomen, and from your armpit to your cleavage.",
        "tip": "💡 Follow a pattern to ensure you don't miss any areas."
    },
    {
        "title": "Step 6: Repeat Standing or Sitting", 
        "description": "Finally, feel your breasts while you are standing or sitting. Many women find this easiest in the shower.",
        "tip": "💡 Wet, soapy skin can make it easier to feel changes."
    }
]

# 📖 Display Steps as Expandable Sections
for i, step in enumerate(steps, 1):
    with st.expander(f"{i}. {step['title']}", expanded=(i==1)):
        st.write(step['description'])
        st.info(step['tip'])

# ⏰ Reminder Feature
st.markdown("---")
st.markdown("### 📅 Monthly Reminder")
st.write("Set a monthly reminder to perform your self-examination:")
col1, col2 = st.columns(2)
with col1:
    reminder_date = st.selectbox("Day of month", list(range(1, 29)))
with col2:
    if st.button("Set Monthly Reminder"):
        st.success(f"✅ Reminder set for the {reminder_date}th of each month!")

# 💪 Encouragement Section
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 2rem; background: #FFF0F5; border-radius: 15px;">
        <h3 style="color: #FF69B4;">You've Got This! 💪</h3>
        <p>Regular self-examination is a powerful way to take control of your health. You're doing something amazing for yourself!</p>
    </div>
    """, unsafe_allow_html=True)