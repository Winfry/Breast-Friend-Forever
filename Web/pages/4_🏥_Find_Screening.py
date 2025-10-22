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

st.set_page_config(page_title="Find Breast Screening", page_icon="🏥", layout="wide")

# 🎨 SCREENING ANIMATION CSS
st.markdown("""
    <style>
    @keyframes mapPulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.8; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    @keyframes locationGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(74, 222, 128, 0.5); }
        50% { box-shadow: 0 0 40px rgba(74, 222, 128, 0.8); }
    }
    
    @keyframes cardReveal {
        0% { transform: translateY(50px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }
    
    .clinic-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border-left: 5px solid #10B981;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.15);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: cardReveal 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .clinic-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transition: left 0.6s;
    }
    
    .clinic-card:hover::before {
        left: 100%;
    }
    
    .clinic-card:hover {
        transform: translateY(-8px);
        animation: locationGlow 2s infinite;
    }
    
    .urgent-card {
        border-left-color: #EF4444;
        background: linear-gradient(135deg, #FEF2F2, #FEE2E2);
    }
    
    .recommended-card {
        border-left-color: #F59E0B;
        background: linear-gradient(135deg, #FFFBEB, #FEF3C7);
    }
    
    .premium-card {
        border-left-color: #8B5CF6;
        background: linear-gradient(135deg, #FAF5FF, #EDE9FE);
    }
    
    .map-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        animation: mapPulse 3s infinite;
        border: 3px solid #10B981;
    }
    
    .filter-panel {
        background: linear-gradient(135deg, #ECFDF5, #D1FAE5);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border: 2px solid #10B981;
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
        position: relative;
        overflow: hidden;
    }
    
    .appointment-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transition: left 0.5s;
    }
    
    .appointment-btn:hover::before {
        left: 100%;
    }
    
    .appointment-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.4);
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
    
    .search-hero {
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
        padding: 3rem;
        border-radius: 25px;
        margin: 2rem 0;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .search-hero::before {
        content: '🏥💖🌟';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        font-size: 4rem;
        opacity: 0.1;
        display: flex;
        align-items: center;
        justify-content: center;
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
    </style>
    """, unsafe_allow_html=True)

# Load animations
try:
    location_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_0fhgwtli.json")
    calendar_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_kdxn8rqk.json")
    doctor_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_w51pcehl.json")
except:
    location_animation = calendar_animation = doctor_animation = None

# Initialize session state
if 'appointments' not in st.session_state:
    st.session_state.appointments = []
if 'clinics_data' not in st.session_state:
    st.session_state.clinics_data = []

st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem;">
        <h1 style="color: #10B981; font-size: 3rem; margin-bottom: 1rem;">
            🏥 Find Breast Screening in Kenya
        </h1>
        <p style="font-size: 1.3rem; color: #666;">
            Connect with trusted healthcare providers across Kenya 🌍
        </p>
    </div>
    """, unsafe_allow_html=True)

# Welcome animation
if location_animation:
    st_lottie(location_animation, speed=1, height=200, key="screening_welcome")

# 🎯 HERO SEARCH SECTION
st.markdown("""
    <div class="search-hero">
        <h2 style="color: white; margin-bottom: 1rem;">🔍 Find Breast Screening Services Near You</h2>
        <p style="color: white; font-size: 1.1rem; opacity: 0.9;">
            We connect you with compassionate, professional breast care services across Kenya
        </p>
    </div>
    """, unsafe_allow_html=True)

# 🏥 LOAD HOSPITAL DATA FROM CSV
@st.cache_data
def load_hospital_data():
    try:
        # Try different possible paths for the CSV file
        possible_paths = [
            "Backend/app/data/hospitals.csv"
            
        ]
        
        df = None
        used_path = ""
        
        for path in possible_paths:
            if os.path.exists(path):
                df = pd.read_csv(path)
                used_path = path
                st.success(f"✅ Loaded {len(df)} hospitals from {path}")
                break
        
        if df is None:
            st.error("❌ Could not find hospitals.csv file. Please ensure the file exists in one of these locations: Backend/data/hospitals.csv, data/hospitals.csv, or hospitals.csv")
            return None, None
        
        # Get unique counties for the filter
        counties = ["All Counties"] + sorted(df['county'].dropna().unique().tolist()) if 'county' in df.columns else ["All Counties"]
        
        return df, counties
        
    except Exception as e:
        st.error(f"❌ Error loading CSV: {e}")
        return None, None

# Load the data
hospital_df, available_counties = load_hospital_data()

# If no counties were loaded, use default ones
if not available_counties or available_counties == ["All Counties"]:
    available_counties = [
        "All Counties", "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Thika", "Machakos", 
        "Meru", "Nyeri", "Garissa", "Kakamega", "Kisii", "Kericho", "Kitale", "Malindi", "Lamu"
    ]

# 📍 SEARCH & FILTERS
col1, col2, col3 = st.columns(3)

with col1:
    location = st.selectbox("📍 Select Your County", available_counties)

with col2:
    search_radius = st.slider("🚗 Maximum Distance (km)", 5, 200, 50, help="How far are you willing to travel?")

with col3:
    facility_type = st.selectbox(
        "🏥 Facility Type",
        ["All Types", "National Hospital", "County Hospital", "Clinic", "Health Center", "MRI Center"]
    )

# Additional filters
st.markdown("### 🎛️ Refine Your Search")

filter_cols = st.columns(4)

with filter_cols[0]:
    insurance_type = st.selectbox(
        "💳 Accepted Insurance",
        ["All Insurance", "NHIF", "Madison", "Jubilee", "AAR", "Comprehensive Care", "Basic Care"]
    )

with filter_cols[1]:
    languages = st.multiselect(
        "🗣️ Languages Spoken",
        ["Swahili", "English", "Kikuyu", "Luhya", "Luo", "Kamba", "Kisii", "Somali"],
        default=["Swahili", "English"]
    )

with filter_cols[2]:
    appointment_type = st.selectbox(
        "📅 Appointment Type",
        ["All Types", "Same Day", "This Week", "Walk-in", "By Appointment Only"]
    )

with filter_cols[3]:
    rating_filter = st.slider("⭐ Minimum Rating", 3.0, 5.0, 4.0, 0.1)

def create_clinic_card(clinic):
    """Create a clinic card using Streamlit components"""
    
    # Status configuration
    status_config = {
        "open": ("status-open", "Open & Available", "clinic-card"),
        "urgent": ("status-urgent", "Urgent Care", "clinic-card urgent-card"),
        "premium": ("status-premium", "Premium Service", "clinic-card premium-card")
    }
    
    status_class, status_text, card_class = status_config.get(
        clinic.get("status", "open"), 
        status_config["open"]
    )
    
    # Create card using Streamlit components
    with st.container():
        st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
        
        # Header section
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <h3 style="color: #1F2937; margin: 0; display: flex; align-items: center;">
                        {clinic['name']}
                        <span class="status-badge {status_class}">{status_text}</span>
                        <span class="county-badge">{clinic['county']}</span>
                    </h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Rating and info
            rating_info = f"⭐ {clinic['rating']}/5 ({clinic['reviews']} reviews)" if clinic.get('reviews') else f"⭐ {clinic['rating']}/5"
            price_info = f"💰 {clinic['price_range']}" if clinic.get('price_range') else ""
            hours_info = f"🕒 {clinic['hours']}" if clinic.get('hours') else ""
            
            st.markdown(f"""
                <div style="color: #6B7280; margin-bottom: 1rem;">
                    <span>{rating_info}</span>
                    <span style="margin-left: 1rem;">📍 {clinic['distance']} km away</span>
                    {f'<span style="margin-left: 1rem;">{price_info}</span>' if price_info else ''}
                    {f'<span style="margin-left: 1rem;">{hours_info}</span>' if hours_info else ''}
                </div>
            """, unsafe_allow_html=True)
        
        # Specialty description
        specialty = clinic.get('specialty', 'Healthcare services')
        st.markdown(f"""
            <div style="background: #F8FAFC; padding: 1.5rem; border-radius: 15px; margin-bottom: 1.5rem;">
                <p style="color: #374151; margin: 0 0 1rem 0; font-style: italic;">"{specialty}"</p>
            """, unsafe_allow_html=True)
        
        # Contact and services in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            phone = clinic.get('phone', 'Contact not available')
            address = clinic.get('address', 'Address not available')
            emergency = clinic.get('emergency', '')
            
            st.markdown(f"""
                <strong>📞 Contact</strong>
                <p style="margin: 0.5rem 0; color: #6B7280;">{phone}</p>
                <p style="margin: 0; color: #6B7280; font-size: 0.9rem;">{address}</p>
                {f'<p style="margin: 0.5rem 0 0 0; color: #EF4444; font-size: 0.9rem;">🚨 Emergency: {emergency}</p>' if emergency else ''}
            """, unsafe_allow_html=True)
        
        with col2:
            wait_time = clinic.get('wait_time', 'Not specified')
            facility_type = clinic.get('type', 'Healthcare facility')
            
            st.markdown(f"""
                <strong>🕒 Availability</strong>
                <p style="margin: 0.5rem 0; color: #6B7280;">Wait time: {wait_time}</p>
                <p style="margin: 0; color: #6B7280; font-size: 0.9rem;">Type: {facility_type}</p>
            """, unsafe_allow_html=True)
        
        with col3:
            insurance_list = clinic.get('insurance', [])
            if isinstance(insurance_list, str):
                insurance_list = [insurance_list]
            insurance_display = ', '.join(insurance_list[:3])
            if len(insurance_list) > 3:
                insurance_display += f" +{len(insurance_list)-3} more"
            
            st.markdown(f"""
                <strong>💼 Insurance</strong>
                <p style="margin: 0.5rem 0; color: #6B7280;">{insurance_display if insurance_display else 'Not specified'}</p>
            """, unsafe_allow_html=True)
        
        # Special services
        services_list = clinic.get('special_services', [])
        if isinstance(services_list, str):
            services_list = [services_list]
        
        if services_list:
            st.markdown(f"""
                <div style="margin-top: 1rem;">
                    <strong>🔬 Special Services:</strong>
                    <p style="margin: 0.5rem 0; color: #6B7280;">{', '.join(services_list)}</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Footer with languages and appointment button
        col1, col2 = st.columns([2, 1])
        with col1:
            languages_list = clinic.get('languages', [])
            if isinstance(languages_list, str):
                languages_list = [languages_list]
            
            if languages_list:
                st.markdown(f"""
                    <strong>🗣️ Languages: </strong>
                    <span style="color: #6B7280;">{', '.join(languages_list)}</span>
                """, unsafe_allow_html=True)
        
        with col2:
            if st.button(f"Book Appointment 📅", key=f"appt_btn_{clinic['id']}", use_container_width=True):
                st.session_state[f"show_date_{clinic['id']}"] = True
            
        # Date selection (only shown when button is clicked)
        if st.session_state.get(f"show_date_{clinic['id']}", False):
            date_col1, date_col2, date_col3 = st.columns([1, 1, 2])
            with date_col1:
                if st.button(f"📞 Call Now", key=f"call_{clinic['id']}", use_container_width=True):
                    st.info(f"📞 Calling {clinic['name']} at {clinic.get('phone', 'number not available')}")
            
            with date_col2:
                if st.button(f"📍 Get Directions", key=f"dir_{clinic['id']}", use_container_width=True):
                    st.info(f"🗺️ Getting directions to {clinic.get('address', 'this facility')}")
            
            with date_col3:
                date = st.date_input("Select appointment date", key=f"date_{clinic['id']}")
                if st.button(f"✅ Confirm Appointment", key=f"confirm_{clinic['id']}", use_container_width=True):
                    st.session_state.appointments.append({
                        "clinic": clinic['name'],
                        "date": date,
                        "status": "Scheduled"
                    })
                    st.success(f"🎉 Appointment booked at {clinic['name']} for {date}!")
                    st.session_state[f"show_date_{clinic['id']}"] = False
        
        st.markdown('</div>', unsafe_allow_html=True)

# Process hospital data
if hospital_df is not None:
    # Convert DataFrame to the expected format
    clinics_data = []
    for idx, row in hospital_df.iterrows():
        clinic = {
            "id": idx + 1,
            "name": row.get('name', 'Hospital'),
            "type": row.get('type', 'National Hospital'),
            "county": row.get('county', 'Nairobi'),
            "distance": float(row.get('distance', 5.0)),
            "rating": float(row.get('rating', 4.0)),
            "reviews": int(row.get('reviews', 100)) if pd.notna(row.get('reviews')) else 100,
            "address": row.get('address', 'Address not available'),
            "phone": row.get('phone', '+254 XXX XXX XXX'),
            "emergency": row.get('emergency', '') if pd.notna(row.get('emergency', '')) else '',
            "insurance": row.get('insurance', 'NHIF').split(',') if pd.notna(row.get('insurance')) and isinstance(row.get('insurance'), str) else ['NHIF'],
            "languages": row.get('languages', 'Swahili,English').split(',') if pd.notna(row.get('languages')) and isinstance(row.get('languages'), str) else ['Swahili', 'English'],
            "wait_time": row.get('wait_time', '1-2 Days'),
            "services": row.get('services', 'Mammography').split(',') if pd.notna(row.get('services')) and isinstance(row.get('services'), str) else ['Mammography'],
            "special_services": row.get('special_services', 'Screening').split(',') if pd.notna(row.get('special_services')) and isinstance(row.get('special_services'), str) else ['Screening'],
            "status": row.get('status', 'open'),
            "price_range": row.get('price_range', '$$'),
            "specialty": row.get('specialty', 'Healthcare services'),
            "hours": row.get('hours', 'Mon-Fri: 8AM-5PM'),
            "lat": float(row.get('lat', -1.286389)) if pd.notna(row.get('lat')) else -1.286389,
            "lon": float(row.get('lon', 36.817223)) if pd.notna(row.get('lon')) else 36.817223
        }
        clinics_data.append(clinic)
    
    st.session_state.clinics_data = clinics_data
else:
    # Use sample data if CSV not available
    st.warning("Using sample data - CSV file not found")
    clinics_data = [
        {
            "id": 1, "name": "Nairobi Women's Hospital", "type": "National Hospital", "county": "Nairobi",
            "distance": 2.3, "rating": 4.8, "reviews": 234, "address": "James Gichuru Road, Lavington, Nairobi",
            "phone": "+254 20 272 6000", "emergency": "+254 733 639 000", 
            "insurance": ["NHIF", "Madison", "Jubilee", "AAR", "Private Pay"],
            "languages": ["Swahili", "English", "Kikuyu"], "wait_time": "1-2 Days",
            "services": ["Mammography", "Ultrasound", "Biopsy", "Breast Surgery", "Oncology"],
            "special_services": ["Digital Mammogram", "Breast Cancer Screening", "Support Groups"],
            "status": "open", "price_range": "$$", "hours": "24/7",
            "specialty": "Comprehensive women's healthcare with specialized breast care services",
            "lat": -1.2684, "lon": 36.7965
        }
    ]
    st.session_state.clinics_data = clinics_data

# 🗺️ INTERACTIVE MAP VISUALIZATION
st.markdown("### 🗺️ Screening Centers Across Kenya")

if st.session_state.clinics_data:
    # Create map data from clinics
    map_data = pd.DataFrame({
        'lat': [clinic['lat'] for clinic in st.session_state.clinics_data],
        'lon': [clinic['lon'] for clinic in st.session_state.clinics_data],
        'name': [clinic['name'] for clinic in st.session_state.clinics_data],
        'county': [clinic['county'] for clinic in st.session_state.clinics_data],
        'size': [20 + (clinic['rating'] - 4) * 10 for clinic in st.session_state.clinics_data],
        'color': ['#10B981' if clinic.get('status') == 'open' else 
                  '#EF4444' if clinic.get('status') == 'urgent' else 
                  '#8B5CF6' for clinic in st.session_state.clinics_data]
    })

    fig = px.scatter_mapbox(
        map_data,
        lat="lat",
        lon="lon",
        hover_name="name",
        hover_data={"county": True, "lat": False, "lon": False, "size": False, "color": False},
        size="size",
        color="color",
        color_discrete_map="identity",
        zoom=6,
        height=500
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":0,"l":0,"b":0},
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No hospital data available to display on the map")

# 🏥 CLINIC LISTINGS
st.markdown("### 🏥 Available Healthcare Facilities")

# Filter clinics based on user selection
filtered_clinics = st.session_state.clinics_data.copy()

if location != "All Counties":
    filtered_clinics = [clinic for clinic in filtered_clinics if clinic["county"] == location]

if facility_type != "All Types":
    type_map = {
        "National Hospital": "National Hospital",
        "County Hospital": "County Hospital", 
        "Clinic": "Clinic",
        "Health Center": "Health Center",
        "MRI Center": "MRI Center"
    }
    filtered_clinics = [clinic for clinic in filtered_clinics if clinic["type"] == type_map.get(facility_type, facility_type)]

filtered_clinics = [clinic for clinic in filtered_clinics 
                   if clinic["distance"] <= search_radius and clinic["rating"] >= rating_filter]

# Display filtered clinics
if filtered_clinics:
    st.success(f"Found {len(filtered_clinics)} facilities matching your criteria")
    for clinic in filtered_clinics:
        create_clinic_card(clinic)
else:
    st.info("No facilities found matching your current filters. Try adjusting your search criteria.")

# 📅 APPOINTMENT MANAGER
st.markdown("### 📅 Your Appointments")

if st.session_state.appointments:
    for i, appointment in enumerate(st.session_state.appointments):
        st.markdown(f"""
            <div class="clinic-card" style="border-left-color: #3B82F6;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0 0 0.5rem 0; color: #1F2937;">{appointment['clinic']}</h4>
                        <p style="margin: 0; color: #6B7280;">📅 {appointment['date']} • 📝 {appointment['status']}</p>
                    </div>
                    <div>
                        <button class="appointment-btn" style="background: #3B82F6;">Modify 🔧</button>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("📝 No appointments scheduled yet. Book your first appointment above!")

# 💡 TIPS & PREPARATION
st.markdown("### 💡 Preparation Tips")

tips_cols = st.columns(2)

with tips_cols[0]:
    with st.expander("📋 Before Your Visit"):
        st.markdown("""
        - **Bring identification and insurance card**
        - **Wear comfortable, easy-to-remove clothing**
        - **Avoid using deodorant, perfume, or powder**
        - **Bring your previous mammogram records if available**
        - **Write down any questions or concerns**
        - **Arrive 15 minutes early for paperwork**
        - **Bring a companion if you need support**
        """)

with tips_cols[1]:
    with st.expander("❓ Questions to Ask"):
        st.markdown("""
        - **What type of mammogram are you performing?**
        - **How long will it take to get results?**
        - **What is your follow-up process if something is found?**
        - **Do you offer 3D mammograms?**
        - **What experience does your radiologist have?**
        - **Are there any additional costs I should know about?**
        - **Do you have support services or support groups?**
        """)

# 🎯 QUICK ACTIONS
st.markdown("### 🎯 Quick Actions")

action_cols = st.columns(3)

with action_cols[0]:
    if st.button("📞 Find Urgent Care", use_container_width=True):
        urgent_clinics = [c for c in st.session_state.clinics_data if c.get('status') == 'urgent']
        if urgent_clinics:
            st.success(f"✅ Found {len(urgent_clinics)} urgent care options!")
        else:
            st.info("No urgent care facilities found in the current data")

with action_cols[1]:
    if st.button("💬 Talk to Support", use_container_width=True):
        st.info("💬 Connecting you with our support team...")
        time.sleep(1)
        st.success("🤝 Support team is ready to assist you!")

with action_cols[2]:
    if st.button("📱 Save This Search", use_container_width=True):
        st.balloons()
        st.success("🔖 Search criteria saved to your profile!")

# 🎊 SUCCESS MESSAGE
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #ECFDF5, #D1FAE5); border-radius: 25px; margin: 2rem 0;">
        <h2 style="color: #065F46; margin-bottom: 1rem;">🎉 You're Taking an Important Step!</h2>
        <p style="color: #047857; font-size: 1.1rem; line-height: 1.6;">
            Booking your screening appointment is a powerful act of self-care. 
            You're taking charge of your health and future well-being. We're proud of you! 🌟
        </p>
        <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 2rem;">
            <span style="animation: mapPulse 2s infinite;">💝</span>
            <span style="animation: mapPulse 2s infinite; animation-delay: 0.3s;">🎯</span>
            <span style="animation: mapPulse 2s infinite; animation-delay: 0.6s;">🌈</span>
            <span style="animation: mapPulse 2s infinite; animation-delay: 0.9s;">🌟</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 🇰🇪 KENYA-SPECIFIC INFORMATION
with st.expander("ℹ️ Additional Kenya Information"):
    st.markdown("""
    ### 🇰🇪 Healthcare Services in Kenya
    
    **🏥 National Hospital Insurance Fund (NHIF)**
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
    
    **📍 Coverage:** This platform includes healthcare facilities from all 47 counties in Kenya
    """)