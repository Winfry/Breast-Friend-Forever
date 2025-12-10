import streamlit as st
from utils.api_client import api_client
from utils.style_utils import apply_custom_styles
from utils.backend_helper import call_backend_feature
import time
from datetime import datetime
import json

# Multi-language support
TRANSLATIONS = {
    "en": {
        "title": "🔍 Interactive Symptom Checker",
        "warning": "⚠️ Important: This tool provides educational information based on medical guidelines. It is NOT a diagnosis. Always consult a healthcare professional for any breast changes.",
        "step1": "📍 Step 1: Where are you feeling the symptom?",
        "step2": "🩺 Step 2: Describe your symptoms",
        "step3": "📅 Step 3: Additional context",
        "step4": "🌸 Step 4: Menstrual cycle",
        "analyze": "🔬 Analyze My Symptoms",
        "select_location": "Please select a location above to continue",
        "results": "📊 Your Results",
        "risk_level": "Risk Level",
        "urgency": "Urgency"
    },
    "sw": {  # Swahili
        "title": "🔍 Kipima Dalili cha Maingiliano",
        "warning": "⚠️ Muhimu: Zana hii inatoa taarifa za elimu kulingana na miongozo ya kimatibabu. Sio utambuzi. Daima wasiliana na mtaalamu wa afya kwa mabadiliko yoyote ya kifua.",
        "step1": "📍 Hatua ya 1: Unahisi dalili wapi?",
        "step2": "🩺 Hatua ya 2: Eleza dalili zako",
        "step3": "📅 Hatua ya 3: Muktadha wa ziada",
        "step4": "🌸 Hatua ya 4: Mzunguko wa hedhi",
        "analyze": "🔬 Tathmini Dalili Zangu",
        "select_location": "Tafadhali chagua eneo hapo juu ili kuendelea",
        "results": "📊 Matokeo Yako",
        "risk_level": "Kiwango cha Hatari",
        "urgency": "Dharura"
    },
    "fr": {  # French
        "title": "🔍 Vérificateur de Symptômes Interactif",
        "warning": "⚠️ Important: Cet outil fournit des informations éducatives basées sur des directives médicales. Ce n'est PAS un diagnostic. Consultez toujours un professionnel de santé pour tout changement mammaire.",
        "step1": "📍 Étape 1: Où ressentez-vous le symptôme?",
        "step2": "🩺 Étape 2: Décrivez vos symptômes",
        "step3": "📅 Étape 3: Contexte supplémentaire",
        "step4": "🌸 Étape 4: Cycle menstruel",
        "analyze": "🔬 Analyser Mes Symptômes",
        "select_location": "Veuillez sélectionner un emplacement ci-dessus pour continuer",
        "results": "📊 Vos Résultats",
        "risk_level": "Niveau de Risque",
        "urgency": "Urgence"
    }
}

def show():
    apply_custom_styles()

    # Language selector
    col1, col2, col3 = st.columns([3, 1, 1])
    with col3:
        lang = st.selectbox("🌍", ["en", "sw", "fr"], format_func=lambda x: {"en": "English", "sw": "Swahili", "fr": "Français"}[x], label_visibility="collapsed")
    
    t = TRANSLATIONS[lang]

    st.markdown(f"## {t['title']}")
    st.markdown(f"""
    <div style="background-color: #fce4ec; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">
        <p style="color: #c2185b; margin: 0;">
            {t['warning']}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'symptom_location' not in st.session_state:
        st.session_state.symptom_location = None
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'symptom_history' not in st.session_state:
        st.session_state.symptom_history = []

    # Progress bar
    progress = st.session_state.current_step / 4
    st.progress(progress)
    st.caption(f"Step {st.session_state.current_step} of 4")

    # History comparison
    if st.session_state.symptom_history:
        with st.expander(f"📜 History ({len(st.session_state.symptom_history)} previous checks)"):
            for i, check in enumerate(reversed(st.session_state.symptom_history[-5:])):  # Last 5
                st.caption(f"**{check['date']}** - {check['location']} - Risk: {check['risk']}")

    # Step 1: Location Selection
    st.markdown("---")
    st.subheader(t['step1'])
    
    # Breast diagram with horizontal layout
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fce4ec 0%, #f8bbd0 100%); 
                padding: 1.5rem; border-radius: 15px; text-align: center; margin: 1rem auto; max-width: 800px;">
        <h4 style="margin-bottom: 0.5rem;">Click on the area where you feel the symptom</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Right Breast - Horizontal Layout
    st.markdown('<div style="text-align: center; margin-top: 1.5rem;"><b>🔴 Right Breast</b></div>', unsafe_allow_html=True)
    
    # Row 1: Upper quadrants + Nipple + Armpit
    r_cols = st.columns([1, 1, 1, 1])
    if r_cols[0].button("⬆️ Upper Outer", key="ruo", use_container_width=True):
        st.session_state.symptom_location = "Right Upper Outer"
        st.session_state.current_step = 2
        st.rerun()
    if r_cols[1].button("⬆️ Upper Inner", key="rui", use_container_width=True):
        st.session_state.symptom_location = "Right Upper Inner"
        st.session_state.current_step = 2
        st.rerun()
    if r_cols[2].button("🎯 Nipple", key="rn", use_container_width=True):
        st.session_state.symptom_location = "Right Nipple"
        st.session_state.current_step = 2
        st.rerun()
    if r_cols[3].button("💪 Armpit", key="ra", use_container_width=True):
        st.session_state.symptom_location = "Right Axilla"
        st.session_state.current_step = 2
        st.rerun()
    
    # Row 2: Lower quadrants
    r_cols2 = st.columns([1, 1, 2])
    if r_cols2[0].button("⬇️ Lower Outer", key="rlo", use_container_width=True):
        st.session_state.symptom_location = "Right Lower Outer"
        st.session_state.current_step = 2
        st.rerun()
    if r_cols2[1].button("⬇️ Lower Inner", key="rli", use_container_width=True):
        st.session_state.symptom_location = "Right Lower Inner"
        st.session_state.current_step = 2
        st.rerun()

    # Left Breast - Horizontal Layout
    st.markdown('<div style="text-align: center; margin-top: 2rem;"><b>🔵 Left Breast</b></div>', unsafe_allow_html=True)
    
    # Row 1: Upper quadrants + Nipple + Armpit
    l_cols = st.columns([1, 1, 1, 1])
    if l_cols[0].button("⬆️ Upper Outer", key="luo", use_container_width=True):
        st.session_state.symptom_location = "Left Upper Outer"
        st.session_state.current_step = 2
        st.rerun()
    if l_cols[1].button("⬆️ Upper Inner", key="lui", use_container_width=True):
        st.session_state.symptom_location = "Left Upper Inner"
        st.session_state.current_step = 2
        st.rerun()
    if l_cols[2].button("🎯 Nipple", key="ln", use_container_width=True):
        st.session_state.symptom_location = "Left Nipple"
        st.session_state.current_step = 2
        st.rerun()
    if l_cols[3].button("💪 Armpit", key="la", use_container_width=True):
        st.session_state.symptom_location = "Left Axilla"
        st.session_state.current_step = 2
        st.rerun()
    
    # Row 2: Lower quadrants
    l_cols2 = st.columns([1, 1, 2])
    if l_cols2[0].button("⬇️ Lower Outer", key="llo", use_container_width=True):
        st.session_state.symptom_location = "Left Lower Outer"
        st.session_state.current_step = 2
        st.rerun()
    if l_cols2[1].button("⬇️ Lower Inner", key="lli", use_container_width=True):
        st.session_state.symptom_location = "Left Lower Inner"
        st.session_state.current_step = 2
        st.rerun()

    if st.session_state.symptom_location:
        st.success(f"✅ Selected: **{st.session_state.symptom_location}**")
        
        st.markdown("---")
        
        with st.form("symptom_form"):
            st.subheader(t['step2'])
            
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

            pain_level = 0
            if symptom_pain != "No pain":
                pain_level = st.slider(
                    "How painful? (0 = No pain, 10 = Severe)", 
                    0, 10, 3,
                    help="Drag the slider to indicate pain intensity"
                )
                if pain_level <= 3:
                    st.info("😊 Mild discomfort")
                elif pain_level <= 6:
                    st.warning("😣 Moderate pain")
                else:
                    st.error("😖 Severe pain - please see a doctor soon")

            st.markdown("---")
            st.subheader(t['step3'])
            
            c1, c2, c3 = st.columns(3)
            with c1:
                duration_days = st.number_input(
                    "How many days?", 
                    min_value=1, 
                    value=1,
                    help="How long have you noticed this?"
                )
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
                
            st.markdown("---")
            st.subheader(t['step4'])
            
            cycle_day = st.slider(
                "Day of cycle (Day 1 = Start of period)", 
                1, 35, 14,
                help="Breast changes are normal during certain cycle phases"
            )
            
            if 1 <= cycle_day <= 7:
                st.caption("📅 Early cycle - breast tenderness is common")
            elif 20 <= cycle_day <= 28:
                st.caption("📅 Late cycle - PMS symptoms may occur")
            
            st.caption("💡 If you don't have periods or are menopausal, leave as default.")

            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button(
                t['analyze'], 
                type="primary",
                use_container_width=True
            )

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
                
                with st.spinner("🔬 Analyzing your symptoms..."):
                    time.sleep(1)
                    result = call_backend_feature("Symptom Checker", api_client.analyze_symptoms, symptom_data)
                    
                    if result and "error" not in result:
                        st.balloons()
                        
                        # Save to history
                        st.session_state.symptom_history.append({
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "location": st.session_state.symptom_location,
                            "risk": result.get("risk_level", "Unknown"),
                            "symptoms": symptoms_list,
                            "result": result
                        })
                        
                        st.markdown("---")
                        st.markdown(f"## {t['results']}")
                        
                        risk = result.get("risk_level", "Unknown")
                        urgency = result.get("urgency", "")
                        
                        if risk == "Low":
                            color, icon, emoji = "#4caf50", "✅", "😊"
                        elif risk == "Moderate":
                            color, icon, emoji = "#ff9800", "⚠️", "🤔"
                        else:
                            color, icon, emoji = "#f44336", "🚨", "😟"
                        
                        st.markdown(f"""
                        <div style="text-align: center; padding: 2rem; 
                                    background: linear-gradient(135deg, {color}20 0%, {color}40 100%); 
                                    border: 3px solid {color}; border-radius: 15px; margin-bottom: 2rem;">
                            <h1 style="color: {color}; margin:0; font-size: 3rem;">{icon}</h1>
                            <h2 style="color: {color}; margin:0.5rem 0;">{t['risk_level']}: {risk} {emoji}</h2>
                            <p style="font-size: 1.2rem; margin-top: 0.5rem;"><b>{t['urgency']}:</b> {urgency}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("📋 Detailed Analysis", expanded=True):
                            st.write(result.get("summary"))
                        
                        with st.expander("💡 Possible Causes"):
                            for cause in result.get("potential_causes", []):
                                st.markdown(f"• {cause}")
                        
                        with st.expander("🩺 Recommended Next Steps"):
                            st.info(result.get('recommendation'))
                        
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
                        
                        if st.button("🔄 Check Another Symptom", type="secondary", use_container_width=True):
                            st.session_state.symptom_location = None
                            st.session_state.current_step = 1
                            st.rerun()
                    else:
                        st.error("❌ Could not analyze symptoms. Please try again.")
    else:
        st.info(f"👆 {t['select_location']}")

if __name__ == "__main__":
    show()
