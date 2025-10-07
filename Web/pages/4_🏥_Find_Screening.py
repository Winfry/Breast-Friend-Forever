import streamlit as st
import requests

st.set_page_config(page_title="Find Screening", page_icon="🏥")

st.markdown("# 🏥 Find Screening Locations") 
st.caption("Locate breast cancer screening centers near you")

# 🏥 Sample Hospital Data (in real app, from backend API)
hospitals = [
    {
        "id": 1,
        "name": "Nairobi Women's Hospital",
        "address": "James Gichuru Road", 
        "city": "Nairobi",
        "phone": "+254 20 272 6000",
        "services": "Mammography, Ultrasound, Biopsy, Breast Surgery"
    },
    {
        "id": 2,
        "name": "Aga Khan University Hospital",
        "address": "3rd Parklands Avenue",
        "city": "Nairobi",
        "phone": "+254 20 366 2000", 
        "services": "Mammography, MRI, Genetic Testing, Oncology"
    },
    {
        "id": 3,
        "name": "Mombasa Women's Hospital",
        "address": "Nyerere Avenue",
        "city": "Mombasa",
        "phone": "+254 41 222 3851",
        "services": "Mammography, Ultrasound, Women's Health"
    }
]

# 🔍 Search Interface
col1, col2 = st.columns([2, 1])
with col1:
    search_city = st.text_input("Search by city", placeholder="e.g., Nairobi, Mombasa...")
with col2:
    search_state = st.text_input("State", placeholder="e.g., Nairobi County")

# 📍 Search Functionality
if st.button("🔍 Search Locations", use_container_width=True):
    filtered_hospitals = hospitals
    
    # Apply city filter
    if search_city:
        filtered_hospitals = [h for h in filtered_hospitals if search_city.lower() in h['city'].lower()]
    
    # Apply state filter (if we had state data)
    if search_state:
        filtered_hospitals = [h for h in filtered_hospitals if search_state.lower() in h.get('state', '').lower()]
    
    # Display results
    if filtered_hospitals:
        for hospital in filtered_hospitals:
            st.markdown(f"""
            <div style="border: 1px solid #FF69B4; border-radius: 10px; padding: 1rem; margin: 0.5rem 0;">
                <h4 style="color: #FF69B4; margin: 0;">{hospital['name']}</h4>
                <p style="margin: 0.25rem 0;">📍 {hospital['address']}, {hospital['city']}</p>
                <p style="margin: 0.25rem 0;">📞 {hospital['phone']}</p>
                <p style="margin: 0.25rem 0;">🩺 {hospital['services']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No screening centers found. Try a different search.")

# 🏙️ Quick City Search Buttons
st.markdown("### 🏙️ Quick Search")
cities = ["Nairobi", "Mombasa", "Kisumu", "Nakuru"]
cols = st.columns(4)
for i, city in enumerate(cities):
    with cols[i]:
        if st.button(city, use_container_width=True):
            st.session_state.search_city = city
            st.rerun()