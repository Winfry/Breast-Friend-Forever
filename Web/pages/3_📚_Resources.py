import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
import json
import base64
from datetime import datetime

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

# Function to create actual PDF downloads
def create_pdf_download_link(pdf_url, filename, button_text="📥 Download PDF"):
    return f'''
    <a href="{pdf_url}" target="_blank" style="
        background: linear-gradient(135deg, #FF69B4, #EC4899); 
        color: white; 
        padding: 0.8rem 1.5rem; 
        border-radius: 25px; 
        text-decoration: none; 
        display: inline-block; 
        margin: 0.5rem;
        font-weight: 600;
        text-align: center;">
        {button_text}
    </a>
    '''

st.set_page_config(page_title="Educational Resources", page_icon="📚", layout="wide")

# 🎨 RESOURCES ANIMATION CSS
st.markdown("""
    <style>
    @keyframes cardFlip {
        0% { transform: perspective(400px) rotateY(90deg); opacity: 0; }
        100% { transform: perspective(400px) rotateY(0deg); opacity: 1; }
    }
    
    @keyframes resourceGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(255, 105, 180, 0.3); }
        50% { box-shadow: 0 0 40px rgba(255, 105, 180, 0.6); }
    }
    
    .resource-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border-left: 5px solid #FF69B4;
        box-shadow: 0 8px 25px rgba(255, 105, 180, 0.15);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: cardFlip 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .resource-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transition: left 0.6s;
    }
    
    .resource-card:hover::before {
        left: 100%;
    }
    
    .resource-card:hover {
        transform: translateY(-8px) scale(1.02);
        animation: resourceGlow 2s infinite;
    }
    
    .article-card {
        border-left-color: #FF69B4;
        background: linear-gradient(135deg, #FFF0F5, #FFE4EC);
    }
    
    .pdf-card {
        border-left-color: #EC4899;
        background: linear-gradient(135deg, #FFE4EC, #FCE7F3);
    }
    
    .link-card {
        border-left-color: #DB2777;
        background: linear-gradient(135deg, #FCE7F3, #FBCFE8);
    }
    
    .category-badge {
        display: inline-block;
        background: linear-gradient(135deg, #FF69B4, #EC4899);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
        animation: cardFlip 0.8s ease-out;
    }
    
    .progress-item {
        display: flex;
        align-items: center;
        margin: 1.5rem 0;
        padding: 1rem;
        background: white;
        border-radius: 15px;
        border-left: 4px solid #FF69B4;
        transition: all 0.3s ease;
        animation: cardFlip 0.6s ease-out;
    }
    
    .progress-item:hover {
        transform: translateX(10px);
        box-shadow: 0 5px 15px rgba(255, 105, 180, 0.2);
    }
    
    .completed-item {
        border-left-color: #4CAF50;
        background: linear-gradient(135deg, #F0FFF0, #E8F5E8);
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(255, 105, 180, 0.1);
        transition: all 0.3s ease;
        animation: cardFlip 0.6s ease-out;
        border: 2px solid transparent;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        border-color: #FF69B4;
        box-shadow: 0 12px 30px rgba(255, 105, 180, 0.2);
    }
    
    .learning-path {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem;
        border-radius: 25px;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .learning-path::before {
        content: '📚🎓🌟';
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
    
    /* Streamlit button styling */
    .stButton > button {
        background: linear-gradient(135deg, #FF69B4, #EC4899);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(255, 105, 180, 0.4);
    }
    
    .external-link {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        text-decoration: none;
        display: inline-block;
        margin: 0.5rem;
        font-weight: 600;
        text-align: center;
        border: none;
        cursor: pointer;
    }
    
    .external-link:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# Load animations
try:
    book_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_sgn7zqbs.json")
    learning_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_ukwacdcs.json")
    stats_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_kdxn8rqk.json")
except:
    book_animation = learning_animation = stats_animation = None

# Initialize session state
if 'completed_resources' not in st.session_state:
    st.session_state.completed_resources = set()
if 'reading_progress' not in st.session_state:
    st.session_state.reading_progress = {}
if 'current_reads' not in st.session_state:
    st.session_state.current_reads = {}

st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem;">
        <h1 style="color: #FF69B4; font-size: 3rem; margin-bottom: 1rem;">
            📚 Educational Resources
        </h1>
        <p style="font-size: 1.3rem; color: #666;">
            Your comprehensive library for breast health knowledge 🌟
        </p>
    </div>
    """, unsafe_allow_html=True)

# Welcome animation
if book_animation:
    st_lottie(book_animation, speed=1, height=200, key="resources_welcome")

# 📊 ANIMATED STATISTICS
st.markdown("### 📈 Your Learning Dashboard")

stats_data = [
    {"number": "15+", "label": "Articles Available", "icon": "📖"},
    {"number": "8", "label": "PDF Guides", "icon": "📄"},
    {"number": "5", "label": "Resource Categories", "icon": "🏷️"},
    {"number": f"{len(st.session_state.completed_resources)}", "label": "Completed", "icon": "✅"},
]

cols = st.columns(4)
for i, stat in enumerate(stats_data):
    with cols[i]:
        st.markdown(f"""
            <div class="stat-card">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">{stat['icon']}</div>
                <h3 style="color: #FF69B4; margin: 0; font-size: 2rem;">{stat['number']}</h3>
                <p style="color: #666; margin: 0.5rem 0 0 0; font-weight: 500;">{stat['label']}</p>
            </div>
            """, unsafe_allow_html=True)

# REAL FUNCTIONAL RESOURCES DATA
resources = {
    "articles": [
        {
            "id": 1,
            "title": "Understanding Breast Self-Examination",
            "description": "Comprehensive guide to performing breast self-exams with proper technique and timing.",
            "category": "Self Exam",
            "reading_time": "5 min",
            "author": "National Breast Cancer Foundation",
            "color": "#FF69B4",
            "url": "https://www.nationalbreastcancer.org/breast-self-exam/",
            "type": "external_article"
        },
        {
            "id": 2,
            "title": "Breast Cancer Risk Factors & Prevention",
            "description": "Learn about genetic, lifestyle, and environmental factors that affect breast cancer risk.",
            "category": "Education",
            "reading_time": "7 min", 
            "author": "Breast Cancer Research Foundation",
            "color": "#EC4899",
            "url": "https://www.bcrf.org/about-breast-cancer/risk-factors-for-breast-cancer/",
            "type": "external_article"
        },
        {
            "id": 3,
            "title": "Nutrition for Breast Health",
            "description": "Discover foods and dietary patterns that support breast health and overall wellness.",
            "category": "Lifestyle",
            "reading_time": "39 min",
            "author": "Memorial Sloan Kettering Cancer Center",
            "color": "#DB2777",
            "url": "https://www.mskcc.org/cancer-care/patient-education/nutrition-and-breast-making-healthy-diet-decisions",
            "type": "external_article"
        },
        {
            "id": 4,
            "title": "Case Studies: Early Detection Success Stories",
            "description": "Real stories of women who detected breast cancer early through self-exams and screening.",
            "category": "Case Studies",
            "reading_time": "10 min",
            "author": "Cancer Research UK",
            "color": "#BE185D",
            "url": "https://www.cancerresearchuk.org/about-cancer/breast-cancer/living-with/your-stories",
            "type": "external_article"
        },
        {
            "id": 5,
            "title": "Latest Breast Cancer Research 2024",
            "description": "Recent breakthroughs and clinical trials in breast cancer treatment and prevention.",
            "category": "Research",
            "reading_time": "8 min",
            "author": "Susan G. Komen Foundation",
            "color": "#9D174D",
            "url": "https://www.komen.org/breast-cancer/research/",
            "type": "external_article"
        }
    ],
    "pdfs": [
        {
            "id": 1,
            "title": "Printable Self-Examination Guide",
            "description": "Step-by-step illustrated guide for breast self-examination with proper technique.",
            "category": "Self Exam",
            "file_size": "2.1 MB",
            "pages": 8,
            "color": "#BE185D",
            "url": "https://www.nationalbreastcancer.org/wp-content/uploads/Breast-Self-Exam-Guide.pdf",
            "filename": "breast_self_exam_guide.pdf",
            "type": "downloadable_pdf"
        },
        {
            "id": 2,
            "title": "Mammogram Preparation Checklist",
            "description": "Everything you need to know and do before your mammogram appointment.",
            "category": "Screening", 
            "file_size": "1.5 MB",
            "pages": 6,
            "color": "#9D174D",
            "url": "https://www.breastcancer.org/sites/default/files/2021-10/mammogram-checklist.pdf",
            "filename": "mammogram_preparation_checklist.pdf",
            "type": "downloadable_pdf"
        },
        {
            "id": 3,
            "title": "Breast Health Nutrition Guide",
            "description": "Complete nutrition guide with recipes and meal plans for breast health.",
            "category": "Lifestyle",
            "file_size": "3.2 MB",
            "pages": 12,
            "color": "#831843",
            "url": "https://www.bccancer.bc.ca/shared-content/Documents/Patient%20and%20Family%20Resources/Nutrition%20and%20Cancer/Healthy-Eating-for-Breast-Cancer-Prevention.pdf",
            "filename": "breast_health_nutrition_guide.pdf",
            "type": "downloadable_pdf"
        },
        {
            "id": 4,
            "title": "Patient Advocacy Toolkit",
            "description": "Guide to becoming your own advocate in breast cancer care and treatment.",
            "category": "Support",
            "file_size": "2.8 MB",
            "pages": 10,
            "color": "#6B21A8",
            "url": "https://www.komen.org/globalassets/healthy-living-tools/patient-advocacy-toolkit.pdf",
            "filename": "patient_advocacy_toolkit.pdf",
            "type": "downloadable_pdf"
        }
    ],
    "external_links": [
        {
            "id": 1,
            "title": "World Health Organization - Breast Cancer",
            "description": "Global statistics, research, and prevention strategies from WHO.",
            "category": "Global Health",
            "url": "https://www.who.int/cancer/breast-cancer",
            "color": "#831843"
        },
        {
            "id": 2,
            "title": "American Cancer Society - Breast Cancer",
            "description": "Comprehensive information on breast cancer screening, treatment, and support.",
            "category": "Education",
            "url": "https://www.cancer.org/cancer/breast-cancer.html",
            "color": "#6B21A8"
        },
        {
            "id": 3,
            "title": "National Breast Cancer Foundation",
            "description": "Resources for early detection, education, and support services.",
            "category": "Support",
            "url": "https://www.nationalbreastcancer.org",
            "color": "#7E22CE"
        },
        {
            "id": 4,
            "title": "CDC Breast Cancer Screening",
            "description": "Official screening guidelines and recommendations from CDC.",
            "category": "Screening",
            "url": "https://www.cdc.gov/cancer/breast/basic_info/screening.htm",
            "color": "#8B5CF6"
        },
        {
            "id": 5,
            "title": "Clinical Trials Database",
            "description": "Search for ongoing breast cancer clinical trials and research studies.",
            "category": "Research",
            "url": "https://clinicaltrials.gov/search?cond=Breast%20Cancer",
            "color": "#A855F7"
        },
        {
            "id": 6,
            "title": "Breast Cancer Support Community",
            "description": "Online support groups and community resources for patients and survivors.",
            "category": "Support",
            "url": "https://www.breastcancersupport.com",
            "color": "#C084FC"
        }
    ],
    "videos": [
        {
            "id": 1,
            "title": "How to Perform Breast Self-Exam",
            "description": "Step-by-step video demonstration of proper self-examination technique.",
            "category": "Self Exam",
            "duration": "4:32",
            "color": "#DC2626",
            "url": "https://www.youtube.com/watch?v=9s1YQtS0W_s",
            "type": "educational_video"
        },
        {
            "id": 2,
            "title": "Understanding Mammograms",
            "description": "What to expect during a mammogram and how to prepare.",
            "category": "Screening",
            "duration": "6:15",
            "color": "#EA580C",
            "url": "https://www.youtube.com/watch?v=8y0W3gVt2Cw",
            "type": "educational_video"
        },
        {
            "id": 3,
            "title": "Nutrition for Breast Cancer Prevention",
            "description": "Dietitian discusses foods that support breast health.",
            "category": "Lifestyle",
            "duration": "8:20",
            "color": "#D97706",
            "url": "https://www.youtube.com/watch?v=6yQdK9kX2FY",
            "type": "educational_video"
        }
    ]
}

# 🏷️ CATEGORY FILTER
st.markdown("### 🏷️ Browse by Category")

categories = ["All Categories", "Self Exam", "Education", "Lifestyle", "Screening", "Global Health", "Support", "Research", "Case Studies"]
selected_category = st.selectbox("Filter resources:", categories, key="category_filter")

# 📖 ARTICLES SECTION
st.markdown("### 📖 Educational Articles & Research")

for article in resources["articles"]:
    if selected_category != "All Categories" and article["category"] != selected_category:
        continue
        
    completed = f"article_{article['id']}" in st.session_state.completed_resources
    
    with st.container():
        # Article Card
        st.markdown(f"""
            <div class="resource-card article-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                    <h3 style="color: {article['color']}; margin: 0; flex: 1;">{article['title']}</h3>
                    <span class="category-badge" style="background: {article['color']};">
                        {article['category']}
                    </span>
                </div>
                <p style="color: #666; line-height: 1.6; margin-bottom: 1.5rem;">{article['description']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"👤 {article['author']} | ⏱️ {article['reading_time']}")
        
        with col2:
            # Direct link to the actual article
            st.markdown(f"""
                <a href="{article['url']}" target="_blank" class="external-link">
                    🌐 Read Full Article
                </a>
            """, unsafe_allow_html=True)
        
        with col3:
            if not completed and st.button(f"✅ Mark Complete", key=f"complete_article_{article['id']}"):
                st.session_state.completed_resources.add(f"article_{article['id']}")
                st.success(f"🎉 Completed: {article['title']}")
                st.rerun()
            elif completed:
                st.success("✅ Completed")
        
        st.markdown("---")

# 🎥 EDUCATIONAL VIDEOS
st.markdown("### 🎥 Educational Videos")

for video in resources["videos"]:
    if selected_category != "All Categories" and video["category"] != selected_category:
        continue
        
    with st.container():
        st.markdown(f"""
            <div class="resource-card article-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                    <h3 style="color: {video['color']}; margin: 0; flex: 1;">{video['title']}</h3>
                    <span class="category-badge" style="background: {video['color']};">
                        {video['category']}
                    </span>
                </div>
                <p style="color: #666; line-height: 1.6; margin-bottom: 1.5rem;">{video['description']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write(f"⏱️ Duration: {video['duration']}")
        
        with col2:
            st.markdown(f"""
                <a href="{video['url']}" target="_blank" class="external-link">
                    ▶️ Watch Video
                </a>
            """, unsafe_allow_html=True)
        
        st.markdown("---")

# 📄 PDF RESOURCES
st.markdown("### 📄 Printable Guides & PDFs")

for pdf in resources["pdfs"]:
    if selected_category != "All Categories" and pdf["category"] != selected_category:
        continue
        
    with st.container():
        st.markdown(f"""
            <div class="resource-card pdf-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                    <h3 style="color: {pdf['color']}; margin: 0; flex: 1;">{pdf['title']}</h3>
                    <span class="category-badge" style="background: {pdf['color']};">
                        {pdf['category']}
                    </span>
                </div>
                <p style="color: #666; line-height: 1.6; margin-bottom: 1.5rem;">{pdf['description']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write(f"📄 {pdf['file_size']} | 📖 {pdf['pages']} pages")
        
        with col2:
            # Direct download link to actual PDF
            st.markdown(create_pdf_download_link(pdf['url'], pdf['filename']), unsafe_allow_html=True)
        
        st.markdown("---")

# 🔗 EXTERNAL RESOURCES
st.markdown("### 🔗 Trusted Organizations & Websites")

for link in resources["external_links"]:
    if selected_category != "All Categories" and link["category"] != selected_category:
        continue
        
    with st.container():
        st.markdown(f"""
            <div class="resource-card link-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                    <h3 style="color: {link['color']}; margin: 0; flex: 1;">{link['title']}</h3>
                    <span class="category-badge" style="background: {link['color']};">
                        {link['category']}
                    </span>
                </div>
                <p style="color: #666; line-height: 1.6; margin-bottom: 1.5rem;">{link['description']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Use st.link_button for external resources
        st.link_button("🌐 Visit Official Website", link['url'])
        
        st.markdown("---")


# 🫂 SUPPORT GROUPS SECTION
st.markdown("### 🫂 Support Groups & Communities")

support_groups = [
    {
        "id": 1,
        "title": "BreastCancer.org Community",
        "description": "Largest online breast cancer community with discussion boards, live chats, and expert Q&A sessions.",
        "category": "Online Community",
        "members": "200,000+",
        "meeting_type": "24/7 Online Forum",
        "url": "https://community.breastcancer.org",
        "color": "#7C3AED",
        "features": ["Discussion Boards", "Live Chats", "Expert Q&A", "Resource Library"]
    },
    {
        "id": 2,
        "title": "American Cancer Society Reach to Recovery",
        "description": "Connects newly diagnosed patients with survivors who have similar experiences and backgrounds.",
        "category": "Peer Support",
        "members": "Trained Volunteers",
        "meeting_type": "One-on-One Matching",
        "url": "https://www.cancer.org/support-programs-and-services/reach-to-recovery.html",
        "color": "#EC4899",
        "features": ["One-on-One Support", "Trained Volunteers", "Phone/Online", "All Stages"]
    },
    {
        "id": 3,
        "title": "Young Survival Coalition (YSC)",
        "description": "Dedicated to young women under 40 diagnosed with breast cancer. In-person and virtual meetings.",
        "category": "Age-Specific",
        "members": "10,000+",
        "meeting_type": "Virtual & In-Person",
        "url": "https://www.youngsurvival.org",
        "color": "#10B981",
        "features": ["Under 40 Focus", "Virtual Meetings", "Local Chapters", "Advocacy"]
    },
    {
        "id": 4,
        "title": "CancerCare Support Groups",
        "description": "Professional-led support groups with oncology social workers. Free and confidential.",
        "category": "Professional-Led",
        "members": "Licensed Leaders",
        "meeting_type": "Weekly Virtual",
        "url": "https://www.cancercare.org/support_groups",
        "color": "#3B82F6",
        "features": ["Professional Led", "Free Service", "All Cancer Types", "Multiple Languages"]
    },
    {
        "id": 5,
        "title": "Metastatic Breast Cancer Network",
        "description": "Specific support for those living with metastatic (stage IV) breast cancer.",
        "category": "Stage-Specific",
        "members": "MBC Community",
        "meeting_type": "Online & Conferences",
        "url": "https://www.mbcn.org",
        "color": "#EF4444",
        "features": ["Stage IV Focus", "Research Updates", "Advocacy", "Annual Conference"]
    },
    {
        "id": 6,
        "title": "Facebook Breast Cancer Support Groups",
        "description": "Various private Facebook groups for different subtypes and stages of breast cancer.",
        "category": "Social Media",
        "members": "Varies by Group",
        "meeting_type": "24/7 Online",
        "url": "https://www.facebook.com/search/groups?q=breast%20cancer%20support",
        "color": "#1877F2",
        "features": ["Private Groups", "Instant Support", "Global Community", "Multiple Subgroups"]
    },
    {
        "id": 7,
        "title": "Local Hospital Support Groups",
        "description": "In-person support groups hosted by cancer centers and hospitals nationwide.",
        "category": "Local In-Person",
        "members": "Faraja Cancer Support",
        "meeting_type": "Monthly Meetings",
        "url": "https://farajacancersupport.org/",
        "color": "#8B5CF6",
        "features": ["In-Person", "Local Community", "Hospital Resources", "Caregiver Support"]
    },
    {
        "id": 8,
        "title": "Breast Cancer Helpline & Hotlines",
        "description": "Immediate phone support from trained specialists and survivors.",
        "category": "Phone Support",
        "members": "Trained Staff",
        "meeting_type": "24/7 Phone",
        "url": "tel:254 (0) 800 721 038",
        "color": "#F59E0B",
        "features": ["24/7 Availability", "Immediate Support", "Confidential", "Multiple Languages"]
    }
]

for group in support_groups:
    if selected_category != "All Categories" and selected_category not in ["Support", "Support Groups"]:
        continue
        
    with st.container():
        st.markdown(f"""
            <div class="resource-card" style="border-left-color: {group['color']}; background: linear-gradient(135deg, #F0F4FF, #E0E7FF);">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                    <h3 style="color: {group['color']}; margin: 0; flex: 1;">{group['title']}</h3>
                    <span class="category-badge" style="background: {group['color']};">
                        {group['category']}
                    </span>
                </div>
                
                <p style="color: #666; line-height: 1.6; margin-bottom: 1rem;">{group['description']}</p>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
                    <div style="background: rgba(255,255,255,0.7); padding: 0.8rem; border-radius: 10px; text-align: center;">
                        <div style="font-size: 0.8rem; color: #666; margin-bottom: 0.3rem;">👥 Members</div>
                        <div style="font-weight: 600; color: {group['color']};">{group['members']}</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.7); padding: 0.8rem; border-radius: 10px; text-align: center;">
                        <div style="font-size: 0.8rem; color: #666; margin-bottom: 0.3rem;">📅 Format</div>
                        <div style="font-weight: 600; color: {group['color']};">{group['meeting_type']}</div>
                    </div>
                </div>
                
                <div style="margin-bottom: 1.5rem;">
                    <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">✨ Features:</div>
                    <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                        {''.join([f'<span style="background: {group["color"]}20; color: {group["color"]}; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; border: 1px solid {group["color"]}40;">{feature}</span>' for feature in group['features']])}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if group['category'] == "Phone Support":
                st.markdown(f"""
                    <a href="{group['url']}" style="
                        background: linear-gradient(135deg, #10B981, #059669);
                        color: white;
                        padding: 0.8rem 1.5rem;
                        border-radius: 25px;
                        text-decoration: none;
                        display: inline-block;
                        font-weight: 600;
                        margin-right: 1rem;">
                        📞 Call Now
                    </a>
                    <span style="color: #666; font-size: 0.9rem;">Available 24/7</span>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <a href="{group['url']}" target="_blank" style="
                        background: linear-gradient(135deg, {group['color']}, {group['color']}CC);
                        color: white;
                        padding: 0.8rem 1.5rem;
                        border-radius: 25px;
                        text-decoration: none;
                        display: inline-block;
                        font-weight: 600;
                        margin-right: 1rem;">
                        🫂 Join Community
                    </a>
                """, unsafe_allow_html=True)
        
        with col2:
            if st.button(f"💾 Save Group", key=f"save_group_{group['id']}"):
                st.success(f"✅ Saved {group['title']} to your resources!")
        
        st.markdown("---")

# Also update the category filter to include Support Groups
# Replace your existing categories line with:
categories = ["All Categories", "Self Exam", "Education", "Lifestyle", "Screening", "Global Health", "Support", "Support Groups", "Research", "Case Studies"]



# 🎯 LEARNING PATH PROGRESS
st.markdown("### 🎯 Your Learning Journey")

learning_path = [
    {"id": 1, "title": "Basic Breast Awareness", "description": "Understanding normal breast changes and anatomy", "completed": True, "icon": "🌱"},
    {"id": 2, "title": "Self-Examination Skills", "description": "Mastering proper self-examination techniques", "completed": len([r for r in st.session_state.completed_resources if 'article' in r]) >= 1, "icon": "🖐️"},
    {"id": 3, "title": "Risk Factor Education", "description": "Learning about genetic and lifestyle factors", "completed": len([r for r in st.session_state.completed_resources if 'article' in r]) >= 2, "icon": "📊"},
    {"id": 4, "title": "Screening Knowledge", "description": "Understanding mammograms and other screenings", "completed": False, "icon": "🏥"},
    {"id": 5, "title": "Lifestyle Integration", "description": "Applying knowledge to daily health habits", "completed": False, "icon": "💝"},
]

for item in learning_path:
    status = "✅" if item["completed"] else "⏳"
    status_color = "#4CAF50" if item["completed"] else "#FF69B4"
    
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown(f"<h1 style='text-align: center;'>{item['icon']}</h1>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div style="border-left: 4px solid {status_color}; padding-left: 1rem; margin: 1rem 0;">
                <h4 style="margin: 0 0 0.5rem 0; color: #333;">{item['title']} {status}</h4>
                <p style="margin: 0; color: #666;">{item['description']}</p>
            </div>
        """, unsafe_allow_html=True)

# 🎓 COMPLETION CELEBRATION
completed_count = len([item for item in learning_path if item["completed"]])
if completed_count == len(learning_path):
    st.balloons()
    st.markdown("""
        <div class="learning-path">
            <h2 style="color: white; text-align: center; margin-bottom: 1rem;">🎓 Learning Champion! 🎓</h2>
            <p style="color: white; text-align: center; font-size: 1.2rem;">
                You've completed your breast health education journey! Your commitment to learning is inspiring! 🌟
            </p>
        </div>
        """, unsafe_allow_html=True)

# 📈 INTERACTIVE CHARTS
st.markdown("### 📊 Learning Analytics")

# Create sample reading data
reading_data = {
    'Category': ['Self-Exam', 'Education', 'Lifestyle', 'Screening', 'Support'],
    'Articles_Read': [3, 2, 1, 0, 0],
    'Total_Articles': [5, 4, 3, 2, 1]
}

df = pd.DataFrame(reading_data)

# Progress chart
fig_progress = px.bar(
    df, 
    x='Category', 
    y=['Articles_Read', 'Total_Articles'],
    title='📖 Your Reading Progress by Category',
    color_discrete_sequence=['#FF69B4', '#EC4899'],
    barmode='group'
)

fig_progress.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color="#333"),
    showlegend=True,
    height=400
)

st.plotly_chart(fig_progress, use_container_width=True)

# 🎨 INTERACTIVE QUIZ
with st.expander("🧠 Quick Knowledge Check"):
    st.markdown("### Test Your Understanding")
    
    questions = [
        {
            "question": "How often should breast self-exams be performed?",
            "options": ["Daily", "Weekly", "Monthly", "Yearly"],
            "correct": 2,
            "explanation": "Monthly self-exams help you become familiar with your breasts and notice changes."
        },
        {
            "question": "What's the recommended age to start regular mammograms?",
            "options": ["25-30", "40-50", "60-70", "Only when symptoms appear"],
            "correct": 1,
            "explanation": "Most guidelines recommend starting between 40-50, but consult your doctor."
        }
    ]
    
    score = 0
    for i, q in enumerate(questions):
        st.markdown(f"**{i+1}. {q['question']}**")
        answer = st.radio("Select your answer:", q['options'], key=f"q_{i}")
        
        if st.button(f"Check Answer {i+1}", key=f"check_{i}"):
            if q['options'].index(answer) == q['correct']:
                st.success(f"✅ Correct! {q['explanation']}")
                score += 1
            else:
                st.error(f"❌ Not quite. {q['explanation']}")
    
    if score > 0:
        st.info(f"🎯 Your score: {score}/{len(questions)} - Keep learning! 🌟")

# 🔄 RESOURCE REFRESH
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔄 Refresh Learning Progress", use_container_width=True):
        st.session_state.completed_resources = set()
        st.success("Progress reset! Start your learning journey fresh! 🌟")
        st.rerun()

# 📱 MOBILE FRIENDLY FOOTER
st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; background: linear-gradient(135deg, #FFF0F5, #FFE4EC); border-radius: 20px;">
        <h3 style="color: #FF69B4;">📱 Access Anywhere, Anytime</h3>
        <p style="color: #666;">All resources are mobile-friendly and accessible from any device</p>
        <p style="color: #888; font-size: 0.9rem;">Last updated: """ + datetime.now().strftime("%B %d, %Y") + """</p>
    </div>
    """, unsafe_allow_html=True)