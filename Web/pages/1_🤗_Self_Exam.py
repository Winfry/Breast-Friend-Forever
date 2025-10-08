import streamlit as st
import time
from streamlit_lottie import st_lottie
import requests
import json

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

st.set_page_config(page_title="Self-Exam Guide", page_icon="🖐️")

# 🎨 EXTREME ANIMATION CSS
st.markdown("""
    <style>
    @keyframes stepGlow {
        0% { box-shadow: 0 0 20px rgba(255, 105, 180, 0.3); }
        50% { box-shadow: 0 0 40px rgba(255, 105, 180, 0.6); }
        100% { box-shadow: 0 0 20px rgba(255, 105, 180, 0.3); }
    }
    
    @keyframes iconBounce {
        0%, 100% { transform: scale(1) rotate(0deg); }
        25% { transform: scale(1.1) rotate(5deg); }
        75% { transform: scale(1.1) rotate(-5deg); }
    }
    
    @keyframes progressFill {
        from { width: 0%; }
        to { width: 100%; }
    }
    
    @keyframes celebration {
        0% { transform: scale(0); opacity: 0; }
        50% { transform: scale(1.2); opacity: 1; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .step-card {
        background: white;
        border-radius: 25px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        border-left: 6px solid #FF69B4;
        box-shadow: 0 8px 25px rgba(255, 105, 180, 0.15);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        animation: fadeIn 0.8s ease-out;
    }
    
    .step-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #FF69B4, #EC4899, #DB2777);
        transform: scaleX(0);
        transition: transform 0.6s ease;
    }
    
    .step-card:hover::before {
        transform: scaleX(1);
    }
    
    .step-card:hover {
        transform: translateY(-8px) scale(1.02);
        animation: stepGlow 2s infinite;
    }
    
    .step-icon {
        font-size: 3.5rem;
        animation: iconBounce 3s infinite;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    .completed-step {
        border-left-color: #4CAF50 !important;
        background: linear-gradient(135deg, #F0FFF0, #E8F5E8);
    }
    
    .current-step {
        animation: stepGlow 2s infinite !important;
        border: 3px solid #FF69B4;
    }
    
    .progress-container {
        background: #F0F0F0;
        border-radius: 15px;
        margin: 3rem 0;
        overflow: hidden;
        position: relative;
        height: 25px;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #FF69B4, #EC4899, #DB2777);
        height: 100%;
        border-radius: 15px;
        transition: width 0.8s cubic-bezier(0.22, 0.61, 0.36, 1);
        animation: progressFill 1.5s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .progress-bar::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .celebration-container {
        animation: celebration 1s ease-out;
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #FF69B4, #FF1493);
        color: white;
        border-radius: 30px;
        margin: 3rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .celebration-container::before {
        content: '🎉✨🌟🎊';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        font-size: 3rem;
        opacity: 0.1;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .tip-bubble {
        background: linear-gradient(135deg, #FFF0F5, #FFE4EC);
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        border: 2px dashed #FF69B4;
        position: relative;
        animation: fadeIn 0.8s ease-out;
    }
    
    .tip-bubble::before {
        content: '💡';
        position: absolute;
        top: -15px;
        left: 20px;
        background: white;
        padding: 5px;
        border-radius: 50%;
        font-size: 1.2rem;
    }
    
    .reminder-button {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        border: none;
        padding: 1.2rem 2.5rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        animation: pulse 2s infinite;
        position: relative;
        overflow: hidden;
    }
    
    .reminder-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(76, 175, 80, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# Load animations
try:
    mirror_anim = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_1pxqjqps.json")
    arms_anim = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_kdxn8rqk.json")
    lie_anim = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_yrpfrkpe.json")
    fingers_anim = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_5mdqni3z.json")
    coverage_anim = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_tllptwqk.json")
    shower_anim = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_5mdqni3z.json")
except:
    mirror_anim = arms_anim = lie_anim = fingers_anim = coverage_anim = shower_anim = None

# Initialize session state
if 'completed_steps' not in st.session_state:
    st.session_state.completed_steps = set()
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0

st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem;">
        <h1 style="color: #FF69B4; font-size: 3rem; margin-bottom: 1rem;" class="pulse-element">
            🖐️ Your Self-Examination Journey
        </h1>
        <p style="font-size: 1.3rem; color: #666;">
            Take it one step at a time - you're doing amazing! 🌟
        </p>
    </div>
    """, unsafe_allow_html=True)

# 🎯 ANIMATED PROGRESS BAR
total_steps = 6
progress = len(st.session_state.completed_steps) / total_steps

st.markdown(f"""
    <div style="margin: 3rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
            <span style="color: #FF69B4; font-weight: bold; font-size: 1.1rem;">
                Your Progress Journey
            </span>
            <span style="color: #FF69B4; font-weight: bold; font-size: 1.1rem;">
                {len(st.session_state.completed_steps)}/{total_steps} Steps
            </span>
        </div>
        <div class="progress-container">
            <div class="progress-bar" style="width: {progress * 100}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 📝 INTERACTIVE STEPS WITH ANIMATIONS
steps = [
    {
        "icon": "👀", "title": "Visual Inspection", 
        "description": "Stand in front of a mirror with your shoulders straight and arms on your hips. Look for any changes in size, shape, or color.",
        "tip": "💖 Be gentle with yourself - this is about loving awareness, not criticism",
        "animation": mirror_anim,
        "color": "#FF69B4"
    },
    {
        "icon": "🙌", "title": "Raise Your Arms", 
        "description": "Raise your arms and look for the same changes from different angles. Check for any fluid coming out of one or both nipples.",
        "tip": "🌈 You're building a powerful health habit - that's something to celebrate!",
        "animation": arms_anim,
        "color": "#EC4899"
    },
    {
        "icon": "🛌", "title": "Lie Down Comfortably", 
        "description": "Lie down and feel your breasts using your right hand to feel your left breast and then your left hand to feel your right breast.",
        "tip": "🎵 Put on some calming music - make this your special self-care time",
        "animation": lie_anim,
        "color": "#DB2777"
    },
    {
        "icon": "👆", "title": "Use Your Fingertips", 
        "description": "Use the pads of your fingers, keeping them flat and together. Use a circular motion, about the size of a quarter.",
        "tip": "💫 You're learning your body's unique landscape - how amazing is that!",
        "animation": fingers_anim,
        "color": "#BE185D"
    },
    {
        "icon": "🗺️", "title": "Cover Entire Breast", 
        "description": "Cover the entire breast from top to bottom, side to side — from your collarbone to the top of your abdomen, and from your armpit to your cleavage.",
        "tip": "🌟 Consistency creates confidence - you're building a lifelong health skill",
        "animation": coverage_anim,
        "color": "#9D174D"
    },
    {
        "icon": "🚿", "title": "Repeat Standing/Sitting", 
        "description": "Finally, feel your breasts while you are standing or sitting. Many women find this easiest in the shower.",
        "tip": "🎉 You did it! Regular checks are an beautiful act of self-love and care",
        "animation": shower_anim,
        "color": "#831843"
    }
]

# Display steps with amazing animations
for i, step in enumerate(steps):
    step_key = f"step_{i}"
    completed = step_key in st.session_state.completed_steps
    is_current = i == st.session_state.current_step
    
    # Animation delays for cascading effect
    animation_delay = f"animation-delay: {i * 0.2}s;"
    
    # Determine card classes
    card_classes = "step-card"
    if completed:
        card_classes += " completed-step"
    if is_current:
        card_classes += " current-step"
    
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
                <div class="{card_classes}" style="{animation_delay} border-left-color: {step['color']};">
                    <div style="display: flex; align-items: flex-start; margin-bottom: 1.5rem;">
                        <div class="step-icon" style="color: {step['color']}; margin-right: 1.5rem;">
                            {step['icon']}
                        </div>
                        <div style="flex: 1;">
                            <h3 style="color: {step['color']}; margin: 0 0 0.5rem 0; font-size: 1.5rem;">
                                Step {i+1}: {step['title']}
                            </h3>
                            <p style="color: #666; line-height: 1.6; margin: 0; font-size: 1.1rem;">
                                {step['description']}
                            </p>
                        </div>
                    </div>
                    
                    <div class="tip-bubble">
                        <strong style="color: {step['color']};">{step['tip']}</strong>
                    </div>
                    
                    <div style="display: flex; gap: 1rem; margin-top: 1.5rem;">
                        {"""
                        <button style="
                            background: linear-gradient(135deg, #4CAF50, #45a049);
                            color: white; border: none; padding: 0.8rem 1.5rem; 
                            border-radius: 25px; cursor: pointer; font-weight: 600;
                            transition: all 0.3s ease;
                        " onMouseOver="this.style.transform='translateY(-2px)'" 
                        onMouseOut="this.style.transform='translateY(0)'">
                            ✓ Mark Complete
                        </button>
                        """ if not completed else """
                        <div style="
                            background: #4CAF50; color: white; padding: 0.8rem 1.5rem; 
                            border-radius: 25px; font-weight: 600; display: inline-block;
                        ">
                            ✅ Completed!
                        </div>
                        """}
                        
                        <button style="
                            background: transparent; color: #FF69B4; border: 2px solid #FF69B4; 
                            padding: 0.8rem 1.5rem; border-radius: 25px; cursor: pointer; 
                            font-weight: 600; transition: all 0.3s ease;
                        " onMouseOver="this.style.background='#FF69B4'; this.style.color='white'" 
                        onMouseOut="this.style.background='transparent'; this.style.color='#FF69B4'">
                            ▶️ Practice This Step
                        </button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # Lottie animation for the step
            if step['animation']:
                st_lottie(
                    step['animation'],
                    speed=1,
                    reverse=False,
                    loop=True,
                    quality="low",
                    height=150,
                    width=150,
                    key=f"step_anim_{i}"
                )
        
        # Handle button interactions
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if not completed and st.button(f"✓ Complete Step {i+1}", key=f"complete_{i}", use_container_width=True):
                st.session_state.completed_steps.add(step_key)
                if i < total_steps - 1:
                    st.session_state.current_step = i + 1
                st.success(f"🎊 Wonderful! {step['title']} completed!")
                time.sleep(1)
                st.rerun()
        
        with col_btn2:
            if st.button(f"🔍 Focus on This Step", key=f"focus_{i}", use_container_width=True):
                st.session_state.current_step = i
                st.info(f"💪 Let's focus on {step['title']} together!")
                st.rerun()
        
        st.markdown("---")

# 🎉 COMPLETION CELEBRATION
if len(st.session_state.completed_steps) == total_steps:
    st.balloons()
    st.snow()
    
    st.markdown("""
        <div class="celebration-container">
            <h1 style="color: white; font-size: 3rem; margin-bottom: 1.5rem;">🎊 INCREDIBLE ACHIEVEMENT! 🎊</h1>
            <p style="font-size: 1.5rem; margin-bottom: 2rem; opacity: 0.9;">
                You've completed your self-examination journey! This is a powerful step in your health care.
            </p>
            <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 2rem;">
                <span class="bounce-element" style="font-size: 3rem;">🌟</span>
                <span class="bounce-element" style="font-size: 3rem; animation-delay: 0.2s;">💖</span>
                <span class="bounce-element" style="font-size: 3rem; animation-delay: 0.4s;">🎉</span>
                <span class="bounce-element" style="font-size: 3rem; animation-delay: 0.6s;">✨</span>
                <span class="bounce-element" style="font-size: 3rem; animation-delay: 0.8s;">🌸</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <h3 style="color: #FF69B4;">🎯 Keep Up the Amazing Work!</h3>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📅 Set Monthly Reminder", use_container_width=True):
            st.success("🔔 Monthly reminder set! You'll continue your amazing self-care journey.")
    
    with col2:
        if st.button("🔄 Practice Again", use_container_width=True):
            st.session_state.completed_steps = set()
            st.session_state.current_step = 0
            st.rerun()
    
    with col3:
        if st.button("🎊 Celebrate Again!", use_container_width=True):
            st.balloons()
            st.snow()

# 🌈 ENCOURAGEMENT SECTION
st.markdown("""
    <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #FFF0F5, #FFE4EC); border-radius: 25px; margin: 3rem 0;">
        <div class="floating-element" style="font-size: 4rem; margin-bottom: 1.5rem;">💫</div>
        <h2 style="color: #FF69B4; margin-bottom: 1rem;">You Are Amazing!</h2>
        <p style="font-size: 1.2rem; color: #666; line-height: 1.6; margin-bottom: 1.5rem;">
            Remember: Regular self-examination is about <strong>awareness, self-care, and empowerment</strong>. 
            You're building a loving, informed relationship with your body - and that's truly beautiful. 🌸
        </p>
        <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 1.5rem;">
            <span class="pulse-element">💪</span>
            <span class="pulse-element" style="animation-delay: 0.3s;">🌟</span>
            <span class="pulse-element" style="animation-delay: 0.6s;">💖</span>
            <span class="pulse-element" style="animation-delay: 0.9s;">🎯</span>
            <span class="pulse-element" style="animation-delay: 1.2s;">🌈</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 🎵 INTERACTIVE PRACTICE TIMER
with st.expander("⏰ Practice Session Timer"):
    st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h4 style="color: #FF69B4;">Set a timer for your practice session</h4>
            <p>Take your time and be present with yourself</p>
        </div>
        """, unsafe_allow_html=True)
    
    timer_cols = st.columns(4)
    with timer_cols[1]:
        if st.button("5 min 🕔", use_container_width=True):
            with st.spinner("⏰ 5-minute practice session starting now..."):
                time.sleep(3)  # Simulated timer
            st.success("🎉 Great job completing your 5-minute practice!")
    
    with timer_cols[2]:
        if st.button("10 min 🕙", use_container_width=True):
            with st.spinner("⏰ 10-minute practice session starting now..."):
                time.sleep(3)  # Simulated timer
            st.success("🎉 Amazing! 10 minutes of self-care completed!")