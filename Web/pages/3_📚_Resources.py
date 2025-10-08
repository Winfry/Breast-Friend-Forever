import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
import json

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

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
    
    @keyframes progressWave {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
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
    
    .download-btn {
        background: linear-gradient(135deg, #FF69B4, #EC4899);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
        position: relative;
        overflow: hidden;
    }
    
    .download-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transition: left 0.5s;
    }
    
    .download-btn:hover::before {
        left: 100%;
    }
    
    .download-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(255, 105, 180, 0.4);
    }
    
    .progress-tracker {
        background: #F0F0F0;
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
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

# Sample resources data
resources = {
    "articles": [
        {
            "id": 1,
            "title": "Understanding Breast Self-Examination",
            "description": "Comprehensive guide to performing breast self-exams with proper technique and timing.",
            "category": "self-exam",
            "reading_time": "5 min",
            "author": "Dr. Sarah Johnson",
            "color": "#FF69B4"
        },
        {
            "id": 2,
            "title": "Breast Cancer Risk Factors & Prevention",
            "description": "Learn about genetic, lifestyle, and environmental factors that affect breast cancer risk.",
            "category": "education",
            "reading_time": "7 min", 
            "author": "Breast Health Foundation",
            "color": "#EC4899"
        },
        {
            "id": 3,
            "title": "Nutrition for Optimal Breast Health",
            "description": "Discover foods and dietary patterns that support breast health and overall wellness.",
            "category": "lifestyle",
            "reading_time": "6 min",
            "author": "Nutrition Specialist Team",
            "color": "#DB2777"
        }
    ],
    "pdfs": [
        {
            "id": 1,
            "title": "Printable Self-Examination Guide",
            "description": "Beautifully designed PDF with step-by-step instructions and illustrations.",
            "category": "self-exam",
            "file_size": "2.1 MB",
            "pages": 8,
            "color": "#BE185D"
        },
        {
            "id": 2,
            "title": "Mammogram Preparation Checklist",
            "description": "Everything you need to know before your mammogram appointment.",
            "category": "screening", 
            "file_size": "1.5 MB",
            "pages": 6,
            "color": "#9D174D"
        }
    ],
    "external_links": [
        {
            "id": 1,
            "title": "World Health Organization - Breast Cancer",
            "description": "Global statistics, research, and prevention strategies from WHO.",
            "category": "global-health",
            "url": "https://www.who.int/cancer/breast-cancer",
            "color": "#831843"
        }
    ]
}

# 🏷️ CATEGORY FILTER
st.markdown("### 🏷️ Browse by Category")

categories = ["All Categories", "self-exam", "education", "lifestyle", "screening", "global-health", "support"]
selected_category = st.selectbox("Filter resources:", categories, key="category_filter")

# 📖 ARTICLES SECTION
st.markdown("### 📖 Educational Articles")

for article in resources["articles"]:
    if selected_category != "All Categories" and article["category"] != selected_category:
        continue
        
    completed = f"article_{article['id']}" in st.session_state.completed_resources
    card_class = "resource-card article-card" + (" completed-item" if completed else "")
    
    st.markdown(f"""
        <div class="{card_class}">
            <div style="display: flex; justify-content: between; align-items: flex-start; margin-bottom: 1rem;">
                <h3 style="color: {article['color']}; margin: 0; flex: 1;">{article['title']}</h3>
                <span class="category-badge" style="background: {article['color']};">
                    {article['category'].replace('-', ' ').title()}
                </span>
            </div>
            
            <p style="color: #666; line-height: 1.6; margin-bottom: 1.5rem;">{article['description']}</p>
            
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="color: #888; font-size: 0.9rem;">
                    <span>👤 {article['author']}</span>
                    <span style="margin-left: 1rem;">⏱️ {article['reading_time']}</span>
                </div>
                
                <div>
                    {"<span style='background: #4CAF50; color: white; padding: 0.5rem 1rem; border-radius: 15px; font-size: 0.8rem; font-weight: 600;'>✅ Completed</span>" if completed else """
                    <button class="download-btn" onclick="alert('Reading article...')">
                        Read Article 📖
                    </button>
                    """}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Handle article completion
    col1, col2 = st.columns([1, 5])
    with col1:
        if not completed and st.button(f"Mark Complete", key=f"article_{article['id']}"):
            st.session_state.completed_resources.add(f"article_{article['id']}")
            st.success(f"🎉 Completed: {article['title']}")
            st.rerun()

# 📄 PDF RESOURCES
st.markdown("### 📄 Printable Guides & PDFs")

for pdf in resources["pdfs"]:
    if selected_category != "All Categories" and pdf["category"] != selected_category:
        continue
        
    st.markdown(f"""
        <div class="resource-card pdf-card">
            <div style="display: flex; justify-content: between; align-items: flex-start; margin-bottom: 1rem;">
                <h3 style="color: {pdf['color']}; margin: 0; flex: 1;">{pdf['title']}</h3>
                <span class="category-badge" style="background: {pdf['color']};">
                    {pdf['category'].replace('-', ' ').title()}
                </span>
            </div>
            
            <p style="color: #666; line-height: 1.6; margin-bottom: 1.5rem;">{pdf['description']}</p>
            
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="color: #888; font-size: 0.9rem;">
                    <span>📄 {pdf['file_size']}</span>
                    <span style="margin-left: 1rem;">📖 {pdf['pages']} pages</span>
                </div>
                
                <button class="download-btn" onclick="alert('Downloading PDF...')">
                    Download PDF ⬇️
                </button>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 🔗 EXTERNAL RESOURCES
st.markdown("### 🔗 Trusted External Resources")

for link in resources["external_links"]:
    if selected_category != "All Categories" and link["category"] != selected_category:
        continue
        
    st.markdown(f"""
        <div class="resource-card link-card">
            <div style="display: flex; justify-content: between; align-items: flex-start; margin-bottom: 1rem;">
                <h3 style="color: {link['color']}; margin: 0; flex: 1;">{link['title']}</h3>
                <span class="category-badge" style="background: {link['color']};">
                    {link['category'].replace('-', ' ').title()}
                </span>
            </div>
            
            <p style="color: #666; line-height: 1.6; margin-bottom: 1.5rem;">{link['description']}</p>
            
            <button class="download-btn" onclick="window.open('{link['url']}', '_blank')">
                Visit Resource 🌐
            </button>
        </div>
        """, unsafe_allow_html=True)

# 🎯 LEARNING PATH PROGRESS
st.markdown("### 🎯 Your Learning Journey")

learning_path = [
    {"id": 1, "title": "Basic Breast Awareness", "description": "Understanding normal breast changes and anatomy", "completed": True, "icon": "🌱"},
    {"id": 2, "title": "Self-Examination Skills", "description": "Mastering proper self-examination techniques", "completed": len([r for r in st.session_state.completed_resources if 'article' in r]) >= 1, "icon": "🖐️"},
    {"id": 3, "title": "Risk Factor Education", "description": "Learning about genetic and lifestyle factors", "completed": len([r for r in st.session_state.completed_resources if 'article' in r]) >= 2, "icon": "📊"},
    {"id": 4, "title": "Screening Knowledge", "description": "Understanding mammograms and other screenings", "completed": False, "icon": "🏥"},
    {"id": 5, "title": "Lifestyle Integration", "description": "Applying knowledge to daily health habits", "completed": False, "icon": "💝"},
]

st.markdown('<div class="progress-tracker">', unsafe_allow_html=True)

for item in learning_path:
    status = "✅" if item["completed"] else "⏳"
    status_color = "#4CAF50" if item["completed"] else "#FF69B4"
    
    st.markdown(f"""
        <div class="progress-item" style="border-left-color: {status_color};">
            <span style="font-size: 2rem; margin-right: 1.5rem;">{item['icon']}</span>
            <div style="flex: 1;">
                <h4 style="margin: 0 0 0.5rem 0; color: #333;">{item['title']}</h4>
                <p style="margin: 0; color: #666;">{item['description']}</p>
            </div>
            <span style="color: {status_color}; font-size: 1.5rem; font-weight: bold;">{status}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

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
if st.button("🔄 Refresh Learning Progress", use_container_width=True):
    st.session_state.completed_resources = set()
    st.rerun()