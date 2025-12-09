import streamlit as st
from utils.api_client import api_client
from utils.style_utils import apply_custom_styles
from datetime import date

def show():
    apply_custom_styles()
    
    st.markdown("## 📔 Symptom Journal")
    st.markdown("""
    <div style="background-color: #f3e5f5; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">
        <p style="color: #7b1fa2; margin: 0;">
            <b>Track your health:</b> Keeping a log helps you notice changes over time. 
            Share this history with your doctor during visits.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["✍️ New Entry", "📖 History"])
    
    with tab1:
        with st.form("journal_form"):
            entry_date = st.date_input("Date", value=date.today())
            
            st.markdown("##### Symptoms Observed")
            symptoms = st.multiselect(
                "Select all that apply:",
                ["Lump", "Pain", "Redness", "Discharge", "Swelling", "Fatigue", "Nausea", "Mood Swings"]
            )
            
            mood = st.select_slider(
                "How are you feeling?",
                options=["😞", "😐", "🙂", "😊", "🤩"],
                value="🙂"
            )
            
            notes = st.text_area("Notes", placeholder="Describe any changes or feelings...")
            
            submitted = st.form_submit_button("Save Entry 💾", type="primary")
            
            if submitted:
                with st.spinner("Saving..."):
                    result = api_client.add_journal_entry(entry_date, symptoms, notes, mood)
                    if "error" in result:
                        st.error("Failed to save entry.")
                    else:
                        st.success("Entry saved successfully!")
                        st.balloons()

    with tab2:
        st.subheader("Your Log History")
        entries = api_client.get_journal_entries()
        
        if not entries:
            st.info("No entries yet. Start logging today!")
        else:
            for entry in entries:
                with st.expander(f"{entry['date']} - {entry['mood']}"):
                    st.markdown(f"**Symptoms:** {', '.join(entry['symptoms'])}")
                    st.markdown(f"**Notes:** {entry['notes']}")
                    st.caption(f"ID: {entry['id']}")

if __name__ == "__main__":
    show()
