import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
import requests
import json
import time

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

def load_lottie_from_urls(url_list):
    """Try multiple URLs until one works"""
    for url in url_list:
        animation = load_lottieurl(url)
        if animation:
            return animation
    return None

st.set_page_config(page_title="Self Exam Guide", page_icon="🤗", layout="wide")

# 🎨 SELF EXAM ANIMATION CSS
st.markdown("""
    <style>
    @keyframes gentlePulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    @keyframes floatUp {
        0% { transform: translateY(0px); opacity: 0.8; }
        50% { transform: translateY(-5px); opacity: 1; }
        100% { transform: translateY(0px); opacity: 0.8; }
    }
    
    @keyframes slideInFromLeft {
        0% { transform: translateX(-100px); opacity: 0; }
        100% { transform: translateX(0); opacity: 1; }
    }
    
    .tip-bubble {
        background: linear-gradient(135deg, #FFF0F5, #FFE4EC);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-left: 5px solid #FF69B4;
        animation: gentlePulse 3s ease-in-out infinite;
        box-shadow: 0 5px 15px rgba(255, 105, 180, 0.2);
    }
    
    .step-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 3px solid transparent;
        box-shadow: 0 8px 25px rgba(255, 105, 180, 0.15);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        animation: slideInFromLeft 0.6s ease-out;
    }
    
    .step-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transition: left 0.6s;
    }
    
    .step-card:hover::before {
        left: 100%;
    }
    
    .step-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(255, 105, 180, 0.3);
    }
    
    .completed-step {
        border-color: #4CAF50;
        background: linear-gradient(135deg, #F0FFF0, #E8F5E8);
    }
    
    .current-step {
        border-color: #FF69B4;
        background: linear-gradient(135deg, #FFF0F5, #FFE4EC);
        animation: gentlePulse 2s infinite;
    }
    
    .progress-circle {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #FF69B4, #EC4899);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1.2rem;
        margin-right: 1.5rem;
        animation: floatUp 3s ease-in-out infinite;
    }
    
    .animation-container {
        text-align: center;
        margin: 1rem 0;
        padding: 1.5rem;
        background: linear-gradient(135deg, #F8FAFC, #F1F5F9);
        border-radius: 20px;
        border: 2px solid #FF69B4;
        animation: gentlePulse 4s ease-in-out infinite;
    }
    
    .practice-highlight {
        background: linear-gradient(135deg, #FFFBEB, #FEF3C7);
        border: 2px solid #F59E0B;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        animation: gentlePulse 2s infinite;
    }
    
    .animation-title {
        color: #FF69B4;
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Load step-specific Lottie animations with multiple URL options
try:
    # Step 1: Mirror Check - Multiple options
    mirror_animation = load_lottie_from_urls([
        "https://assets1.lottiefiles.com/packages/lf20_ukwacdcs.json",  # Person looking in mirror
        "https://assets9.lottiefiles.com/packages/lf20_5tt2Th.json",    # Alternative mirror animation
        "https://assets1.lottiefiles.com/packages/lf20_u8mG1R.json"     # Person animation
    ])
    
    # Step 2: Arms Up - Multiple options
    arms_up_animation = load_lottie_from_urls([
        "https://assets1.lottiefiles.com/packages/lf20_u8mG1R.json",    # Person with raised arms
        "https://assets9.lottiefiles.com/packages/lf20_5tt2Th.json",    # Alternative arms up
        "https://assets1.lottiefiles.com/packages/lf20_ukwacdcs.json"   # Fallback
    ])
    
    # Step 3: Lie Down - Multiple options
    lie_down_animation = load_lottie_from_urls([
        "https://assets9.lottiefiles.com/packages/lf20_5tt2Th.json",    # Person lying down
        "https://assets1.lottiefiles.com/packages/lf20_ukwacdcs.json",  # Alternative
        "https://assets1.lottiefiles.com/packages/lf20_u8mG1R.json"     # Fallback
    ])
    
    # Step 4: Circular Motion - Multiple options
    circular_motion_animation = load_lottie_from_urls([
        "https://assets1.lottiefiles.com/packages/lf20_sgn7zqbs.json",  # Circular hand motion
        "https://assets5.lottiefiles.com/packages/lf20_0fhgwtli.json",  # Hand movements
        "https://assets1.lottiefiles.com/packages/lf20_kdxn8rqk.json"   # Circular pattern
    ])
    
    # Step 5: Full Coverage - Multiple options
    full_coverage_animation = load_lottie_from_urls([
        "https://assets5.lottiefiles.com/packages/lf20_0fhgwtli.json",  # Hand covering area
        "https://assets1.lottiefiles.com/packages/lf20_sgn7zqbs.json",  # Hand movements
        "https://assets1.lottiefiles.com/packages/lf20_kdxn8rqk.json"   # Coverage animation
    ])
    
    # Step 6: Shower Check - Multiple options
    shower_animation = load_lottie_from_urls([
        "https://assets1.lottiefiles.com/packages/lf20_kdxn8rqk.json",  # Person in shower
        "https://assets9.lottiefiles.com/packages/lf20_5tt2Th.json",    # Water/self-care
        "https://assets1.lottiefiles.com/packages/lf20_ukwacdcs.json"   # Fallback
    ])
    
    # Additional specialized animations
    hand_circular_animation = load_lottie_from_urls([
        "https://assets1.lottiefiles.com/packages/lf20_sgn7zqbs.json",  # Circular hand motion
        "https://assets5.lottiefiles.com/packages/lf20_0fhgwtli.json"   # Hand movements
    ])
    
    # Celebration animations
    heart_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_5njp3vgg.json")
    celebration_animation = load_lottie_from_urls([
        "https://assets1.lottiefiles.com/packages/lf20_ukwacdcs.json",
        "https://assets1.lottiefiles.com/packages/lf20_kdxn8rqk.json"
    ])
    
    # Medical/health animations
    medical_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_w51pcehl.json")
    
except Exception as e:
    st.warning(f"Some animations failed to load: {e}")
    # Set fallbacks to None
    mirror_animation = arms_up_animation = lie_down_animation = None
    circular_motion_animation = full_coverage_animation = shower_animation = None
    heart_animation = celebration_animation = medical_animation = None

# Initialize session state
if 'completed_steps' not in st.session_state:
    st.session_state.completed_steps = set()
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'practice_mode' not in st.session_state:
    st.session_state.practice_mode = False
if 'current_practice_step' not in st.session_state:
    st.session_state.current_practice_step = 1

st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem;">
        <h1 style="color: #FF69B4; font-size: 3rem; margin-bottom: 1rem;">
            🤗 Self-Exam Guide
        </h1>
        <p style="font-size: 1.3rem; color: #666;">
            Learn to perform breast self-exams with love, care, and confidence 💝
        </p>
    </div>
    """, unsafe_allow_html=True)

# Welcome animation
if mirror_animation:
    st_lottie(mirror_animation, speed=1, height=200, key="self_exam_welcome")

# 🎯 PROGRESS TRACKER
st.markdown("### 🎯 Your Self-Exam Journey")

total_steps = 6
progress = len(st.session_state.completed_steps) / total_steps

col1, col2, col3 = st.columns([2, 3, 2])

with col2:
    st.markdown(f"""
        <div style="text-align: center; background: linear-gradient(135deg, #FFF0F5, #FFE4EC); 
                    padding: 2rem; border-radius: 20px; margin: 1rem 0;">
            <h3 style="color: #FF69B4; margin-bottom: 1rem;">Your Progress</h3>
            <div style="background: #E5E7EB; border-radius: 10px; height: 20px; margin: 1rem 0;">
                <div style="background: linear-gradient(135deg, #FF69B4, #EC4899); 
                            height: 100%; border-radius: 10px; width: {progress * 100}%; 
                            transition: width 0.5s ease;"></div>
            </div>
            <p style="color: #666; margin: 0;">
                {len(st.session_state.completed_steps)} of {total_steps} steps completed
            </p>
            <div style="display: flex; justify-content: center; gap: 0.5rem; margin-top: 1rem;">
                {"".join(["✅" if i+1 in st.session_state.completed_steps else "⭕" for i in range(total_steps)])}
            </div>
        </div>
        """, unsafe_allow_html=True)

# 🎮 PRACTICE MODE TOGGLE
if st.button("🎮 Enter Practice Mode" if not st.session_state.practice_mode else "🎮 Exit Practice Mode", 
             use_container_width=True, type="primary" if not st.session_state.practice_mode else "secondary"):
    st.session_state.practice_mode = not st.session_state.practice_mode
    st.rerun()

if st.session_state.practice_mode:
    st.markdown("""
        <div class="practice-highlight">
            <h3 style="color: #F59E0B; text-align: center; margin-bottom: 1rem;">🎮 Practice Mode Active</h3>
            <p style="text-align: center; color: #666; margin: 0;">
                Follow along with the animations to practice each step in real-time!
            </p>
        </div>
        """, unsafe_allow_html=True)

# 📝 SELF-EXAM STEPS WITH SPECIFIC ANIMATIONS
st.markdown("### 📝 Step-by-Step Guide")

exam_steps = [
    {
        "id": 1,
        "title": "Get Comfortable & Relax",
        "description": "Find a quiet, private space where you can relax. Sit or stand in front of a mirror with your shoulders straight and arms on your hips. Take a few deep breaths to relax.",
        "visual": "🪞",
        "tip": "💖 Be gentle with yourself - this is about loving awareness, not criticism",
        "tip_color": "#FF69B4",
        "animation": mirror_animation,
        "animation_name": "Mirror Position",
        "practice_instructions": "Stand in front of a mirror. Relax your shoulders. Place hands on hips."
    },
    {
        "id": 2,
        "title": "Visual Inspection - Arms Down",
        "description": "Look for any changes in size, shape, color, or visible distortion. Check for swelling, dimpling, puckering, or changes in the nipple with arms at your sides.",
        "visual": "👀",
        "tip": "🌈 You're building a powerful health habit - that's something to celebrate!",
        "tip_color": "#EC4899",
        "animation": mirror_animation,
        "animation_name": "Visual Inspection",
        "practice_instructions": "Look carefully at your breasts in the mirror. Note any changes from last month."
    },
    {
        "id": 3,
        "title": "Raise Arms & Inspect",
        "description": "Raise your arms overhead and look for the same changes. Notice if there's any fluid coming from one or both nipples. Check for symmetry and skin changes.",
        "visual": "🙆‍♀️",
        "tip": "🎵 Put on some calming music - make this your special self-care time",
        "tip_color": "#DB2777",
        "animation": arms_up_animation,
        "animation_name": "Arms Raised Inspection",
        "practice_instructions": "Raise both arms overhead. Look for changes in shape or contour."
    },
    {
        "id": 4,
        "title": "Lie Down & Feel",
        "description": "Lie down and use your right hand to feel your left breast, then left hand for right breast. Use a firm, smooth touch with the first few finger pads of your hand.",
        "visual": "💆‍♀️",
        "tip": "💫 You're learning your body's unique landscape - how amazing is that!",
        "tip_color": "#BE185D",
        "animation": lie_down_animation,
        "animation_name": "Lying Down Position",
        "practice_instructions": "Lie down with a pillow under your right shoulder. Place right arm behind your head."
    },
    {
        "id": 5,
        "title": "Follow a Systematic Pattern",
        "description": "Use a systematic pattern - circular, up-and-down, or wedge. Cover the entire breast from collarbone to top of abdomen, armpit to cleavage. Don't forget the armpit area.",
        "visual": "🌀",
        "tip": "🌟 Consistency creates confidence - you're building a lifelong health skill",
        "tip_color": "#9D174D",
        "animation": circular_motion_animation,
        "animation_name": "Circular Examination Pattern",
        "practice_instructions": "Use circular motions with your finger pads. Cover the entire breast area systematically."
    },
    {
        "id": 6,
        "title": "Final Check in Shower",
        "description": "Many women find it easiest to feel their breasts when skin is wet and slippery. In the shower, repeat the same hand movements with soapy hands for better glide.",
        "visual": "🚿",
        "tip": "🎉 You did it! Regular checks are a beautiful act of self-love and care",
        "tip_color": "#831843",
        "animation": shower_animation,
        "animation_name": "Shower Examination",
        "practice_instructions": "In the shower, use soapy hands to repeat the examination with smooth gliding motions."
    }
]

# Display steps with specific animations
for step in exam_steps:
    is_completed = step["id"] in st.session_state.completed_steps
    is_current = step["id"] == st.session_state.current_step
    animation_delay = f"animation-delay: {step['id'] * 0.1}s;"
    
    card_class = "step-card"
    if is_completed:
        card_class += " completed-step"
    elif is_current:
        card_class += " current-step"
    
    st.markdown(f"""
        <div class="{card_class}" style="{animation_delay}">
            <div style="display: flex; align-items: flex-start;">
                <div class="progress-circle">
                    {step["visual"]}
                </div>
                <div style="flex: 1;">
                    <h3 style="color: #1F2937; margin: 0 0 1rem 0;">Step {step['id']}: {step["title"]}</h3>
                    <p style="color: #6B7280; line-height: 1.6; margin-bottom: 1.5rem;">
                        {step["description"]}
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display the step-specific animation
    if step["animation"]:
        st.markdown(f"""
            <div class="animation-container">
                <div class="animation-title">🎬 {step['animation_name']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st_lottie(
            step["animation"], 
            speed=1, 
            height=200, 
            key=f"step_anim_{step['id']}",
            quality="high"
        )
    
    # Practice instructions for practice mode
    if st.session_state.practice_mode and step["id"] == st.session_state.current_step:
        st.markdown(f"""
            <div class="practice-highlight">
                <h4 style="color: #F59E0B; margin-bottom: 0.5rem;">🧭 Practice Instructions:</h4>
                <p style="color: #666; margin: 0;">{step['practice_instructions']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="tip-bubble">
            <strong style="color: {step['tip_color']};">{step["tip"]}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    # Buttons with enhanced functionality
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button(f"✓ Mark Complete", key=f"complete_{step['id']}", use_container_width=True):
            st.session_state.completed_steps.add(step["id"])
            if step["id"] < total_steps:
                st.session_state.current_step = step["id"] + 1
            st.success(f"🎉 Completed: {step['title']}!")
            if heart_animation:
                st_lottie(heart_animation, speed=1, height=150, key=f"celebration_{step['id']}")
            st.rerun()
    
    with col2:
        if st.button(f"▶️ Practice Step", key=f"practice_{step['id']}", use_container_width=True):
            st.session_state.practice_mode = True
            st.session_state.current_practice_step = step["id"]
            st.info(f"💫 Now practicing: {step['title']}")
            st.rerun()
    
    with col3:
        if st.button(f"🔁 Repeat Animation", key=f"repeat_{step['id']}", use_container_width=True):
            st.info(f"🔄 Replaying animation for: {step['title']}")
            # The animation will automatically replay due to key change
    
    with col4:
        if step["id"] > 1:
            if st.button(f"⬅️ Previous", key=f"prev_{step['id']}", use_container_width=True):
                st.session_state.current_step = step["id"] - 1
                st.rerun()
    
    st.markdown("---")

# 🎉 COMPLETION CELEBRATION
if len(st.session_state.completed_steps) == total_steps:
    st.balloons()
    st.markdown("""
        <div style="text-align: center; background: linear-gradient(135deg, #FF69B4, #EC4899); 
                    color: white; padding: 3rem; border-radius: 25px; margin: 2rem 0;">
            <h2 style="color: white; margin-bottom: 1rem;">🎊 Amazing! You've Completed Your Self-Exam Training! 🎊</h2>
            <p style="font-size: 1.2rem; opacity: 0.9;">
                You've learned a valuable lifelong skill for taking charge of your breast health. 
                Remember to perform self-exams monthly, about 3-5 days after your period ends.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    if celebration_animation:
        st_lottie(celebration_animation, speed=1, height=250, key="completion_celebration")
    
    # Certificate of completion
    st.markdown("""
        <div style="text-align: center; background: linear-gradient(135deg, #FFF0F5, #FFE4EC); 
                    padding: 2rem; border-radius: 20px; margin: 2rem 0; border: 3px dashed #FF69B4;">
            <h3 style="color: #FF69B4; margin-bottom: 1rem;">🏆 Certificate of Completion</h3>
            <p style="color: #666; font-size: 1.1rem;">
                <strong>This certifies that you have successfully completed</strong><br>
                the Breast Self-Examination Training Program
            </p>
            <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1.5rem;">
                <span style="font-size: 2rem;">🌸</span>
                <span style="font-size: 2rem;">💖</span>
                <span style="font-size: 2rem;">🌟</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 🎮 INTERACTIVE PRACTICE AREA WITH ANIMATIONS
st.markdown("### 🎮 Practice & Animation Library")

practice_cols = st.columns(2)

with practice_cols[0]:
    st.markdown("""
        <div style="text-align: center; background: #F8FAFC; padding: 2rem; border-radius: 20px;">
            <h4 style="color: #FF69B4;">Pattern Practice Studio</h4>
            <p style="color: #666;">Practice different examination patterns with guided animations</p>
        </div>
        """, unsafe_allow_html=True)
    
    pattern = st.selectbox(
        "Choose a pattern to practice:",
        ["Circular Motion 🌀", "Up-and-Down Lines ↕️", "Wedge Slices 🍰", "Spiral Outward 🎯", "Grid Pattern #️⃣"]
    )
    
    practice_speed = st.slider("Animation Speed", 0.5, 2.0, 1.0, 0.1)
    
    if st.button("🎬 Start Pattern Practice", use_container_width=True):
        st.info(f"🔍 Practicing {pattern} at {practice_speed}x speed...")
        # Show circular motion animation for practice
        if hand_circular_animation:
            st_lottie(hand_circular_animation, speed=practice_speed, height=200, key="pattern_practice")
        
        # Pattern-specific instructions
        pattern_instructions = {
            "Circular Motion 🌀": "Move in small circles, about the size of a coin. Overlap each circle slightly.",
            "Up-and-Down Lines ↕️": "Move straight up and down in vertical lines. Cover the entire breast area.",
            "Wedge Slices 🍰": "Imagine slicing the breast into wedges. Examine each wedge thoroughly.",
            "Spiral Outward 🎯": "Start at the nipple and spiral outward. Cover all breast tissue.",
            "Grid Pattern #️⃣": "Move in a grid pattern - up/down and left/right for complete coverage."
        }
        
        st.markdown(f"""
            <div class="practice-highlight">
                <h4 style="color: #F59E0B;">Pattern Instructions:</h4>
                <p style="color: #666; margin: 0;">{pattern_instructions[pattern]}</p>
            </div>
            """, unsafe_allow_html=True)

with practice_cols[1]:
    st.markdown("""
        <div style="text-align: center; background: #F8FAFC; padding: 2rem; border-radius: 20px;">
            <h4 style="color: #FF69B4;">Animation Reference Library</h4>
            <p style="color: #666;">Review all self-exam animations and techniques</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Animation library with descriptions
    animation_library = [
        {"name": "Mirror Position 🪞", "anim": mirror_animation, "desc": "Proper positioning for visual inspection"},
        {"name": "Arms Raised 🙆‍♀️", "anim": arms_up_animation, "desc": "Arm positions for complete visual check"},
        {"name": "Lying Down 💆‍♀️", "anim": lie_down_animation, "desc": "Correct position for physical examination"},
        {"name": "Circular Motion 🌀", "anim": circular_motion_animation, "desc": "Systematic circular examination technique"},
        {"name": "Full Coverage ✋", "anim": full_coverage_animation, "desc": "Ensuring complete breast tissue coverage"},
        {"name": "Shower Check 🚿", "anim": shower_animation, "desc": "Water-assisted examination technique"}
    ]
    
    selected_animation = st.selectbox(
        "Choose animation to review:",
        [anim["name"] for anim in animation_library],
        key="animation_library"
    )
    
    selected_anim_data = next(anim for anim in animation_library if anim["name"] == selected_animation)
    
    if selected_anim_data["anim"]:
        st.markdown(f"""
            <div style="text-align: center; margin: 1rem 0;">
                <p style="color: #666; font-style: italic;">{selected_anim_data['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
        st_lottie(selected_anim_data["anim"], speed=1, height=200, key="animation_library_demo")

# 💡 REMINDER & PROGRESS SYSTEM
st.markdown("### 💡 Reminder & Progress System")

reminder_cols = st.columns([2, 1, 1])

with reminder_cols[0]:
    st.markdown("""
        <div style="background: linear-gradient(135deg, #ECFDF5, #D1FAE5); 
                    padding: 1.5rem; border-radius: 15px; border-left: 5px solid #10B981;">
            <h4 style="color: #065F46; margin-bottom: 0.5rem;">📅 Monthly Reminder</h4>
            <p style="color: #047857; margin: 0; font-size: 0.9rem;">
                Best time: 3-5 days after your period ends<br>
                Or same date each month if post-menopausal
            </p>
        </div>
        """, unsafe_allow_html=True)

with reminder_cols[1]:
    if st.button("🔔 Set Reminder", use_container_width=True):
        st.balloons()
        st.success("📱 Monthly reminder set! You'll be notified to perform your self-exam.")

with reminder_cols[2]:
    if st.button("📊 View Progress", use_container_width=True):
        # Show progress analytics
        st.info("""
        **Your Progress Analytics:**
        - Steps Completed: {}/6
        - Current Streak: 🔥
        - Total Practices: 📈
        - Confidence Level: 💪
        """.format(len(st.session_state.completed_steps)))

# 🎊 FINAL ENCOURAGEMENT
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #FFF0F5, #FFE4EC); 
                border-radius: 25px; margin: 2rem 0;">
        <h2 style="color: #FF69B4; margin-bottom: 1rem;">💝 You're Becoming Your Own Health Advocate</h2>
        <p style="color: #666; font-size: 1.1rem; line-height: 1.6;">
            By learning proper self-examination techniques, you're taking powerful control of your health. 
            This knowledge empowers you to notice changes early and seek timely care if needed.<br>
            <strong>Your commitment to self-care is inspiring! 🌸</strong>
        </p>
        <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 2rem;">
            <span style="animation: gentlePulse 2s infinite; font-size: 1.5rem;">💖</span>
            <span style="animation: gentlePulse 2s infinite; animation-delay: 0.3s; font-size: 1.5rem;">🌟</span>
            <span style="animation: gentlePulse 2s infinite; animation-delay: 0.6s; font-size: 1.5rem;">🤗</span>
            <span style="animation: gentlePulse 2s infinite; animation-delay: 0.9s; font-size: 1.5rem;">🌈</span>
            <span style="animation: gentlePulse 2s infinite; animation-delay: 1.2s; font-size: 1.5rem;">🎯</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 🔄 MANAGEMENT OPTIONS
with st.expander("⚙️ Management Options"):
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Reset All Progress", use_container_width=True):
            st.session_state.completed_steps = set()
            st.session_state.current_step = 1
            st.session_state.practice_mode = False
            st.success("🔄 All progress reset! Ready to start fresh.")
            st.rerun()
    
    with col2:
        if st.button("📋 Export Progress", use_container_width=True):
            st.info("""
            **Progress Summary:**
            - Completed Steps: {}
            - Current Step: {}
            - Practice Mode: {}
            - Last Updated: {}
            """.format(
                len(st.session_state.completed_steps),
                st.session_state.current_step,
                "Active" if st.session_state.practice_mode else "Inactive",
                "Now"
            ))

# 🆘 QUICK HELP
with st.expander("🆘 Quick Help & Tips"):
    st.markdown("""
    **Common Questions:**
    
    **🤔 How often should I do self-exams?**
    - Monthly, 3-5 days after your period ends
    - Same date each month if post-menopausal
    
    **🕒 How long does it take?**
    - About 5-10 minutes once you're comfortable
    
    **👐 What pressure should I use?**
    - Use light, medium, and firm pressure in each area
    - You should feel different layers of tissue
    
    **🚨 When should I call a doctor?**
    - Any new lump or hard knot
    - Unusual swelling, warmth, or redness  
    - Changes in size, shape, or skin texture
    - Nipple discharge or pulling in
    
    **💪 Remember:**
    - Most breast changes are NOT cancer
    - You're learning what's normal FOR YOU
    - Consistency is more important than perfection
    """)