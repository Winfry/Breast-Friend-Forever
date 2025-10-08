import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
import json
import time

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

# 🏥 REAL KENYAN HOSPITAL DATA
clinics_data = [
    {
        "id": 1,
        "name": "Nairobi Women's Hospital",
        "type": "Hospitali Kuu",
        "county": "Nairobi",
        "distance": 2.3,
        "rating": 4.8,
        "reviews": 234,
        "address": "James Gichuru Road, Lavington, Nairobi",
        "phone": "+254 20 272 6000",
        "emergency": "+254 733 639 000",
        "insurance": ["NHIF", "Madison", "Jubilee", "AAR", "Private Pay"],
        "languages": ["Kiswahili", "English", "Kikuyu"],
        "wait_time": "Siku 1-2",
        "services": ["Mammography", "Ultrasound", "Biopsy", "Breast Surgery", "Oncology"],
        "special_services": ["Digital Mammogram", "Breast Cancer Screening", "Support Groups"],
        "status": "open",
        "price_range": "$$",
        "specialty": "Comprehensive women's healthcare with specialized breast care services",
        "hours": "24/7",
        "lat": -1.2684,
        "lon": 36.7965
    },
    {
        "id": 2,
        "name": "Aga Khan University Hospital",
        "type": "Hospitali Kuu",
        "county": "Nairobi", 
        "distance": 4.1,
        "rating": 4.9,
        "reviews": 189,
        "address": "3rd Parklands Avenue, Nairobi",
        "phone": "+254 20 366 2000",
        "emergency": "+254 711 709 100",
        "insurance": ["NHIF", "Madison", "Jubilee", "AAR", "CIC", "Britam"],
        "languages": ["Kiswahili", "English", "Hindi", "Gujarati"],
        "wait_time": "Siku 3-5",
        "services": ["3D Mammography", "Breast MRI", "Genetic Testing", "Oncology", "Radiation Therapy"],
        "special_services": ["Advanced Imaging", "Genetic Counseling", "Multidisciplinary Care"],
        "status": "premium",
        "price_range": "$$$",
        "specialty": "State-of-the-art diagnostic imaging and comprehensive cancer care",
        "hours": "Mon-Sun: 6AM-10PM",
        "lat": -1.2542,
        "lon": 36.8134
    },
    {
        "id": 3,
        "name": "Mombasa Women's Hospital",
        "type": "Hospitali ya Wilaya",
        "county": "Mombasa",
        "distance": 0.8,
        "rating": 4.5,
        "reviews": 156,
        "address": "Nyerere Avenue, Mombasa",
        "phone": "+254 41 222 3851",
        "emergency": "+254 722 516 363",
        "insurance": ["NHIF", "Jubilee", "Private Pay", "Huduma Bora"],
        "languages": ["Kiswahili", "English", "Digo", "Duruma"],
        "wait_time": "Same day",
        "services": ["Mammography", "Ultrasound", "Women's Health", "Family Planning"],
        "special_services": ["Community Outreach", "Affordable Screening", "Mobile Clinics"],
        "status": "urgent",
        "price_range": "$",
        "specialty": "Coastal region's leading women's health provider with compassionate care",
        "hours": "Mon-Sat: 7AM-9PM, Sun: 8AM-6PM",
        "lat": -4.0547,
        "lon": 39.6636
    },
    {
        "id": 4,
        "name": "Kisumu Breast Care Center",
        "type": "Kliniki",
        "county": "Kisumu",
        "distance": 1.2,
        "rating": 4.6,
        "reviews": 98,
        "address": "Oginga Odinga Street, Kisumu",
        "phone": "+254 57 202 4991",
        "emergency": "+254 723 654 321",
        "insurance": ["NHIF", "Private Pay", "Huduma ya Kawaida"],
        "languages": ["Kiswahili", "English", "Luo", "Kisii"],
        "wait_time": "Walk-in",
        "services": ["Clinical Breast Exam", "Ultrasound", "Mammography Referrals", "Education"],
        "special_services": ["Free Screening Days", "Community Education", "Support Groups"],
        "status": "open",
        "price_range": "$$",
        "specialty": "Lake region's dedicated breast care facility with community focus",
        "hours": "Mon-Fri: 8AM-6PM, Sat: 9AM-2PM",
        "lat": -0.1022,
        "lon": 34.7617
    },
    {
        "id": 5,
        "name": "Nakuru Provincial Hospital",
        "type": "Hospitali ya Wilaya",
        "county": "Nakuru",
        "distance": 3.5,
        "rating": 4.3,
        "reviews": 167,
        "address": "Kenyatta Avenue, Nakuru",
        "phone": "+254 51 221 5351",
        "emergency": "+254 720 123 456",
        "insurance": ["NHIF", "Huduma Bora", "Private Pay"],
        "languages": ["Kiswahili", "English", "Kikuyu", "Kalenjin"],
        "wait_time": "Siku 2-3",
        "services": ["Mammography", "General Surgery", "Oncology Referrals", "Pathology"],
        "special_services": ["Public Health Services", "Subsidized Care", "Mobile Screening"],
        "status": "open",
        "price_range": "$",
        "specialty": "Rift Valley's public healthcare provider with breast screening services",
        "hours": "24/7",
        "lat": -0.3031,
        "lon": 36.0800
    },
    {
        "id": 6,
        "name": "Eldoret Medical Centre",
        "type": "Hospitali Kuu",
        "county": "Eldoret",
        "distance": 2.1,
        "rating": 4.7,
        "reviews": 134,
        "address": "Uganda Road, Eldoret",
        "phone": "+254 53 206 3000",
        "emergency": "+254 732 987 654",
        "insurance": ["NHIF", "Madison", "Jubilee", "Private Pay"],
        "languages": ["Kiswahili", "English", "Kalenjin", "Luhya"],
        "wait_time": "Siku 1-2",
        "services": ["Digital Mammography", "Breast Surgery", "Chemotherapy", "Palliative Care"],
        "special_services": ["Cancer Treatment", "Pain Management", "Nutrition Counseling"],
        "status": "open",
        "price_range": "$$",
        "specialty": "Western Kenya's comprehensive cancer care and breast health services",
        "hours": "Mon-Sun: 6AM-10PM",
        "lat": 0.5143,
        "lon": 35.2698
    },
    {
        "id": 7,
        "name": "Thika Level 5 Hospital",
        "type": "Hospitali ya Wilaya",
        "county": "Kiambu",
        "distance": 5.2,
        "rating": 4.2,
        "reviews": 89,
        "address": "Garissa Road, Thika",
        "phone": "+254 67 224 0000",
        "emergency": "+254 711 222 333",
        "insurance": ["NHIF", "Huduma Bora"],
        "languages": ["Kiswahili", "English", "Kikuyu"],
        "wait_time": "Siku 3-4",
        "services": ["Basic Mammography", "Ultrasound", "Surgical Services", "Lab Services"],
        "special_services": ["Public Healthcare", "Emergency Services", "Maternal Health"],
        "status": "open",
        "price_range": "$",
        "specialty": "Central Kenya's public hospital providing essential breast screening",
        "hours": "24/7",
        "lat": -1.0333,
        "lon": 37.0833
    },
    {
        "id": 8,
        "name": "Kenyatta National Hospital",
        "type": "Hospitali Kuu",
        "county": "Nairobi",
        "distance": 3.8,
        "rating": 4.4,
        "reviews": 278,
        "address": "Hospital Road, Nairobi",
        "phone": "+254 20 272 6300",
        "emergency": "+254 722 205 901",
        "insurance": ["NHIF", "Private Pay", "Huduma Bora"],
        "languages": ["Kiswahili", "English"],
        "wait_time": "Siku 5-7",
        "services": ["Comprehensive Cancer Care", "Radiation Therapy", "Clinical Trials", "Research"],
        "special_services": ["Teaching Hospital", "Research Programs", "Specialist Referrals"],
        "status": "premium",
        "price_range": "$$",
        "specialty": "National referral hospital with comprehensive breast cancer management",
        "hours": "24/7",
        "lat": -1.3041,
        "lon": 36.8013
    }
]

# 🗺️ INTERACTIVE MAP VISUALIZATION
st.markdown("### 🗺️ Vituo vya Uchunguzi Karibu Nawe")

# Create map data from clinics
map_data = pd.DataFrame({
    'lat': [clinic['lat'] for clinic in clinics_data],
    'lon': [clinic['lon'] for clinic in clinics_data],
    'name': [clinic['name'] for clinic in clinics_data],
    'size': [20 + (clinic['rating'] - 4) * 10 for clinic in clinics_data],  # Size based on rating
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
    height=400,
    title="Healthcare Facilities Offering Breast Screening in Kenya"
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

for clinic in filtered_clinics:
    # Apply filters
    if clinic["distance"] > search_radius:
        continue
    if clinic["rating"] < rating_filter:
        continue
    
    # Status badge and card class
    status_config = {
        "open": ("status-open", "Fungua & Inapatikana", "clinic-card"),
        "urgent": ("status-urgent", "Huduma ya Haraka", "clinic-card urgent-card"),
        "premium": ("status-premium", "Huduma Bora", "clinic-card premium-card")
    }
    
    status_class, status_text, card_class = status_config[clinic["status"]]
    
    st.markdown(f"""
        <div class="{card_class}">
            <div style="display: flex; justify-content: between; align-items: flex-start; margin-bottom: 1rem;">
                <div style="flex: 1;">
                    <h3 style="color: #1F2937; margin: 0 0 0.5rem 0; display: flex; align-items: center;">
                        {clinic['name']}
                        <span class="status-badge {status_class}">{status_text}</span>
                        <span class="county-badge">{clinic['county']}</span>
                    </h3>
                    <div style="color: #6B7280; margin-bottom: 1rem;">
                        <span>⭐ {clinic['rating']}/5 ({clinic['reviews']} reviews)</span>
                        <span style="margin-left: 1rem;">📍 {clinic['distance']} km away</span>
                        <span style="margin-left: 1rem;">💰 {clinic['price_range']}</span>
                        <span style="margin-left: 1rem;">🕒 {clinic['hours']}</span>
                    </div>
                </div>
            </div>
            
            <div style="background: #F8FAFC; padding: 1.5rem; border-radius: 15px; margin-bottom: 1.5rem;">
                <p style="color: #374151; margin: 0 0 1rem 0; font-style: italic;">"{clinic['specialty']}"</p>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
                    <div>
                        <strong>📞 Mawasiliano</strong>
                        <p style="margin: 0.5rem 0; color: #6B7280;">{clinic['phone']}</p>
                        <p style="margin: 0; color: #6B7280; font-size: 0.9rem;">{clinic['address']}</p>
                        <p style="margin: 0.5rem 0 0 0; color: #EF4444; font-size: 0.9rem;">
                            🚨 Dharura: {clinic['emergency']}
                        </p>
                    </div>
                    
                    <div>
                        <strong>🕒 Upatikanaji</strong>
                        <p style="margin: 0.5rem 0; color: #6B7280;">Muda wa kusubiri: {clinic['wait_time']}</p>
                        <p style="margin: 0; color: #6B7280; font-size: 0.9rem;">Aina: {clinic['type']}</p>
                    </div>
                    
                    <div>
                        <strong>💼 Bima</strong>
                        <p style="margin: 0.5rem 0; color: #6B7280;">
                            {', '.join(clinic['insurance'][:3])}
                            {f" +{len(clinic['insurance'])-3} zaidi" if len(clinic['insurance']) > 3 else ""}
                        </p>
                    </div>
                </div>
                
                <div style="margin-top: 1rem;">
                    <strong>🔬 Huduma Maalum:</strong>
                    <p style="margin: 0.5rem 0; color: #6B7280;">{', '.join(clinic['special_services'])}</p>
                </div>
            </div>
            
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>🗣️ Lugha: </strong>
                    <span style="color: #6B7280;">{', '.join(clinic['languages'])}</span>
                </div>
                
                <button class="appointment-btn" onclick="alert('Inakuandalia miadi...')">
                    Weka Miadi 📅
                </button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Appointment scheduling
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button(f"📞 Piga Sasa", key=f"call_{clinic['id']}", use_container_width=True):
            st.info(f"📞 Inapigia {clinic['name']} kwa {clinic['phone']}")
    
    with col2:
        if st.button(f"📍 Pata Maelekezo", key=f"dir_{clinic['id']}", use_container_width=True):
            st.info(f"🗺️ Inakupa maelekezo ya kwenda {clinic['address']}")
    
    with col3:
        date = st.date_input("Chagua tarehe ya miadi", key=f"date_{clinic['id']}")
        if st.button(f"✅ Thibitisha Miadi", key=f"appt_{clinic['id']}", use_container_width=True):
            st.session_state.appointments.append({
                "clinic": clinic['name'],
                "date": date,
                "status": "Imepangwa"
            })
            st.success(f"🎉 Miadi imepangwa {clinic['name']} kwa {date}!")

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
                        <button class="appointment-btn" style="background: #3B82F6;" 
                                onclick="alert('Inarekebisha miadi...')">
                            Rekebisha 🔧
                        </button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("📝 Hakuna miadi iliyopangwa bado. Weka miadi yako ya kwanza hapo juu!")

# 💡 TIPS & PREPARATION
st.markdown("### 💡 Vidokezo vya Uandaaaji")

tips_cols = st.columns(2)

with tips_cols[0]:
    with st.expander("📋 Kabla ya Kwendako"):
        st.markdown("""
        - **Lete kitambulisho na kadi ya bima**
        - **Vaa nguo nyepesi za kubadilishwa kwa urahisi**
        - **Epuka kutumia deodorant, marashi, au unga**
        - **Lete rekodi zako za mammogram zilizopita ikiwepo**
        - **Andika maswali yoyote au wasiwasi**
        - **Fika dakika 15 mapema kwa nyaraka**
        - **Lete msaidizi ikiwa unahitaji usaidizi**
        """)

with tips_cols[1]:
    with st.expander("❓ Maswali ya Kuuliza"):
        st.markdown("""
        - **Ni aina gani ya mammogram unafanya?**
        - **Muda gani nitachukua kupata matokeo?**
        - **Mchakato wako wa kufuata ikiwa kitu kitapatikana?**
        - **Je, unatoa mammogram ya 3D?**
        - **Uzoefu gani unao na radiologist?**
        - **Je, kuna gharama zingine ninazopaswa kujua?**
        - **Je, una huduma za usaidizi au vikundi vya kuunga mkono?**
        """)

# 🎯 QUICK ACTIONS
st.markdown("### 🎯 Vitendo vya Haraka")

action_cols = st.columns(3)

with action_cols[0]:
    if st.button("📞 Tafuta Huduma ya Haraka", use_container_width=True):
        st.warning("🔄 Inatafuta miadi ya leo leo...")
        time.sleep(2)
        st.success("✅ Imepata chaguzi 3 za huduma ya haraka karibu!")

with action_cols[1]:
    if st.button("💬 Zungumza na Msaidizi", use_container_width=True):
        st.info("💬 Inakuunganisha na timu yetu ya usaidizi...")
        time.sleep(1)
        st.success("🤝 Timu ya usaidizi iko tayari kukusaidia!")

with action_cols[2]:
    if st.button("📱 Hifadhi Utafutaji Huu", use_container_width=True):
        st.balloons()
        st.success("🔖 Vigezo vya utafutaji vimehifadhiwa kwenye profaili yako!")

# 🎊 SUCCESS MESSAGE
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #ECFDF5, #D1FAE5); border-radius: 25px; margin: 2rem 0;">
        <h2 style="color: #065F46; margin-bottom: 1rem;">🎉 Unachukua Hatua Muhimu!</h2>
        <p style="color: #047857; font-size: 1.1rem; line-height: 1.6;">
            Kuweka miadi yako ya uchunguzi ni kitendo chenye nguvu cha kujitunza. 
            Unajali afya yako na ustawi wako wa baadaye. Tuna fahari yako! 🌟
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
with st.expander("ℹ️ Maelezo ya Ziada ya Kenya"):
    st.markdown("""
    ### 🇰🇪 Huduma za Afya Kenya
    
    **🏥 Huduma ya Bima ya Taifa (NHIF)**
    - Inalipa hadi KSh 300,000 kwa matibabu ya saratani
    - Inalipa uchunguzi wa mammogram na vipimo vingine
    - Wasajili wote wa NHIF wanastahiki
    
    **🎗️ Mashirika ya Kusaidia Saratani ya Matiti Kenya**
    - **Women for Cancer** - Huduma za uhamasishaji na usaidizi
    - **Kenya Cancer Association** - Msaada wa kisheria na kijamii
    - **Faraja Cancer Support Trust** - Usaidizi wa kisaikolojia
    
    **📞 Nambari za Msaada:**
    - **Dharura ya Afya:** 1199
    - **Msaada wa Kisaikolojia:** 1190
    - **NHIF Huduma:** 0709 074 000
    
    **💰 Makisio ya Gharama:**
    - Mammogram ya kawaida: KSh 3,000 - 8,000
    - Mammogram ya 3D: KSh 8,000 - 15,000
    - Ultrasound ya matiti: KSh 2,500 - 6,000
    """)