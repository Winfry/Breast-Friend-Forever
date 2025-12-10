from utils.backend_helper import call_backend_feature
import streamlit as st
from utils.api_client import api_client
from utils.style_utils import apply_custom_styles

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

    with st.form("symptom_form"):
        st.subheader("1. What are you feeling?")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Lumps or Thickness")
            symptom_lump = st.radio("Select best description:", 
                ["No lump", "Soft, movable lump", "Hard, fixed lump", "General thickening"],
                key="lump"
            )
            
            st.markdown("##### Skin Changes")
            symptom_skin = st.radio("Any skin changes?", 
                ["Normal", "Redness/Warmth", "Dimpling (like orange peel)", "Rash/Scaly"],
                key="skin"
            )

        with col2:
            st.markdown("##### Nipple Changes")
            symptom_nipple = st.radio("Any nipple changes?", 
                ["Normal", "Turned inward (Inverted)", "Bloody discharge", "Clear/Milky discharge"],
                key="nipple"
            )
            
            st.markdown("##### Pain")
            symptom_pain = st.radio("Are you in pain?", 
                ["No pain", "Cyclical (comes and goes with period)", "Constant pain"],
                key="pain_type"
            )

        st.subheader("2. Context")
        c1, c2, c3 = st.columns(3)
        with c1:
            pain_level = st.slider("Pain Level (0-10)", 0, 10, 0)
        with c2:
            duration = st.number_input("How many days has this lasted?", min_value=1, value=1)
        with c3:
            age = st.number_input("Your Age", min_value=15, max_value=100, value=30)
            
        st.subheader("3. Cycle Information")
        cycle_day = st.slider("Day of Menstrual Cycle (Day 1 = Start of Period)", 1, 35, 14)
        st.caption("If you don't have periods or are menopausal, leave as default.")

        submitted = st.form_submit_button("Analyze Symptoms 🩺", type="primary")

    if submitted:
        # Collect symptoms into a list
        symptoms_list = []
        if symptom_lump != "No lump": symptoms_list.append(symptom_lump)
        if symptom_skin != "Normal": symptoms_list.append(symptom_skin)
        if symptom_nipple != "Normal": symptoms_list.append(symptom_nipple)
        if symptom_pain != "No pain": symptoms_list.append(symptom_pain)
        
        if not symptoms_list:
            st.info("Please select at least one symptom for analysis.")
        else:
            with st.spinner("Consulting medical guidelines..."):
                result = api_client.analyze_symptoms(
                    symptoms=symptoms_list,
                    pain_level=pain_level,
                    duration=duration,
                    cycle_day=cycle_day,
                    age=age
                )
                
                if "error" in result:
                    st.error("Could not connect to the analysis engine. Please ensure the backend is running.")
                else:
                    # Display Results
                    st.markdown("---")
                    
                    # Risk Level Badge
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
