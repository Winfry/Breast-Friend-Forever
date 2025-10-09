import streamlit as st
import time
import json
import os
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="Breast Self-Exam",
    page_icon="🤗",
    layout="wide"
)

# Function to load local Lottie files with correct path
def load_lottie_file(filepath: str):
    try:
        # Try multiple possible paths
        possible_paths = [
            filepath,  # Direct path
            f"../{filepath}",  # One level up
            f"../lottie_animations/{filepath.split('/')[-1]}",  # From pages folder
            f"lottie_animations/{filepath.split('/')[-1]}"  # Relative to current dir
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, "r") as f:
                    return json.load(f)
        
        st.error(f"Could not find animation file: {filepath}")
        st.info(f"Looking in: {os.getcwd()}")
        return None
    except Exception as e:
        st.error(f"Error loading animation {filepath}: {str(e)}")
        return None

# Custom CSS for styling
st.markdown("""
<style>
    .tip-bubble {
        background-color: #f8f9fa;
        border-left: 4px solid #FF69B4;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .step-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
    }
    .animation-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 1rem;
        background: #fafafa;
        border-radius: 10px;
        min-height: 250px;
    }
    .completed-step {
        border: 2px solid #4CAF50 !important;
        background: #f8fff8 !important;
    }
    .practiced-step {
        border: 2px solid #FFB6C1 !important;
        background: #fff8f8 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤗 Breast Self-Exam Guide")
st.markdown("Learn how to perform a breast self-exam in 6 simple steps with interactive guidance.")

# Debug: Show current working directory and check if files exist
with st.expander("Debug Info (Click to see file paths)"):
    st.write("Current working directory:", os.getcwd())
    st.write("Files in current directory:", os.listdir("."))
    if os.path.exists("../lottie_animations"):
        st.write("Files in lottie_animations folder:", os.listdir("../lottie_animations"))
    elif os.path.exists("lottie_animations"):
        st.write("Files in lottie_animations folder:", os.listdir("lottie_animations"))
    else:
        st.error("lottie_animations folder not found!")

# Initialize session state for completion tracking
if 'completed_steps' not in st.session_state:
    st.session_state.completed_steps = set()
if 'practiced_steps' not in st.session_state:
    st.session_state.practiced_steps = set()

def create_step(step_number, title, tip_text, tip_color, animation_file, button_key_suffix, instructions):
    # Determine CSS class based on completion status
    container_class = "step-container"
    if step_number in st.session_state.completed_steps:
        container_class += " completed-step"
    elif step_number in st.session_state.practiced_steps:
        container_class += " practiced-step"
    
    st.markdown(f'<div class="{container_class}">', unsafe_allow_html=True)
    
    st.subheader(f"Step {step_number}: {title}")
    
    # Create two columns: animation on left, instructions on right
    col_anim, col_content = st.columns([2, 3])
    
    with col_anim:
        st.markdown('<div class="animation-container">', unsafe_allow_html=True)
        
        # Try different path configurations
        animation_paths = [
            f"../lottie_animations/{animation_file}",  # From pages folder
            f"lottie_animations/{animation_file}",     # Relative to current dir
            animation_file                             # Just the filename
        ]
        
        lottie_anim = None
        for path in animation_paths:
            lottie_anim = load_lottie_file(path)
            if lottie_anim:
                break
        
        if lottie_anim:
            st_lottie(lottie_anim, height=200, key=f"anim_{button_key_suffix}")
        else:
            # Show a placeholder with the animation name
            st.warning(f"Animation placeholder for: {animation_file}")
            st.markdown(f"*{animation_file.replace('.json', '').replace('-', ' ').title()}*")
            # You could add a fallback image here
            st.image("https://via.placeholder.com/200x150/FF69B4/FFFFFF?text=Animation", width=200)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_content:
        # Instructions
        st.markdown(f"**How to do it:**")
        st.markdown(instructions)
        
        # Tip bubble
        st.markdown(f'''
        <div class="tip-bubble">
            <strong style="color: {tip_color}; font-size: 1.1em;">{tip_text}</strong>
        </div>
        ''', unsafe_allow_html=True)
        
        # Buttons
        button_col1, button_col2 = st.columns(2)
        
        with button_col1:
            if st.button(f"✓ Mark Complete", 
                        key=f"complete_{button_key_suffix}",
                        use_container_width=True,
                        type="primary" if step_number not in st.session_state.completed_steps else "secondary"):
                st.session_state.completed_steps.add(step_number)
                if step_number in st.session_state.practiced_steps:
                    st.session_state.practiced_steps.remove(step_number)
                st.success("✅ Step marked as complete!")
                time.sleep(1)
                st.rerun()
        
        with button_col2:
            if st.button(f"▶️ Practice This Step", 
                        key=f"practice_{button_key_suffix}",
                        use_container_width=True):
                st.session_state.practiced_steps.add(step_number)
                st.info("🔄 Practicing this step...")
                time.sleep(1)
                st.rerun()
        
        # Show completion status
        if step_number in st.session_state.completed_steps:
            st.markdown("**Status: ✅ Completed**")
        elif step_number in st.session_state.practiced_steps:
            st.markdown("**Status: 🔄 Practiced**")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Step 1: Visual Inspection with Mirror
create_step(1, "Visual Inspection", 
           "💖 Be gentle with yourself - this is about loving awareness, not criticism", 
           "#FF69B4", "mirror-check.json", "step1",
           """
           - Stand in front of a mirror with your shoulders straight
           - Look for any changes in size, shape, or color
           - Check for visible distortion or swelling
           - Observe for any skin changes or redness
           """)

# Step 2: Raise Arms  
create_step(2, "Raise Arms", 
           "🌈 You're building a powerful health habit - that's something to celebrate!", 
           "#EC4899", "arms-up.json", "step2",
           """
           - Raise your arms high above your head
           - Look for the same changes as in step 1
           - Check under your arms for any swelling
           - Observe from different angles
           """)

# Step 3: Lying Down Position
create_step(3, "Lying Down Position", 
           "🎵 Put on some calming music - make this your special self-care time", 
           "#DB2777", "lie-down.json", "step3",
           """
           - Lie down on your back with a pillow under your right shoulder
           - Use your left hand to examine your right breast
           - Keep fingers flat and together
           - Use a systematic pattern (circles, lines, or wedges)
           """)

# Step 4: Circular Motion
create_step(4, "Circular Motion", 
           "💫 You're learning your body's unique landscape - how amazing is that!", 
           "#BE185D", "circular-motion.json", "step4",
           """
           - Use the pads of your three middle fingers
           - Make circular motions about the size of a quarter
           - Vary pressure: light, medium, and firm
           - Feel for any lumps or thickening
           """)

# Step 5: Full Coverage
create_step(5, "Full Coverage", 
           "🌟 Consistency creates confidence - you're building a lifelong health skill", 
           "#9D174D", "full-coverage.json", "step5",
           """
           - Ensure you cover the entire breast area
           - From collarbone to top of abdomen
           - From armpit to cleavage
           - Don't forget the nipple area
           """)

# Step 6: Shower Check
create_step(6, "Shower Check", 
           "🎉 You did it! Regular checks are a beautiful act of self-love and care", 
           "#831843", "shower-check.json", "step6",
           """
           - Repeat the examination in the shower
           - Wet, soapy skin can make it easier to feel
           - Use the same systematic approach
           - Check both breasts thoroughly
           """)

# Progress tracking in sidebar
st.sidebar.markdown("### 📊 Your Progress")
total_steps = 6
completed = len(st.session_state.completed_steps)
practiced = len(st.session_state.practiced_steps)

# Progress bar
progress = completed / total_steps
st.sidebar.progress(progress)

# Metrics
st.sidebar.metric("Completed Steps", f"{completed}/{total_steps}")
st.sidebar.metric("Practiced Steps", f"{practiced}/{total_steps}")

# Celebration message when all steps are completed
if completed == total_steps:
    st.sidebar.balloons()
    st.sidebar.success("🎊 Amazing! You've completed all steps!")
    st.balloons()

# Reset button
if st.sidebar.button("🔄 Reset All Progress", use_container_width=True):
    st.session_state.completed_steps = set()
    st.session_state.practiced_steps = set()
    st.rerun()

# Additional resources
st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Additional Resources")
st.sidebar.page_link("pages/3_📚_Resources.py", label="📚 Educational Resources", icon="📚")
st.sidebar.page_link("pages/4_🏥_Find_Screening.py", label="🏥 Find Screening Centers", icon="🏥")
st.sidebar.page_link("pages/5_💕_Encouragement_Wall.py", label="💕 Encouragement Wall", icon="💕")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Remember: Breast self-exams should be done monthly, about 3-5 days after your period ends.</p>
    <p>If you notice any changes, contact your healthcare provider.</p>
</div>
""", unsafe_allow_html=True)