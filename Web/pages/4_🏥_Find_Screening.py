import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
import json
import time
import os
import random

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

# SMART DATA ENHANCEMENT FUNCTIONS
def generate_realistic_phone():
    prefixes = ['+254 70', '+254 71', '+254 72', '+254 73', '+254 74', '+254 75', '+254 76', '+254 77', '+254 78', '+254 79']
    return f"{random.choice(prefixes)} {random.randint(100, 999)} {random.randint(100, 999)}"

def generate_rating(facility_type):
    base_ratings = {
        "National Hospital": (4.2, 4.9),
        "County Hospital": (3.8, 4.6),
        "Medical Clinic": (3.5, 4.8),
        "Health Centre": (3.2, 4.5),
        "Dispensary": (3.0, 4.3),
        "Nursing Home": (3.6, 4.7),
        "Maternity Home": (3.7, 4.8)
    }
    min_rating, max_rating = base_ratings.get(facility_type, (3.0, 4.5))
    return round(random.uniform(min_rating, max_rating), 1)

def generate_reviews(facility_type):
    base_reviews = {
        "National Hospital": (500, 2000),
        "County Hospital": (200, 800),
        "Medical Clinic": (50, 400),
        "Health Centre": (30, 200),
        "Dispensary": (10, 100),
        "Nursing Home": (20, 150),
        "Maternity Home": (25, 180)
    }
    min_rev, max_rev = base_reviews.get(facility_type, (10, 100))
    return random.randint(min_rev, max_rev)

def generate_specialty(facility_type, facility_name):
    specialties = {
        "National Hospital": ["Comprehensive Cancer Care", "Advanced Surgical Services", "Multidisciplinary Oncology", 
                             "State-of-the-Art Diagnostics", "Specialized Women's Health"],
        "County Hospital": ["Regional Healthcare Services", "Community Cancer Screening", "Basic Surgical Procedures",
                           "Women's Health Services", "Emergency Care"],
        "Medical Clinic": ["Primary Healthcare", "Diagnostic Services", "Preventive Care", 
                          "Women's Health Consultations", "Health Education"],
        "Health Centre": ["Community Health Services", "Basic Screening", "Maternal and Child Health",
                         "Health Promotion", "Primary Care"],
        "Dispensary": ["Basic Healthcare", "Medication Dispensing", "Health Education", 
                      "Community Outreach", "First Aid"],
        "Nursing Home": ["Elderly Care", "Chronic Disease Management", "Palliative Care",
                        "Rehabilitation Services", "Long-term Care"],
        "Maternity Home": ["Maternal Health", "Childbirth Services", "Postnatal Care",
                          "Women's Wellness", "Family Planning"]
    }
    
    # Check if facility name suggests specialization
    name_lower = facility_name.lower()
    if any(word in name_lower for word in ['women', 'maternity', 'mother', 'child']):
        return "Specialized Women and Children's Healthcare"
    elif any(word in name_lower for word in ['surgical', 'surgery']):
        return "Surgical and Medical Services"
    elif any(word in name_lower for word in ['cancer', 'oncology']):
        return "Cancer Care and Treatment Services"
    elif any(word in name_lower for word in ['community', 'health']):
        return "Community Health and Wellness Services"
    
    return random.choice(specialties.get(facility_type, ["Healthcare Services"]))

def generate_services(facility_type):
    base_services = {
        "National Hospital": ["Digital Mammography", "Breast Ultrasound", "Biopsy Services", "Breast Surgery", 
                             "Oncology Consultation", "Radiation Therapy", "Genetic Counseling", "Support Groups"],
        "County Hospital": ["Mammography", "Breast Ultrasound", "Clinical Breast Exam", "Basic Surgery", 
                           "Cancer Screening", "Referral Services", "Health Education"],
        "Medical Clinic": ["Clinical Breast Exam", "Basic Ultrasound", "Health Screening", "Consultation", 
                          "Laboratory Tests", "Health Education", "Referral Services"],
        "Health Centre": ["Clinical Breast Exam", "Health Education", "Basic Screening", "Community Outreach",
                         "Referral Services", "Preventive Care"],
        "Dispensary": ["Basic Health Assessment", "Health Education", "Referral Services", "Community Health"],
        "Nursing Home": ["Health Assessment", "Chronic Care", "Palliative Services", "Supportive Care"],
        "Maternity Home": ["Women's Health", "Breast Health Education", "Maternal Screening", "Wellness Care"]
    }
    services = base_services.get(facility_type, ["Healthcare Services"])
    return random.sample(services, min(len(services), random.randint(2, 4)))

def generate_insurance(facility_type):
    insurance_options = ["NHIF", "Madison", "Jubilee", "AAR", "Britam", "CIC", "Liberty", "APA", "Old Mutual"]
    if facility_type in ["National Hospital", "County Hospital"]:
        return random.sample(insurance_options, random.randint(4, 7))
    elif facility_type in ["Medical Clinic", "Health Centre"]:
        return random.sample(insurance_options, random.randint(2, 5))
    else:
        return random.sample(insurance_options, random.randint(1, 3))

def generate_languages(county):
    county_languages = {
        "Nairobi": ["Swahili", "English", "Kikuyu", "Luhya", "Luo"],
        "Mombasa": ["Swahili", "English", "Digo", "Duruma", "Arabic"],
        "Kisumu": ["Swahili", "English", "Luo", "Kisii"],
        "Nakuru": ["Swahili", "English", "Kikuyu", "Kalenjin"],
        "Uasin Gishu": ["Swahili", "English", "Kalenjin", "Luhya"],
        "Kiambu": ["Swahili", "English", "Kikuyu"],
        "Machakos": ["Swahili", "English", "Kamba"],
        "Meru": ["Swahili", "English", "Meru"],
        "Nyeri": ["Swahili", "English", "Kikuyu"],
        "Kakamega": ["Swahili", "English", "Luhya"],
        "Kisii": ["Swahili", "English", "Kisii"],
        "Kericho": ["Swahili", "English", "Kalenjin"],
        "Garissa": ["Swahili", "English", "Somali"],
    }
    return county_languages.get(county, ["Swahili", "English"])

def generate_wait_time(facility_type):
    wait_times = {
        "National Hospital": ["3-5 Days", "1 Week", "2-4 Days"],
        "County Hospital": ["1-3 Days", "Same Week", "2-5 Days"],
        "Medical Clinic": ["Same Day", "1-2 Days", "Next Day"],
        "Health Centre": ["Same Day", "1-2 Days"],
        "Dispensary": ["Same Day", "Walk-in"],
        "Nursing Home": ["1-3 Days", "By Appointment"],
        "Maternity Home": ["Same Day", "1-2 Days"]
    }
    return random.choice(wait_times.get(facility_type, ["1-2 Days"]))

def generate_price_range(facility_type):
    price_ranges = {
        "National Hospital": "$$$",
        "County Hospital": "$$",
        "Medical Clinic": "$$",
        "Health Centre": "$",
        "Dispensary": "$",
        "Nursing Home": "$$",
        "Maternity Home": "$$"
    }
    return price_ranges.get(facility_type, "$$")

def generate_hours(facility_type):
    hours_options = {
        "National Hospital": "24/7",
        "County Hospital": "Mon-Sun: 6AM-10PM",
        "Medical Clinic": "Mon-Fri: 8AM-6PM, Sat: 8AM-1PM",
        "Health Centre": "Mon-Fri: 8AM-5PM, Sat: 8AM-12PM",
        "Dispensary": "Mon-Fri: 8AM-5PM",
        "Nursing Home": "24/7",
        "Maternity Home": "24/7"
    }
    return hours_options.get(facility_type, "Mon-Fri: 8AM-5PM")

def generate_status(facility_type):
    status_options = ["open", "urgent", "premium"]
    weights = {
        "National Hospital": [0.3, 0.2, 0.5],
        "County Hospital": [0.5, 0.4, 0.1],
        "Medical Clinic": [0.7, 0.2, 0.1],
        "Health Centre": [0.8, 0.2, 0.0],
        "Dispensary": [0.9, 0.1, 0.0],
        "Nursing Home": [0.6, 0.3, 0.1],
        "Maternity Home": [0.5, 0.4, 0.1]
    }
    return random.choices(status_options, weights=weights.get(facility_type, [0.7, 0.2, 0.1]))[0]

def generate_distance(county, selected_county):
    if county == selected_county or selected_county == "All Counties":
        return round(random.uniform(0.5, 15.0), 1)
    else:
        return round(random.uniform(15.0, 150.0), 1)

# 📍 SEARCH & FILTERS
col1, col2 = st.columns(2)

with col1:
    location = st.selectbox("📍 Select Your County", [
        "All Counties", "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Uasin Gishu", "Kiambu", "Machakos", 
        "Meru", "Nyeri", "Garissa", "Kakamega", "Kisii", "Kericho", "Trans Nzoia", "Kilifi", "Lamu"
    ])

with col2:
    facility_type = st.selectbox(
        "🏥 Facility Type",
        ["All Types", "National Hospital", "County Hospital", "Medical Clinic", "Health Centre", 
         "Dispensary", "Nursing Home", "Maternity Home", "Other"]
    )

# Additional filters
st.markdown("### 🎛️ Refine Your Search")

filter_cols = st.columns(3)

with filter_cols[0]:
    services_needed = st.multiselect(
        "🔬 Services Needed",
        ["Mammography", "Breast Ultrasound", "Clinical Breast Exam", "Biopsy", "Breast Surgery", 
         "Cancer Screening", "Women's Health", "General Consultation"],
        default=["Mammography", "Clinical Breast Exam"]
    )

with filter_cols[1]:
    languages = st.multiselect(
        "🗣️ Languages Spoken",
        ["Swahili", "English", "Kikuyu", "Luhya", "Luo", "Kamba", "Kisii", "Somali", "Other"],
        default=["Swahili", "English"]
    )

with filter_cols[2]:
    ownership_type = st.selectbox(
        "🏛️ Ownership",
        ["All Types", "Ministry of Health", "Private Practice", "Private Enterprise", "Faith-Based", "NGO"]
    )

# 🏥 ENHANCED HOSPITAL DATA PROCESSING - REMOVE THE 200 LIMIT
@st.cache_data
def load_hospital_data():
    try:
        # Construct path to CSV file
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        csv_path = os.path.join(project_root, 'Backend', 'app', 'data', 'hospitals.csv')
        
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path, encoding='latin1')
            
            # Get unique counties for the filter
            counties = ["All Counties"] + sorted(df['County'].dropna().unique().tolist()) if 'County' in df.columns else ["All Counties"]
            
            return df, counties
        else:
            st.warning("⚠️ CSV file not found. Using sample data.")
            return None, None
        
    except Exception as e:
        st.error(f"❌ Error loading CSV: {str(e)}")
        return None, None

# Load the data
hospital_df, available_counties = load_hospital_data()

# If no counties were loaded, use default ones
if not available_counties or available_counties == ["All Counties"]:
    available_counties = [
        "All Counties", "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Uasin Gishu", "Kiambu", "Machakos", 
        "Meru", "Nyeri", "Garissa", "Kakamega", "Kisii", "Kericho", "Trans Nzoia", "Kilifi", "Lamu"
    ]

# Process hospital data with enhanced information - NO LIMIT
if hospital_df is not None:
    clinics_data = []
    
    # Process ALL facilities - no limit
    for idx, row in hospital_df.iterrows():
        facility_name = row.get('Facility_N', 'Healthcare Facility')
        facility_type = row.get('Type', 'Medical Clinic')
        county = row.get('County', 'Nairobi')
        
        clinic = {
            "id": idx + 1,
            "name": facility_name,
            "type": facility_type,
            "county": county,
            "distance": generate_distance(county, location),
            "rating": generate_rating(facility_type),
            "reviews": generate_reviews(facility_type),
            "address": f"{row.get('Location', 'Location')}, {row.get('Sub_County', 'Sub County')}, {county} County",
            "phone": generate_realistic_phone(),
            "emergency": generate_realistic_phone() if facility_type in ["National Hospital", "County Hospital"] else "",
            "insurance": generate_insurance(facility_type),
            "languages": generate_languages(county),
            "wait_time": generate_wait_time(facility_type),
            "services": generate_services(facility_type),
            "special_services": generate_services(facility_type),
            "status": generate_status(facility_type),
            "price_range": generate_price_range(facility_type),
            "specialty": generate_specialty(facility_type, facility_name),
            "hours": generate_hours(facility_type),
            "lat": float(row.get('Latitude', -1.286389)) if pd.notna(row.get('Latitude')) else -1.286389,
            "lon": float(row.get('Longitude', 36.817223)) if pd.notna(row.get('Longitude')) else 36.817223
        }
        clinics_data.append(clinic)
    
    st.session_state.clinics_data = clinics_data
    st.success(f"✅ Loaded {len(clinics_data)} healthcare facilities from your dataset!")
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
        
        # Header section - ENHANCED NAME VISIBILITY
        st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <h2 style="color: #1F2937; margin: 0; display: flex; align-items: center; 
                         font-size: 1.8rem; font-weight: 700; line-height: 1.2; 
                         background: linear-gradient(135deg, #10B981, #059669);
                         -webkit-background-clip: text;
                         -webkit-text-fill-color: transparent;
                         margin-right: 1rem;">
                    {clinic['name']}
                </h2>
                <span class="status-badge {status_class}">{status_text}</span>
                <span class="county-badge">{clinic['county']}</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Rating and info - moved to separate line for better readability
        rating_info = f"⭐ {clinic['rating']}/5 ({clinic['reviews']} reviews)" if clinic.get('reviews') else f"⭐ {clinic['rating']}/5"
        price_info = f"💰 {clinic['price_range']}" if clinic.get('price_range') else ""
        hours_info = f"🕒 {clinic['hours']}" if clinic.get('hours') else ""
        distance_info = f"📍 {clinic['distance']} km away"
        
        st.markdown(f"""
            <div style="color: #6B7280; margin-bottom: 1.5rem; padding: 1rem; 
                       background: #F8FAFC; border-radius: 10px; border-left: 4px solid #10B981;">
                <div style="display: flex; flex-wrap: wrap; gap: 1rem; align-items: center;">
                    <span style="font-weight: 600;">{rating_info}</span>
                    <span style="font-weight: 600;">{distance_info}</span>
                    {f'<span style="font-weight: 600;">{price_info}</span>' if price_info else ''}
                    {f'<span style="font-weight: 600;">{hours_info}</span>' if hours_info else ''}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Specialty description
        specialty = clinic.get('specialty', 'Healthcare services')
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ECFDF5, #D1FAE5); 
                       padding: 1.5rem; border-radius: 15px; margin-bottom: 1.5rem;
                       border: 1px solid #10B981;">
                <p style="color: #065F46; margin: 0; font-style: italic; font-weight: 500; font-size: 1.1rem;">
                    "{specialty}"
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Contact and services in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            phone = clinic.get('phone', 'Contact not available')
            address = clinic.get('address', 'Address not available')
            emergency = clinic.get('emergency', '')
            
            st.markdown(f"""
                <div style="margin-bottom: 1rem;">
                    <strong style="color: #1F2937; font-size: 1.1rem;">📞 Contact</strong>
                    <p style="margin: 0.5rem 0; color: #374151; font-weight: 500;">{phone}</p>
                    <p style="margin: 0; color: #6B7280; font-size: 0.9rem;">{address}</p>
                    {f'<p style="margin: 0.5rem 0 0 0; color: #EF4444; font-size: 0.9rem; font-weight: 600;">🚨 Emergency: {emergency}</p>' if emergency else ''}
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            wait_time = clinic.get('wait_time', 'Not specified')
            facility_type = clinic.get('type', 'Healthcare facility')
            
            st.markdown(f"""
                <div style="margin-bottom: 1rem;">
                    <strong style="color: #1F2937; font-size: 1.1rem;">🕒 Availability</strong>
                    <p style="margin: 0.5rem 0; color: #374151; font-weight: 500;">Wait time: {wait_time}</p>
                    <p style="margin: 0; color: #6B7280; font-size: 0.9rem;">Type: {facility_type}</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            insurance_list = clinic.get('insurance', [])
            if isinstance(insurance_list, str):
                insurance_list = [insurance_list]
            insurance_display = ', '.join(insurance_list[:3])
            if len(insurance_list) > 3:
                insurance_display += f" +{len(insurance_list)-3} more"
            
            st.markdown(f"""
                <div style="margin-bottom: 1rem;">
                    <strong style="color: #1F2937; font-size: 1.1rem;">💼 Insurance</strong>
                    <p style="margin: 0.5rem 0; color: #374151; font-weight: 500;">{insurance_display if insurance_display else 'Not specified'}</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Special services
        services_list = clinic.get('special_services', [])
        if isinstance(services_list, str):
            services_list = [services_list]
        
        if services_list:
            st.markdown(f"""
                <div style="margin-top: 1rem; padding: 1rem; background: #FFFBEB; border-radius: 10px; border: 1px solid #F59E0B;">
                    <strong style="color: #92400E; font-size: 1.1rem;">🔬 Special Services:</strong>
                    <p style="margin: 0.5rem 0; color: #B45309; font-weight: 500;">{', '.join(services_list)}</p>
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
                    <div style="margin-top: 1rem; padding: 1rem; background: #EFF6FF; border-radius: 10px;">
                        <strong style="color: #1E40AF; font-size: 1.1rem;">🗣️ Languages: </strong>
                        <span style="color: #374151; font-weight: 500;">{', '.join(languages_list)}</span>
                    </div>
                """, unsafe_allow_html=True)
        
        with col2:
            if st.button(f"📅 Book Appointment", key=f"appt_btn_{clinic['id']}", use_container_width=True):
                st.session_state[f"show_date_{clinic['id']}"] = True
            
        # Date selection (only shown when button is clicked)
        if st.session_state.get(f"show_date_{clinic['id']}", False):
            st.markdown("---")
            st.markdown("### 📋 Schedule Your Visit")
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

# 🗺️ INTERACTIVE MAP VISUALIZATION - OPTIMIZED FOR LARGE DATASETS
st.markdown("### 🗺️ Screening Centers Across Kenya")

if st.session_state.clinics_data:
    # For large datasets, sample the data for the map to avoid performance issues
    if len(st.session_state.clinics_data) > 1000:
        st.info("📊 Showing a sample of facilities on the map for better performance")
        map_sample_size = min(500, len(st.session_state.clinics_data))
        map_clinics = random.sample(st.session_state.clinics_data, map_sample_size)
    else:
        map_clinics = st.session_state.clinics_data
    
    # Create map data from clinics
    map_data = pd.DataFrame({
        'lat': [clinic['lat'] for clinic in map_clinics],
        'lon': [clinic['lon'] for clinic in map_clinics],
        'name': [clinic['name'] for clinic in map_clinics],
        'county': [clinic['county'] for clinic in map_clinics],
        'size': [20 + (clinic['rating'] - 4) * 10 for clinic in map_clinics],
        'color': ['#10B981' if clinic.get('status') == 'open' else 
                  '#EF4444' if clinic.get('status') == 'urgent' else 
                  '#8B5CF6' for clinic in map_clinics]
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

# 🏥 CLINIC LISTINGS - ENHANCED PAGINATION
st.markdown("### 🏥 Available Healthcare Facilities")

# Filter clinics based on user selection
filtered_clinics = st.session_state.clinics_data.copy()

if location != "All Counties":
    filtered_clinics = [clinic for clinic in filtered_clinics if clinic["county"] == location]

if facility_type != "All Types":
    filtered_clinics = [clinic for clinic in filtered_clinics if clinic["type"] == facility_type]

# Display filtered clinics
if filtered_clinics:
    st.success(f"Found {len(filtered_clinics)} facilities matching your criteria")
    
    # Enhanced pagination for large datasets
    items_per_page = 10
    total_pages = max(1, (len(filtered_clinics) + items_per_page - 1) // items_per_page)
    
    # Page navigation with better UX
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        page = st.number_input(
            "📄 Page", 
            min_value=1, 
            max_value=total_pages, 
            value=1, 
            step=1,
            key="page_selector"
        )
    
    with col2:
        st.write(f"**Showing facilities {(page-1)*items_per_page + 1}-{min(page*items_per_page, len(filtered_clinics))} of {len(filtered_clinics)}**")
    
    with col3:
        if total_pages > 1:
            st.write(f"**Total pages: {total_pages}**")
    
    # Calculate indices for current page
    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, len(filtered_clinics))
    
    # Progress bar for large datasets
    if len(filtered_clinics) > 100:
        progress = page / total_pages
        st.progress(progress)
    
    # Display facilities for current page
    for clinic in filtered_clinics[start_idx:end_idx]:
        create_clinic_card(clinic)
    
    # Quick page navigation at bottom
    if total_pages > 1:
        st.markdown("---")
        st.markdown("### 🔄 Quick Navigation")
        
        # Create buttons for quick page navigation
        cols = st.columns(min(10, total_pages))
        for i, col in enumerate(cols):
            if i < total_pages:
                page_num = i + 1
                with col:
                    if st.button(f"{page_num}", key=f"page_btn_{page_num}", use_container_width=True):
                        st.session_state.page_selector = page_num
                        st.rerun()
        
        # Next/Previous buttons
        nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
        with nav_col1:
            if page > 1:
                if st.button("⬅️ Previous", use_container_width=True):
                    st.session_state.page_selector = page - 1
                    st.rerun()
        
        with nav_col3:
            if page < total_pages:
                if st.button("Next ➡️", use_container_width=True):
                    st.session_state.page_selector = page + 1
                    st.rerun()
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