import streamlit as st
from utils.api_client import api_client
from utils.style_utils import apply_custom_styles
from datetime import date, timedelta

def show():
    apply_custom_styles()
    
    st.markdown("## 📅 Smart Cycle Reminders")
    st.markdown("""
    <div style="background-color: #e3f2fd; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">
        <p style="color: #0d47a1; margin: 0;">
            <b>Why track?</b> Your breasts change throughout your cycle. 
            The best time to check is when hormones are stable (Day 7-10), usually 3-5 days after your period ends.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Your Cycle Details")
        with st.form("cycle_form"):
            last_period = st.date_input(
                "When did your last period START?",
                value=date.today() - timedelta(days=14),
                max_value=date.today()
            )
            
            cycle_length = st.slider(
                "Average Cycle Length (Days)", 
                min_value=21, 
                max_value=35, 
                value=28
            )
            
            submitted = st.form_submit_button("Calculate Best Date 🗓️", type="primary")

    with col2:
        if submitted:
            with st.spinner("Calculating optimal window..."):
                result = api_client.calculate_reminders(last_period, cycle_length)
                
                if "error" in result:
                    st.error("Could not connect to reminder service.")
                else:
                    best_date = result.get("best_exam_date")
                    next_period = result.get("next_period_date")
                    
                    st.markdown("### 🎯 Your Personal Exam Date")
                    
                    st.markdown(f"""
                    <div style="text-align: center; padding: 2rem; background-color: #fce4ec; border-radius: 15px; border: 2px dashed #e91e63;">
                        <h1 style="color: #e91e63; margin:0;">{best_date}</h1>
                        <p style="color: #880e4f; font-weight: bold;">Best Day for Self-Exam</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.success(result.get("message"))
                    
                    st.info(f"🩸 Next period expected around: **{next_period}**")
                    
                    st.button("🔔 Set Calendar Reminder (Demo)", disabled=True, help="Calendar integration coming soon!")

if __name__ == "__main__":
    show()
