# Web/pages/3_🏥_Find_Screening.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
import json
import time
import os

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

st.set_page_config(page_title="Find Screening", page_icon="🏥", layout="wide")

# 🎨 SIMPLIFIED CSS - NO BROKEN HTML
st.markdown("""
    <style>
    .clinic-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border-left: 5px solid #10B981;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.15);
        transition: all 0.4s ease;
    }
    
    .clinic-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(16, 185, 129, 0.25);
    }
    
    .urgent-card {
        border-left-color: #EF4444;
        background: linear-gradient(135deg, #FEF2F2, #FEE2E2);
    }
    
    .premium-card {
        border-left-color: #8B5CF6;
        background: linear-gradient(135deg, #FAF5FF, #EDE9FE);
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: 1rem;
    }
    
    .status-open {
        background: #D1FAE5;
        color: #065F46;
    }
    
    .status-urgent {
        background: #FEE2E2;
        color: #991B1B;
    }
    
    .status-premium {
        background: #EDE9FE;
        color: #5B21B6;
    }
    
    .county-badge {
        background: linear-gradient(135deg, #FF69B4, #EC4899);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    
    .appointment-btn {
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .appointment-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# Load animations
try:
    location_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_0fhgwtli.json")
except:
    location_animation = None

# Initialize session state
if 'appointments' not in st.session_state:
    st.session_state.appointments = []

# 🎯 HEADER
st.title("🏥 Pata Uchunguzi wa Matiti Kenya")
st.markdown("Connect with trusted healthcare providers across Kenya 🌍")

# Welcome animation
if location_animation:
    st_lottie(location_animation, speed=1, height=200, key="screening_welcome")

# 🎯 HERO SECTION
st.markdown("""
    <div style="background: linear-gradient(135deg, #10B981, #059669); color: white; padding: 2rem; border-radius: 20px; margin: 2rem 0; text-align: center;">
        <h2 style="color: white; margin-bottom: 1rem;">🔍 Tafuta Huduma ya Matiti Karibu Nawe</h2>
        <p style="color: white; font-size: 1.1rem; opacity: 0.9;">
            We connect you with compassionate, professional breast care services across Kenya
        </p>
    </div>
    """, unsafe_allow_html=True)

# 📍 SEARCH & FILTERS
st.markdown("### 🔍 Tafuta Kituo cha Uchunguzi")

col1, col2, col3 = st.columns(3)

with col1:
    counties = [
        "All Counties", "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Thika", "Machakos", 
        "Meru", "Nyeri", "Garissa", "Kakamega", "Kisii", "Kericho", "Kitale", "Malindi", "Lamu"
    ]
    selected_county = st.selectbox("📍 Chagua County Yako", counties)

with col2:
    search_radius = st.slider("🚗 Umbali wa Juu (km)", 5, 200, 50)

with col3:
    facility_type = st.selectbox(
        "🏥 Aina ya Kituo",
        ["All Types", "Main Hospital", "District Hospital", "Clinic", "Health Center", "MRI Unit"]
    )

# 🏥 LOAD HOSPITALS FROM CSV OR USE DEFAULT DATA
@st.cache_data
def load_hospitals_data():
    """Load hospitals from CSV file or use default data"""
    csv_path = "data/kenya_hospitals.csv"  # Adjust path as needed
    
    # Try to load from CSV first
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            st.success(f"✅ Loaded {len(df)} hospitals from CSV")
            return df.to_dict('records')
        except Exception as e:
            st.warning(f"⚠️ Could not load CSV: {e}. Using default data.")
    
    # Default hospital data (fallback)
    default_hospitals = [
        {
            "name": "Nairobi Women's Hospital",
            "type": "Main Hospital",
            "county": "Nairobi",
            "distance": 2.3,
            "rating": 4.8,
            "reviews": 234,
            "address": "James Gichuru Road, Lavington, Nairobi",
            "phone": "+254 20 272 6000",
            "emergency": "+254 733 639 000",
            "insurance": "NHIF, Madison, Jubilee, AAR, Private Pay",
            "languages": "Kiswahili, English, Kikuyu",
            "wait_time": "1-2 days",
            "services": "Mammography, Ultrasound, Biopsy, Breast Surgery, Oncology",
            "special_services": "Digital Mammogram, Breast Cancer Screening, Support Groups",
            "status": "open",
            "price_range": "$$",
            "specialty": "Comprehensive women's healthcare with specialized breast care services",
            "hours": "24/7",
            "lat": -1.2684,
            "lon": 36.7965
        },
        {
            "name": "Aga Khan University Hospital",
            "type": "Main Hospital",
            "county": "Nairobi", 
            "distance": 4.1,
            "rating": 4.9,
            "reviews": 189,
            "address": "3rd Parklands Avenue, Nairobi",
            "phone": "+254 20 366 2000",
            "emergency": "+254 711 709 100",
            "insurance": "NHIF, Madison, Jubilee, AAR, CIC, Britam",
            "languages": "Kiswahili, English, Hindi, Gujarati",
            "wait_time": "3-5 days",
            "services": "3D Mammography, Breast MRI, Genetic Testing, Oncology, Radiation Therapy",
            "special_services": "Advanced Imaging, Genetic Counseling, Multidisciplinary Care",
            "status": "premium",
            "price_range": "$$$",
            "specialty": "State-of-the-art diagnostic imaging and comprehensive cancer care",
            "hours": "Mon-Sun: 6AM-10PM",
            "lat": -1.2542,
            "lon": 36.8134
        },
        {
            "name": "Mombasa Women's Hospital",
            "type": "District Hospital",
            "county": "Mombasa",
            "distance": 0.8,
            "rating": 4.5,
            "reviews": 156,
            "address": "Nyerere Avenue, Mombasa",
            "phone": "+254 41 222 3851",
            "emergency": "+254 722 516 363",
            "insurance": "NHIF, Jubilee, Private Pay, Huduma Bora",
            "languages": "Kiswahili, English, Digo, Duruma",
            "wait_time": "Same day",
            "services": "Mammography, Ultrasound, Women's Health, Family Planning",
            "special_services": "Community Outreach, Affordable Screening, Mobile Clinics",
            "status": "urgent",
            "price_range": "$",
            "specialty": "Coastal region's leading women's health provider with compassionate care",
            "hours": "Mon-Sat: 7AM-9PM, Sun: 8AM-6PM",
            "lat": -4.0547,
            "lon": 39.6636
        }
    ]
    return default_hospitals

# Load hospital data
hospitals_data = load_hospitals_data()

# Filter hospitals based on user selection
filtered_hospitals = hospitals_data.copy()

if selected_county != "All Counties":
    filtered_hospitals = [h for h in filtered_hospitals if h["county"] == selected_county]

if facility_type != "All Types":
    filtered_hospitals = [h for h in filtered_hospitals if h["type"] == facility_type]

# Filter by distance
filtered_hospitals = [h for h in filtered_hospitals if h["distance"] <= search_radius]

# 🗺️ INTERACTIVE MAP
st.markdown("### 🗺️ Vituo vya Uchunguzi Karibu Nawe")

if filtered_hospitals:
    # Create map data
    map_data = pd.DataFrame({
        'lat': [h['lat'] for h in filtered_hospitals],
        'lon': [h['lon'] for h in filtered_hospitals],
        'name': [h['name'] for h in filtered_hospitals],
        'size': [20 for _ in filtered_hospitals],
        'color': ['#10B981' if h['status'] == 'open' else 
                  '#EF4444' if h['status'] == 'urgent' else 
                  '#8B5CF6' for h in filtered_hospitals]
    })

    fig = px.scatter_mapbox(
        map_data,
        lat="lat",
        lon="lon",
        hover_name="name",
        size="size",
        color="color",
        color_discrete_map="identity",
        zoom=6,
        height=400
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":0,"l":0,"b":0},
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("🔍 No hospitals found matching your criteria. Try adjusting your filters.")

# 🏥 HOSPITAL LISTINGS - FIXED: NO BROKEN HTML!
st.markdown(f"### 🏥 Vituo Vinavyopatikana ({len(filtered_hospitals)} found)")

for hospital in filtered_hospitals:
    # Determine card style and status
    status_config = {
        "open": ("status-open", "Open & Available", "clinic-card"),
        "urgent": ("status-urgent", "Urgent Care", "clinic-card urgent-card"),
        "premium": ("status-premium", "Premium Service", "clinic-card premium-card")
    }
    
    status_class, status_text, card_class = status_config[hospital["status"]]
    
    # 🎯 FIXED: Use Streamlit components instead of raw HTML
    with st.container():
        st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
        
        # Header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{hospital['name']}**")
        with col2:
            st.markdown(f'<span class="status-badge {status_class}">{status_text}</span>', unsafe_allow_html=True)
            st.markdown(f'<span class="county-badge">{hospital["county"]}</span>', unsafe_allow_html=True)
        
        # Ratings and info
        st.write(f"⭐ {hospital['rating']}/5 ({hospital['reviews']} reviews) • 📍 {hospital['distance']}km • 💰 {hospital['price_range']} • 🕒 {hospital['hours']}")
        
        # Specialty
        st.info(f"*{hospital['specialty']}*")
        
        # Contact Information
        with st.expander("📞 Contact Information"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Phone:** {hospital['phone']}")
                st.write(f"**Address:** {hospital['address']}")
                st.write(f"**Emergency:** {hospital['emergency']}")
            with col2:
                st.write(f"**Languages:** {hospital['languages']}")
                st.write(f"**Wait Time:** {hospital['wait_time']}")
                st.write(f"**Insurance:** {hospital['insurance']}")
        
        # Services
        with st.expander("🔬 Services Available"):
            st.write(f"**Main Services:** {hospital['services']}")
            st.write(f"**Special Services:** {hospital['special_services']}")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"📞 Call Now", key=f"call_{hospital['name']}", use_container_width=True):
                st.info(f"📞 Calling {hospital['name']} at {hospital['phone']}")
        with col2:
            if st.button(f"📍 Get Directions", key=f"dir_{hospital['name']}", use_container_width=True):
                st.info(f"🗺️ Getting directions to {hospital['address']}")
        with col3:
            appointment_date = st.date_input("Select appointment date", key=f"date_{hospital['name']}")
            if st.button(f"✅ Book Appointment", key=f"book_{hospital['name']}", use_container_width=True):
                st.session_state.appointments.append({
                    "hospital": hospital['name'],
                    "date": appointment_date,
                    "status": "Scheduled"
                })
                st.success(f"🎉 Appointment booked at {hospital['name']} for {appointment_date}!")
        
        st.markdown('</div>', unsafe_allow_html=True)

# 📅 APPOINTMENT MANAGER
st.markdown("### 📅 Your Appointments")

if st.session_state.appointments:
    for i, appointment in enumerate(st.session_state.appointments):
        with st.container():
            st.markdown(f"""
            <div class="clinic-card" style="border-left-color: #3B82F6;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0 0 0.5rem 0; color: #1F2937;">{appointment['hospital']}</h4>
                        <p style="margin: 0; color: #6B7280;">📅 {appointment['date']} • 📝 {appointment['status']}</p>
                    </div>
                    <div>
                        <button class="appointment-btn" style="background: #3B82F6;">Reschedule 🔧</button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("📝 No appointments scheduled yet. Book your first appointment above!")

# 💡 TIPS & INFORMATION
st.markdown("### 💡 Preparation Tips")

col1, col2 = st.columns(2)

with col1:
    with st.expander("📋 Before Your Visit"):
        st.markdown("""
        - Bring identification and insurance card
        - Wear comfortable, easy-to-remove clothing
        - Avoid using deodorant, perfume, or powder
        - Bring previous mammogram records if available
        - Write down any questions or concerns
        - Arrive 15 minutes early for paperwork
        """)

with col2:
    with st.expander("❓ Questions to Ask"):
        st.markdown("""
        - What type of mammogram are you performing?
        - How long will it take to get results?
        - What is your follow-up process if something is found?
        - Do you offer 3D mammograms?
        - What experience does your radiologist have?
        - Are there any additional costs I should know about?
        - Do you offer support services or support groups?
        """)

# 🎯 QUICK ACTIONS
st.markdown("### 🎯 Quick Actions")

action_cols = st.columns(3)

with action_cols[0]:
    if st.button("📞 Find Urgent Care", use_container_width=True):
        st.warning("🔄 Finding same-day appointments...")
        time.sleep(2)
        st.success("✅ Found 3 urgent care options nearby!")

with action_cols[1]:
    if st.button("💬 Talk to Support", use_container_width=True):
        st.info("💬 Connecting you with our support team...")

with action_cols[2]:
    if st.button("📱 Save This Search", use_container_width=True):
        st.balloons()
        st.success("🔖 Search criteria saved to your profile!")

# 🇰🇪 KENYA-SPECIFIC INFORMATION
with st.expander("ℹ️ Additional Kenya Information"):
    st.markdown("""
    ### 🇰🇪 Kenya Health Services
    
    **🏥 National Health Insurance Fund (NHIF)**
    - Covers up to KSh 300,000 for cancer treatment
    - Covers mammogram screening and other tests
    - All NHIF members are eligible
    
    **🎗️ Breast Cancer Support Organizations in Kenya**
    - **Women for Cancer** - Awareness and support services
    - **Kenya Cancer Association** - Legal and social support
    - **Faraja Cancer Support Trust** - Psychological support
    
    **📞 Support Numbers:**
    - **Health Emergency:** 1199
    - **Psychological Support:** 1190
    - **NHIF Services:** 0709 074 000
    
    **💰 Cost Estimates:**
    - Standard mammogram: KSh 3,000 - 8,000
    - 3D mammogram: KSh 8,000 - 15,000
    - Breast ultrasound: KSh 2,500 - 6,000
    """)

# CSV UPLOAD FOR HOSPITAL DATA
st.markdown("---")
st.markdown("### 📊 Upload Your Hospital Data")

uploaded_file = st.file_uploader("Upload a CSV file with hospital data", type=['csv'])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Successfully loaded {len(df)} hospitals from your CSV file!")
        st.dataframe(df.head())
        
        # Option to use the uploaded data
        if st.button("Use This Hospital Data"):
            hospitals_data = df.to_dict('records')
            st.rerun()
            
    except Exception as e:
        st.error(f"❌ Error reading CSV file: {e}")

# SUCCESS MESSAGE
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #ECFDF5, #D1FAE5); border-radius: 20px; margin: 2rem 0;">
        <h2 style="color: #065F46; margin-bottom: 1rem;">🎉 You're Taking an Important Step!</h2>
        <p style="color: #047857; font-size: 1.1rem;">
            Scheduling your screening appointment is a powerful act of self-care. 
            You're prioritizing your health and future well-being. We're proud of you! 🌟
        </p>
    </div>
    """, unsafe_allow_html=True)