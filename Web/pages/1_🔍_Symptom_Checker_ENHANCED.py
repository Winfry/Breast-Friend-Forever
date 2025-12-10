import streamlit as st
from utils.api_client import api_client
from utils.style_utils import apply_custom_styles
from utils.backend_helper import call_backend_feature
import time

def show():
    apply_custom_styles()

    st.markdown("## 🔍 Interactive Symptom Checker")
    st.markdown("""
    <div style="background-color: #fce4ec; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">
        <p style="color: #c2185b; margin: 0;">
            <b>⚠️ Important:</b> This tool provides educational information based on medical guidelines. 
            It is <b>NOT</b> a diagnosis. Always consult a healthcare professional for any breast changes.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'symptom_location' not in st.session_state:
        st.session_state.symptom_location = None
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1

    # Progress bar
    progress = st.session_state.current_step / 4
    st.progress(progress)
    st.caption(f"Step {st.session_state.current_step} of 4")

    # Step 1: Location Selection with Visual Diagram
    st.markdown("---")
    st.subheader("📍 Step 1: Where are you feeling the symptom?")
    
    # Create a more visual breast diagram using emojis and styled buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fce4ec 0%, #f8bbd0 100%); 
                    padding: 2rem; border-radius: 15px; text-align: center;">
            <h4 style="margin-bottom: 1rem;">Click on the area</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Right Breast
        st.markdown('<div style="text-align: center; margin-top: 1rem;"><b>🔴 Right Breast</b></div>', unsafe_allow_html=True)
        r1, r2, r3, r4 = st.columns(4)
        
        with r1:
            if st.button("⬆️ Upper\nOuter", key="ruo", use_container_width=True):
                st.session_state.symptom_location = "Right Upper Outer"
                st.session_state.current_step = 2
                st.rerun()
        with r2:
            if st.button("⬆️ Upper\nInner", key="rui", use_container_width=True):
                st.session_state.symptom_location = "Right Upper Inner"
                st.session_state.current_step = 2
                st.rerun()
        with r3:
            if st.button("🎯 Nipple", key="rn", use_container_width=True):
                st.session_state.symptom_location = "Right Nipple"
                st.session_state.current_step = 2
                st.rerun()
        with r4:
            if st.button("💪 Armpit", key="ra", use_container_width=True):
                st.session_state.symptom_location = "Right Axilla"
                st.session_state.current_step = 2
                st.rerun()
        
        r5, r6, r7, r8 = st.columns(4)
        with r5:
            if st.button("⬇️ Lower\nOuter", key="rlo", use_container_width=True):
                st.session_state.symptom_location = "Right Lower Outer"
                st.session_state.current_step = 2
                st.rerun()
        with r6:
            if st.button("⬇️ Lower\nInner", key="rli", use_container_width=True):
                st.session_state.symptom_location = "Right Lower Inner"
                st.session_state.current_step = 2
                st.rerun()

        # Left Breast
        st.markdown('<div style="text-align: center; margin-top: 2rem;"><b>🔵 Left Breast</b></div>', unsafe_allow_html=True)
        l1, l2, l3, l4 = st.columns(4)
        
        with l1:
            if st.button("⬆️ Upper\nOuter", key="luo", use_container_width=True):
                st.session_state.symptom_location = "Left Upper Outer"
                st.session_state.current_step = 2
                st.rerun()
        with l2:
            if st.button("⬆️ Upper\nInner", key="lui", use_container_width=True):
                st.session_state.symptom_location = "Left Upper Inner"
                st.session_state.current_step = 2
                st.rerun()
        with l3:
            if st.button("🎯 Nipple", key="ln", use_container_width=True):
                st.session_state.symptom_location = "Left Nipple"
                st.session_state.current_step = 2
                st.rerun()
        with l4:
            if st.button("💪 Armpit", key="la", use_container_width=True):
                st.session_state.symptom_location = "Left Axilla"
                st.session_state.current_step = 2
                st.rerun()
        
        l5, l6, l7, l8 = st.columns(4)
        with l5:
            if st.button("⬇️ Lower\nOuter", key="llo", use_container_width=True):
                st.session_state.symptom_location = "Left Lower Outer"
                st.session_state.current_step = 2
                st.rerun()
        with l6:
            if st.button("⬇️ Lower\nInner", key="lli", use_container_width=True):
                st.session_state.symptom_location = "Left Lower Inner"
                st.session_state.current_step = 2
                st.rerun()

    # Show selected location with animation
    if st.session_state.symptom_location:
        st.success(f"✅ Selected: **{st.session_state.symptom_location}**")
        
        # Only show form if location is selected
        st.markdown("---")
        
        with st.form("symptom_form"):
            # Step 2: Symptoms
            st.subheader("🩺 Step 2: Describe your symptoms")
            
            col1, col2 = st.columns(2)
            
            with col1:
                symptom_lump = st.radio("Lumps or Thickness", 
                    ["No lump", "Soft, movable lump", "Hard, fixed lump", "General thickening"],
                    key="lump",
                    help="Select the option that best describes what you're feeling"
                )
                
                symptom_skin = st.radio("Skin Changes", 
                    ["Normal", "Redness/Warmth", "Dimpling (like orange peel)", "Rash/Scaly"],
                    key="skin",
                    help="Any visible changes to the skin?"
                )

            with col2:
                symptom_nipple = st.radio("Nipple Changes", 
                    ["Normal", "Turned inward (Inverted)", "Bloody discharge", "Clear/Milky discharge"],
                    key="nipple",
                    help="Any changes to the nipple area?"
                )
                
                symptom_pain = st.radio("Pain Level", 
                    ["No pain", "Cyclical (comes and goes with period)", "Constant pain"],
                    key="pain_type",
                    help="Does it hurt?"
                )

            # Conditional Pain Slider with emoji feedback
            pain_level = 0
            if symptom_pain != "No pain":
                pain_level = st.slider(
                    "How painful? (0 = No pain, 10 = Severe)", 
                    0, 10, 3,
                    help="Drag the slider to indicate pain intensity"
                )
                # Visual feedback for pain level
                if pain_level <= 3:
                    st.info("😊 Mild discomfort")
                elif pain_level <= 6:
                    st.warning("😣 Moderate pain")
                else:
                    st.error("😖 Severe pain - please see a doctor soon")

            # Step 3: Context
            st.markdown("---")
            st.subheader("📅 Step 3: Additional context")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                duration_days = st.number_input(
                    "How many days?", 
                    min_value=1, 
                    value=1,
                    help="How long have you noticed this?"
                )
                # Duration feedback
                if duration_days > 14:
                    st.caption("⏰ Persistent for 2+ weeks - worth checking")
            
            with c2:
                age = st.number_input(
                    "Your Age", 
                    min_value=15, 
                    max_value=100, 
                    value=30,
                    help="Age helps assess risk factors"
                )
            
            with c3:
                is_breastfeeding = st.checkbox(
                    "Currently Breastfeeding?",
                    help="Breastfeeding can cause normal changes"
                )
                
            # Step 4: Cycle Info
            st.markdown("---")
            st.subheader("🌸 Step 4: Menstrual cycle")
            
            cycle_day = st.slider(
                "Day of cycle (Day 1 = Start of period)", 
                1, 35, 14,
                help="Breast changes are normal during certain cycle phases"
            )
            
            # Cycle phase feedback
            if 1 <= cycle_day <= 7:
                st.caption("📅 Early cycle - breast tenderness is common")
            elif 20 <= cycle_day <= 28:
                st.caption("📅 Late cycle - PMS symptoms may occur")
            
            st.caption("💡 If you don't have periods or are menopausal, leave as default.")

            # Submit button with better styling
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button(
                "🔬 Analyze My Symptoms", 
                type="primary",
                use_container_width=True
            )

        # Process submission
        if submitted:
            symptoms_list = []
            if symptom_lump != "No lump": symptoms_list.append(symptom_lump)
            if symptom_skin != "Normal": symptoms_list.append(symptom_skin)
            if symptom_nipple != "Normal": symptoms_list.append(symptom_nipple)
            if symptom_pain != "No pain": symptoms_list.append(symptom_pain)
            
            if not symptoms_list:
                st.warning("⚠️ Please select at least one symptom for analysis.")
            else:
                symptom_data = {
                    "symptoms": symptoms_list,
                    "location": st.session_state.symptom_location,
                    "pain_level": pain_level,
                    "duration_days": duration_days,
                    "age": age,
                    "cycle_day": cycle_day,
                    "is_breastfeeding": is_breastfeeding
                }
                
                # Animated loading
                with st.spinner("🔬 Analyzing your symptoms..."):
                    time.sleep(1)  # Brief pause for UX
                    result = call_backend_feature("Symptom Checker", api_client.analyze_symptoms, symptom_data)
                    
                    if result and "error" not in result:
                        # Animated reveal
                        st.balloons()
                        
                        st.markdown("---")
                        st.markdown("## 📊 Your Results")
                        
                        # Risk level with color-coded badge
                        risk = result.get("risk_level", "Unknown")
                        urgency = result.get("urgency", "")
                        
                        if risk == "Low":
                            color = "#4caf50"
                            icon = "✅"
                            emoji = "😊"
                        elif risk == "Moderate":
                            color = "#ff9800"
                            icon = "⚠️"
                            emoji = "🤔"
                        else:
                            color = "#f44336"
                            icon = "🚨"
                            emoji = "😟"
                        
                        st.markdown(f"""
                        <div style="text-align: center; padding: 2rem; 
                                    background: linear-gradient(135deg, {color}20 0%, {color}40 100%); 
                                    border: 3px solid {color}; border-radius: 15px; margin-bottom: 2rem;">
                            <h1 style="color: {color}; margin:0; font-size: 3rem;">{icon}</h1>
                            <h2 style="color: {color}; margin:0.5rem 0;">Risk Level: {risk} {emoji}</h2>
                            <p style="font-size: 1.2rem; margin-top: 0.5rem;"><b>Urgency:</b> {urgency}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Analysis in expandable sections
                        with st.expander("📋 Detailed Analysis", expanded=True):
                            st.write(result.get("summary"))
                        
                        with st.expander("💡 Possible Causes"):
                            for cause in result.get("potential_causes", []):
                                st.markdown(f"• {cause}")
                        
                        with st.expander("🩺 Recommended Next Steps"):
                            st.info(result.get('recommendation'))
                        
                        # Action buttons
                        st.markdown("---")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("🏥 Find Nearest Hospital", use_container_width=True):
                                st.switch_page("pages/4_🏥_Find_Screening.py")
                        with col2:
                            if st.button("📔 Log in Journal", use_container_width=True):
                                st.switch_page("pages/3_📔_Journal.py")
                        with col3:
                            if st.button("💬 Ask AI Assistant", use_container_width=True):
                                st.switch_page("pages/2_💬_Chat_Assistant.py")
                        
                        # Reset button
                        if st.button("🔄 Check Another Symptom", type="secondary", use_container_width=True):
                            st.session_state.symptom_location = None
                            st.session_state.current_step = 1
                            st.rerun()
                    else:
                        st.error("❌ Could not analyze symptoms. Please try again or contact support.")
    else:
        st.info("👆 Please select a location above to continue")

if __name__ == "__main__":
    show()
