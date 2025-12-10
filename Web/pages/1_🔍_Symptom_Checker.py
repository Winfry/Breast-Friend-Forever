import streamlit as st
from utils.api_client import api_client
from utils.style_utils import apply_custom_styles
from utils.backend_helper import call_backend_feature

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

    # Initialize session state for location
    if 'symptom_location' not in st.session_state:
        st.session_state.symptom_location = None

    def set_location(location):
        st.session_state.symptom_location = location

    st.subheader("1. Where are you feeling the symptom?")
    st.write("Click a button to select the area.")

    # Create a more visual and interactive layout for location selection
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Breast diagram
        st.markdown('<div style="text-align: center;"><b>Right Breast</b></div>', unsafe_allow_html=True)
        _, r_upper_outer, r_upper_inner, _ = st.columns(4)
        r_upper_outer.button("Upper Outer", on_click=set_location, args=("Right Upper Outer",))
        r_upper_inner.button("Upper Inner", on_click=set_location, args=("Right Upper Inner",))
        
        r_axilla, r_lower_outer, r_lower_inner, r_nipple = st.columns(4)
        r_lower_outer.button("Lower Outer", on_click=set_location, args=("Right Lower Outer",))
        r_lower_inner.button("Lower Inner", on_click=set_location, args=("Right Lower Inner",))
        r_nipple.button("Nipple", on_click=set_location, args=("Right Nipple",))
        r_axilla.button("Armpit", on_click=set_location, args=("Right Axilla",))

        st.markdown('<div style="text-align: center; margin-top: 1rem;"><b>Left Breast</b></div>', unsafe_allow_html=True)
        _, l_upper_outer, l_upper_inner, _ = st.columns(4)
        l_upper_outer.button("Upper Outer", on_click=set_location, args=("Left Upper Outer",), key="luo")
        l_upper_inner.button("Upper Inner", on_click=set_location, args=("Left Upper Inner",), key="lui")

        l_axilla, l_lower_outer, l_lower_inner, l_nipple = st.columns(4)
        l_lower_outer.button("Lower Outer", on_click=set_location, args=("Left Lower Outer",), key="llo")
        l_lower_inner.button("Lower Inner", on_click=set_location, args=("Left Lower Inner",), key="lli")
        l_nipple.button("Nipple", on_click=set_location, args=("Left Nipple",), key="ln")
        l_axilla.button("Armpit", on_click=set_location, args=("Left Axilla",), key="la")

    if st.session_state.symptom_location:
        st.success(f"Selected Location: **{st.session_state.symptom_location}**")

    with st.form("symptom_form"):
        st.subheader("2. What are you feeling?")
        
        symptom_lump = st.selectbox("Lumps or Thickness", 
            ["No lump", "Soft, movable lump", "Hard, fixed lump", "General thickening"],
            key="lump"
        )
        
        symptom_skin = st.selectbox("Skin Changes", 
            ["Normal", "Redness/Warmth", "Dimpling (like orange peel)", "Rash/Scaly"],
            key="skin"
        )

        symptom_nipple = st.selectbox("Nipple Changes", 
            ["Normal", "Turned inward (Inverted)", "Bloody discharge", "Clear/Milky discharge"],
            key="nipple"
        )
        
        symptom_pain = st.radio("Are you in pain?", 
            ["No pain", "Cyclical (comes and goes with period)", "Constant pain"],
            key="pain_type"
        )

        # Conditional Pain Slider
        pain_level = None
        if symptom_pain != "No pain":
            pain_level = st.slider("Pain Level (0-10)", 0, 10, 3)

        st.subheader("3. Context")
        c1, c2, c3 = st.columns(3)
        with c1:
            duration_days = st.number_input("How many days has this lasted?", min_value=1, value=1)
        with c2:
            age = st.number_input("Your Age", min_value=15, max_value=100, value=30)
        with c3:
            is_breastfeeding = st.checkbox("Currently Breastfeeding?")
            
        st.subheader("4. Cycle Information")
        cycle_day = st.slider("Day of Menstrual Cycle (Day 1 = Start of Period)", 1, 35, 14)
        st.caption("If you don't have periods or are menopausal, leave as default.")

        submitted = st.form_submit_button("Analyze Symptoms 🩺", type="primary")

    if submitted:
        symptoms_list = []
        if symptom_lump != "No lump": symptoms_list.append(symptom_lump)
        if symptom_skin != "Normal": symptoms_list.append(symptom_skin)
        if symptom_nipple != "Normal": symptoms_list.append(symptom_nipple)
        if symptom_pain != "No pain": symptoms_list.append(symptom_pain)
        
        if not symptoms_list and not st.session_state.symptom_location:
            st.warning("Please select a symptom location and describe at least one symptom.")
        elif not symptoms_list:
            st.warning("Please select at least one symptom for analysis.")
        elif not st.session_state.symptom_location:
            st.warning("Please select the location of the symptom.")
        else:
            symptom_data = {
                "symptoms": symptoms_list,
                "location": st.session_state.symptom_location,
                "pain_level": pain_level if pain_level is not None else 0,
                "duration_days": duration_days,
                "age": age,
                "cycle_day": cycle_day,
                "is_breastfeeding": is_breastfeeding
            }
            with st.spinner("Consulting medical guidelines..."):
                result = call_backend_feature("Symptom Checker", api_client.analyze_symptoms, symptom_data)
                
                if "error" in result:
                    st.error(f"Could not connect to the analysis engine: {result['error']}")
                else:
                    st.markdown("---")
                    risk = result.get("risk_level", "Unknown")
                    color = "#4caf50" if risk == "Low" else "#ff9800" if risk == "Moderate" else "#f44336"
                    
                    st.markdown(f"""
                    <div style="text-align: center; padding: 1rem; background-color: {color}20; border: 2px solid {color}; border-radius: 10px;">
                        <h2 style="color: {color}; margin:0;">Risk Assessment: {risk}</h2>
                        <p style="margin-top: 0.5rem;"><b>Urgency:</b> {result.get('urgency')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"### 📋 Analysis")
                    st.write(result.get("summary"))
                    
                    st.markdown("### 💡 Potential Causes")
                    for cause in result.get("potential_causes", []):
                        st.markdown(f"- {cause}")
                        
                    st.info(f"**Recommendation:** {result.get('recommendation')}")

if __name__ == "__main__":
    show()
