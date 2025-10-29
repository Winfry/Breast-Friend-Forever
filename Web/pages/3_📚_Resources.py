import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
import json
import base64

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

# Function to create downloadable PDF content
def create_pdf_content(content, filename):
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}" style="background: linear-gradient(135deg, #FF69B4, #EC4899); color: white; padding: 0.8rem 1.5rem; border-radius: 25px; text-decoration: none; display: inline-block; margin: 0.5rem;">📥 Download PDF</a>'
    return href

st.set_page_config(page_title="Educational Resources", page_icon="📚", layout="wide")

# 🎨 RESOURCES ANIMATION CSS (same as before)
st.markdown("""
    <style>
    /* Your existing CSS here */
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

# ACTUAL RESOURCE CONTENT
breast_self_exam_content = """
# Understanding Breast Self-Examination

## Why Self-Exams Are Important
Regular breast self-exams help you become familiar with how your breasts normally look and feel so you can notice any changes.

## How to Perform a Self-Exam

### Step 1: Visual Inspection
- Stand in front of a mirror with your shoulders straight and arms on your hips
- Look for:
  - Changes in size, shape, or color
  - Dimpling, puckering, or bulging of the skin
  - Nipple changes or discharge
  - Redness, soreness, rash, or swelling

### Step 2: Manual Examination - Standing
- Raise your right arm overhead
- Use the pads of your three middle fingers on your left hand to feel for lumps
- Move in a circular pattern covering the entire breast and armpit area
- Use light, medium, and firm pressure
- Repeat on the other side

### Step 3: Manual Examination - Lying Down
- Lie down and place a pillow under your right shoulder
- Use the same circular motion with your left hand
- Cover the entire breast area and armpit
- Repeat on the other side

## When to Perform Self-Exams
- **Best time**: 3-5 days after your period ends
- **Post-menopausal**: Same day each month
- **Frequency**: Once per month

## What to Look For
- New lumps or thickening
- Changes in breast size or shape
- Skin changes (redness, dimpling)
- Nipple changes (inversion, discharge)
- Persistent pain in one spot

## When to See a Doctor
Contact your healthcare provider if you notice:
- Any new lump or mass
- Changes that concern you
- Persistent symptoms

*Remember: Most breast changes are not cancer, but it's important to get them checked.*
"""

nutrition_breast_health_content = """
# Nutrition for Optimal Breast Health

## Foods That Support Breast Health

### 🥦 Cruciferous Vegetables
- Broccoli, cauliflower, cabbage, Brussels sprouts
- Contain indole-3-carbinol and sulforaphane
- Help balance estrogen metabolism

### 🫐 Berries and Colorful Fruits
- Blueberries, strawberries, raspberries
- Rich in antioxidants that fight free radicals
- Reduce inflammation

### 🐟 Omega-3 Rich Foods
- Salmon, mackerel, sardines
- Walnuts, flaxseeds, chia seeds
- Anti-inflammatory properties

### 🌿 Fiber-Rich Foods
- wholewheat couscous and quinoa Pulses such as lentils and beans
- Starchy foods such as potatoes and sweet potatoes, ideally
with their skins on
- Vegetables and fruits
- Help eliminate excess estrogen
- Support healthy digestion

### 🥜 Healthy Fats
- Olive oil, rapeseed oil and their spreads,Oily fish such as salmon and mackerel, Avocado, Nuts and seeds
- Support hormone balance
- Aid nutrient absorption

## Foods to Limit

### ❌ Processed Foods
- High in unhealthy fats and additives
- Can promote inflammation

### ❌ Sugary Drinks and Snacks
- May contribute to weight gain
- Can increase inflammation

### ❌ Excessive Alcohol
- Limit to 1 drink per day or less
- Alcohol can increase estrogen levels

## Sample Daily Eating Plan

### Breakfast
- Greek yogurt with berries and walnuts
- Green tea

### Lunch
- Large salad with mixed greens, chickpeas, and olive oil dressing
- Grilled chicken or tofu

### Dinner
- Baked salmon with roasted broccoli and quinoa
- Steamed carrots

### Snacks
- Apple with almond butter
- Carrot sticks with hummus

## Important Nutrients

### Vitamin D
- Supports immune function
- Sources: sunlight, fatty fish, fortified foods

### Calcium
- Bone health
- Sources: dairy, leafy greens, fortified plant milks

### Antioxidants
- Protect cells from damage
- Sources: colorful fruits and vegetables

## Lifestyle Factors

### Maintain Healthy Weight
- Excess weight can increase breast cancer risk
- Focus on gradual, sustainable weight loss if needed

### Stay Active
- Aim for 150 minutes of moderate exercise weekly
- Include strength training twice weekly

### Limit Alcohol
- Stick to recommended guidelines
- Consider alcohol-free days

*Note: Always consult with a healthcare provider before making significant dietary changes.*
"""

risk_factors_content = """
# Breast Cancer Risk Factors & Prevention

## Understanding Your Risk

### Non-Modifiable Risk Factors

#### 🔬 Genetic Factors
- **BRCA1 and BRCA2 gene mutations**
- Family history of breast cancer
- Personal history of breast conditions
- Inherited risk factors

#### 👵 Age and Gender
- Risk increases with age
- Women are at higher risk than men
- Most cases occur after age 50

#### 🩺 Reproductive History
- Early menstruation (before age 12)
- Late menopause (after age 55)
- First pregnancy after age 30
- Never carrying a pregnancy to term

#### 📊 Personal Health History
- Previous breast cancer
- Certain non-cancerous breast conditions
- Chest radiation therapy before age 30

### Modifiable Risk Factors

#### 🏃‍♀️ Lifestyle Factors
- **Physical inactivity**
- Being overweight or obese (especially after menopause)
- **Alcohol consumption**
- Smoking

#### 💊 Hormone Factors
- Hormone replacement therapy
- Oral contraceptive use

## Prevention Strategies

### Lifestyle Changes

#### 🥗 Healthy Eating
- Follow a balanced diet rich in fruits and vegetables
- Limit processed foods and red meat
- Maintain healthy weight

#### 🏃‍♀️ Regular Exercise
- Aim for 150-300 minutes of moderate activity weekly
- Include strength training
- Stay active throughout life

#### 🍷 Alcohol Moderation
- Limit to 1 drink per day or less
- Consider alcohol-free days

#### 🚭 Avoid Smoking
- No safe level of tobacco use
- Seek help to quit if needed

### Medical Prevention

#### 🩺 Regular Screening
- Follow recommended mammogram schedules
- Clinical breast exams
- Discuss MRI screening if high risk

#### 💊 Risk-Reducing Medications
- For high-risk women only
- Discuss with healthcare provider
- Understand benefits and risks

#### 🔬 Genetic Counseling
- If strong family history
- Before genetic testing
- To understand risk management options

## Know Your Body

### Breast Awareness
- Know how your breasts normally look and feel
- Report changes promptly
- Don't wait for scheduled screenings

### Symptom Awareness
- New lumps or thickening
- Changes in size, shape, or appearance
- Skin changes or dimpling
- Nipple changes or discharge
- Persistent pain

## When to Seek Help

### Immediate Attention Needed For:
- New, persistent lumps
- Bloody nipple discharge
- Skin changes like orange peel texture
- Sudden breast swelling or pain

### Regular Check-ups
- Annual well-woman exams
- Discuss family history updates
- Review screening schedule

*Remember: Having risk factors doesn't mean you'll get breast cancer, and many women with breast cancer have no known risk factors.*
"""

# Sample PDF content (in real app, you'd use actual PDF files)
self_exam_pdf_content = "Breast Self-Examination Guide PDF Content"
mammogram_checklist_content = "Mammogram Preparation Checklist PDF Content"

# Updated resources data with actual content
resources = {
    "articles": [
        {
            "id": 1,
            "title": "Understanding Breast Self-Examination",
            "description": "Comprehensive guide to performing breast self-exams with proper technique and timing.",
            "category": "Self Exam",
            "reading_time": "5 min",
            "author": "Dr. Sarah Johnson",
            "color": "#FF69B4",
            "content": breast_self_exam_content
        },
        {
            "id": 2,
            "title": "Breast Cancer Risk Factors & Prevention",
            "description": "Learn about genetic, lifestyle, and environmental factors that affect breast cancer risk.",
            "category": "Education",
            "reading_time": "7 min", 
            "author": "Breast Health Foundation",
            "color": "#EC4899",
            "content": risk_factors_content
        },
        {
            "id": 3,
            "title": "Nutrition for Optimal Breast Health",
            "description": "Discover foods and dietary patterns that support breast health and overall wellness.",
            "category": "Lifestyle",
            "reading_time": "6 min",
            "author": "Nutrition Specialist Team",
            "color": "#DB2777",
            "content": nutrition_breast_health_content
        }
    ],
    "pdfs": [
        {
            "id": 1,
            "title": "Printable Self-Examination Guide",
            "description": "Beautifully designed PDF with step-by-step instructions and illustrations.",
            "category": "Self Exam",
            "file_size": "2.1 MB",
            "pages": 8,
            "color": "#BE185D",
            "content": self_exam_pdf_content,
            "filename": "breast_self_exam_guide.pdf"
        },
        {
            "id": 2,
            "title": "Mammogram Preparation Checklist",
            "description": "Everything you need to know before your mammogram appointment.",
            "category": "Screening", 
            "file_size": "1.5 MB",
            "pages": 6,
            "color": "#9D174D",
            "content": mammogram_checklist_content,
            "filename": "mammogram_preparation_checklist.pdf"
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
            "color": "#831843"
        },
        {
            "id": 3,
            "title": "National Breast Cancer Foundation",
            "description": "Resources for early detection, education, and support services.",
            "category": "Support",
            "url": "https://www.nationalbreastcancer.org",
            "color": "#831843"
        }
    ]
}

# 🏷️ CATEGORY FILTER
st.markdown("### 🏷️ Browse by Category")

categories = ["All Categories", "Self Exam", "Education", "Lifestyle", "Screening", "Global Health", "Support"]
selected_category = st.selectbox("Filter resources:", categories, key="category_filter")

# 📖 ARTICLES SECTION
st.markdown("### 📖 Educational Articles")

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
            </div>
        """, unsafe_allow_html=True)
        
        # Article content
        st.markdown(f"*{article['description']}*")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"👤 {article['author']} | ⏱️ {article['reading_time']}")
        
        with col2:
            col2a, col2b = st.columns(2)
            with col2a:
                if st.button(f"📖 Read", key=f"read_article_{article['id']}"):
                    st.session_state.current_reads[f"article_{article['id']}"] = article
            
            with col2b:
                if not completed and st.button(f"✅ Complete", key=f"complete_article_{article['id']}"):
                    st.session_state.completed_resources.add(f"article_{article['id']}")
                    st.success(f"🎉 Completed: {article['title']}")
                    st.rerun()
                elif completed:
                    st.success("✅ Completed")
        
        # Show article content when "Read" is clicked
        if f"article_{article['id']}" in st.session_state.get('current_reads', {}):
            st.markdown("---")
            st.markdown("### 📖 Article Content")
            st.markdown(article['content'])
            st.markdown("---")
            
            if not completed and st.button(f"✅ Mark as Completed", key=f"mark_complete_{article['id']}"):
                st.session_state.completed_resources.add(f"article_{article['id']}")
                st.success(f"🎉 Completed: {article['title']}")
                st.rerun()
        
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
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"*{pdf['description']}*")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"📄 {pdf['file_size']} | 📖 {pdf['pages']} pages")
        
        with col2:
            # Create downloadable PDF link
            download_link = create_pdf_content(pdf['content'], pdf['filename'])
            st.markdown(download_link, unsafe_allow_html=True)
        
        st.markdown("---")

# 🔗 EXTERNAL RESOURCES
st.markdown("### 🔗 Trusted External Resources")

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
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"*{link['description']}*")
        
        # Use st.link_button for external resources
        st.link_button("🌐 Visit Official Website", link['url'])
        
        st.markdown("---")

# ... rest of your existing code for learning path, charts, quiz, etc.
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

# Continue with your existing charts and quiz code...
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