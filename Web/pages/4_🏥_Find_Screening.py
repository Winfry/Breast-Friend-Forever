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

st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem;">
        <h1 style="color: #10B981; font-size: 3rem; margin-bottom: 1rem;">
            🏥 Pata Uchunguzi wa Matiti Kenya
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
        <h2 style="color: white; margin-bottom: 1rem;">🔍 Tafuta Huduma ya Matiti Karibu Nawe</h2>
        <p style="color: white; font-size: 1.1rem; opacity: 0.9;">
            We connect you with compassionate, professional breast care services across Kenya
        </p>
    </div>
    """, unsafe_allow_html=True)

# 📍 SEARCH & FILTERS
col1, col2, col3 = st.columns(3)

with col1:
    counties = [
        "All Counties", "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Thika", "Machakos", 
        "Meru", "Nyeri", "Garissa", "Kakamega", "Kisii", "Kericho", "Kitale", "Malindi", "Lamu"
    ]
    location = st.selectbox("📍 Chagua County Yako", counties)

with col2:
    search_radius = st.slider("🚗 Umbali wa Juu (km)", 5, 200, 50, help="How far are you willing to travel?")

with col3:
    facility_type = st.selectbox(
        "🏥 Aina ya Kituo",
        ["Aina Zote", "Hospitali Kuu", "Hospitali ya Wilaya", "Kliniki", "Kituo cha Afya", "Kitengo cha MRI"]
    )

# Additional filters
st.markdown("### 🎛️ Refine Your Search")

filter_cols = st.columns(4)

with filter_cols[0]:
    insurance_type = st.selectbox(
        "💳 Bima Inayokubaliwa",
        ["Bima Zote", "NHIF", "Madison", "Jubilee", "AAR", "Huduma Bora", "Huduma ya Kawaida"]
    )

with filter_cols[1]:
    languages = st.multiselect(
        "🗣️ Lugha Unazozungumza",
        ["Kiswahili", "English", "Kikuyu", "Luhya", "Luo", "Kamba", "Kisii", "Somali"],
        default=["Kiswahili", "English"]
    )

with filter_cols[2]:
    appointment_type = st.selectbox(
        "📅 Aina ya Miadi",
        ["Aina Zote", "Leo Leo", "Wiki Hii", "Walk-in", "Kwa Miadi Tu"]
    )

with filter_cols[3]:
    rating_filter = st.slider("⭐ Ukadiriaji wa Chini", 3.0, 5.0, 4.0, 0.1)

# 🏥 LOAD HOSPITAL DATA FROM CSV
@st.cache_data
def load_hospital_data():
    try:
        # Try to load from CSV file
        csv_path = "Backend/data/hospitals.csv"
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            st.success(f"✅ Loaded {len(df)} hospitals from CSV")
            return df
        else:
            st.warning("⚠️ CSV file not found. Using sample data.")
            return None
    except Exception as e:
        st.error(f"❌ Error loading CSV: {e}")
        return None

def create_clinic_card(clinic):
    """Create a clinic card using Streamlit components instead of raw HTML"""
    
    # Status configuration
    status_config = {
        "open": ("status-open", "Fungua & Inapatikana", "clinic-card"),
        "urgent": ("status-urgent", "Huduma ya Haraka", "clinic-card urgent-card"),
        "premium": ("status-premium", "Huduma Bora", "clinic-card premium-card")
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
            st.markdown(f"""
                <div style="color: #6B7280; margin-bottom: 1rem;">
                    <span>⭐ {clinic['rating']}/5 ({clinic['reviews']} reviews)</span>
                    <span style="margin-left: 1rem;">📍 {clinic['distance']} km away</span>
                    <span style="margin-left: 1rem;">💰 {clinic['price_range']}</span>
                    <span style="margin-left: 1rem;">🕒 {clinic['hours']}</span>
                </div>
            """, unsafe_allow_html=True)
        
        # Specialty description
        st.markdown(f"""
            <div style="background: #F8FAFC; padding: 1.5rem; border-radius: 15px; margin-bottom: 1.5rem;">
                <p style="color: #374151; margin: 0 0 1rem 0; font-style: italic;">"{clinic['specialty']}"</p>
            """, unsafe_allow_html=True)
        
        # Contact and services in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <strong>📞 Mawasiliano</strong>
                <p style="margin: 0.5rem 0; color: #6B7280;">{clinic['phone']}</p>
                <p style="margin: 0; color: #6B7280; font-size: 0.9rem;">{clinic['address']}</p>
                <p style="margin: 0.5rem 0 0 0; color: #EF4444; font-size: 0.9rem;">
                    🚨 Dharura: {clinic['emergency']}
                </p>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <strong>🕒 Upatikanaji</strong>
                <p style="margin: 0.5rem 0; color: #6B7280;">Muda wa kusubiri: {clinic['wait_time']}</p>
                <p style="margin: 0; color: #6B7280; font-size: 0.9rem;">Aina: {clinic['type']}</p>
            """, unsafe_allow_html=True)
        
        with col3:
            insurance_list = clinic['insurance'] if isinstance(clinic['insurance'], list) else [clinic['insurance']]
            insurance_display = ', '.join(insurance_list[:3])
            if len(insurance_list) > 3:
                insurance_display += f" +{len(insurance_list)-3} zaidi"
            
            st.markdown(f"""
                <strong>💼 Bima</strong>
                <p style="margin: 0.5rem 0; color: #6B7280;">{insurance_display}</p>
            """, unsafe_allow_html=True)
        
        # Special services
        services_list = clinic['special_services'] if isinstance(clinic['special_services'], list) else [clinic['special_services']]
        st.markdown(f"""
            <div style="margin-top: 1rem;">
                <strong>🔬 Huduma Maalum:</strong>
                <p style="margin: 0.5rem 0; color: #6B7280;">{', '.join(services_list)}</p>
            </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Footer with languages and appointment button
        col1, col2 = st.columns([2, 1])
        with col1:
            languages_list = clinic['languages'] if isinstance(clinic['languages'], list) else [clinic['languages']]
            st.markdown(f"""
                <strong>🗣️ Lugha: </strong>
                <span style="color: #6B7280;">{', '.join(languages_list)}</span>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button(f"Weka Miadi 📅", key=f"appt_btn_{clinic['id']}", use_container_width=True):
                st.session_state[f"show_date_{clinic['id']}"] = True
            
        # Date selection (only shown when button is clicked)
        if st.session_state.get(f"show_date_{clinic['id']}", False):
            date_col1, date_col2, date_col3 = st.columns([1, 1, 2])
            with date_col1:
                if st.button(f"📞 Piga Sasa", key=f"call_{clinic['id']}", use_container_width=True):
                    st.info(f"📞 Inapigia {clinic['name']} kwa {clinic['phone']}")
            
            with date_col2:
                if st.button(f"📍 Pata Maelekezo", key=f"dir_{clinic['id']}", use_container_width=True):
                    st.info(f"🗺️ Inakupa maelekezo ya kwenda {clinic['address']}")
            
            with date_col3:
                date = st.date_input("Chagua tarehe ya miadi", key=f"date_{clinic['id']}")
                if st.button(f"✅ Thibitisha Miadi", key=f"confirm_{clinic['id']}", use_container_width=True):
                    st.session_state.appointments.append({
                        "clinic": clinic['name'],
                        "date": date,
                        "status": "Imepangwa"
                    })
                    st.success(f"🎉 Miadi imepangwa {clinic['name']} kwa {date}!")
                    st.session_state[f"show_date_{clinic['id']}"] = False
        
        st.markdown('</div>', unsafe_allow_html=True)

# Load hospital data
hospital_df = load_hospital_data()

if hospital_df is not None:
    # Convert DataFrame to the expected format
    clinics_data = []
    for idx, row in hospital_df.iterrows():
        clinic = {
            "id": idx + 1,
            "name": row.get('name', 'Hospital'),
            "type": row.get('type', 'Hospitali Kuu'),
            "county": row.get('county', 'Nairobi'),
            "distance": float(row.get('distance', 5.0)),
            "rating": float(row.get('rating', 4.0)),
            "reviews": int(row.get('reviews', 100)),
            "address": row.get('address', 'Address not available'),
            "phone": row.get('phone', '+254 XXX XXX XXX'),
            "emergency": row.get('emergency', '+254 XXX XXX XXX'),
            "insurance": row.get('insurance', 'NHIF').split(',') if isinstance(row.get('insurance'), str) else ['NHIF'],
            "languages": row.get('languages', 'Kiswahili,English').split(',') if isinstance(row.get('languages'), str) else ['Kiswahili', 'English'],
            "wait_time": row.get('wait_time', 'Siku 1-2'),
            "services": row.get('services', 'Mammography').split(',') if isinstance(row.get('services'), str) else ['Mammography'],
            "special_services": row.get('special_services', 'Screening').split(',') if isinstance(row.get('special_services'), str) else ['Screening'],
            "status": row.get('status', 'open'),
            "price_range": row.get('price_range', '$$'),
            "specialty": row.get('specialty', 'Healthcare services'),
            "hours": row.get('hours', 'Mon-Fri: 8AM-5PM'),
            "lat": float(row.get('lat', -1.286389)),
            "lon": float(row.get('lon', 36.817223))
        }
        clinics_data.append(clinic)
else:
    # Use sample data if CSV not available
    clinics_data = [
        {
            "id": 1, "name": "Nairobi Women's Hospital", "type": "Hospitali Kuu", "county": "Nairobi",
            "distance": 2.3, "rating": 4.8, "reviews": 234, "address": "James Gichuru Road, Lavington, Nairobi",
            "phone": "+254 20 272 6000", "emergency": "+254 733 639 000", 
            "insurance": ["NHIF", "Madison", "Jubilee", "AAR", "Private Pay"],
            "languages": ["Kiswahili", "English", "Kikuyu"], "wait_time": "Siku 1-2",
            "services": ["Mammography", "Ultrasound", "Biopsy", "Breast Surgery", "Oncology"],
            "special_services": ["Digital Mammogram", "Breast Cancer Screening", "Support Groups"],
            "status": "open", "price_range": "$$", "hours": "24/7",
            "specialty": "Comprehensive women's healthcare with specialized breast care services",
            "lat": -1.2684, "lon": 36.7965
        },
        # ... (include other sample clinics as needed)
    ]

# 🗺️ INTERACTIVE MAP VISUALIZATION
st.markdown("### 🗺️ Vituo vya Uchunguzi Karibu Nawe")

# Create map data from clinics
map_data = pd.DataFrame({
    'lat': [clinic['lat'] for clinic in clinics_data],
    'lon': [clinic['lon'] for clinic in clinics_data],
    'name': [clinic['name'] for clinic in clinics_data],
    'size': [20 + (clinic['rating'] - 4) * 10 for clinic in clinics_data],
    'color': ['#10B981' if clinic['status'] == 'open' else 
              '#EF4444' if clinic['status'] == 'urgent' else 
              '#8B5CF6' for clinic in clinics_data]
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

# 🏥 CLINIC LISTINGS
st.markdown("### 🏥 Vituo Vinavyopatikana")

# Filter clinics based on user selection
filtered_clinics = clinics_data.copy()

if location != "All Counties":
    filtered_clinics = [clinic for clinic in filtered_clinics if clinic["county"] == location]

if facility_type != "Aina Zote":
    type_map = {
        "Hospitali Kuu": "Hospitali Kuu",
        "Hospitali ya Wilaya": "Hospitali ya Wilaya", 
        "Kliniki": "Kliniki",
        "Kituo cha Afya": "Kituo cha Afya",
        "Kitengo cha MRI": "Kitengo cha MRI"
    }
    filtered_clinics = [clinic for clinic in filtered_clinics if clinic["type"] == type_map[facility_type]]

filtered_clinics = [clinic for clinic in filtered_clinics 
                   if clinic["distance"] <= search_radius and clinic["rating"] >= rating_filter]

# Display filtered clinics
for clinic in filtered_clinics:
    create_clinic_card(clinic)

# 📅 APPOINTMENT MANAGER
st.markdown("### 📅 Miadi Yako")

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
                        <button class="appointment-btn" style="background: #3B82F6;">Rekebisha 🔧</button>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("📝 Hakuna miadi iliyopangwa bado. Weka miadi yako ya kwanza hapo juu!")

# The rest of your code remains the same for tips, quick actions, etc.
# ... (keep the tips, quick actions, and Kenya-specific information sections)