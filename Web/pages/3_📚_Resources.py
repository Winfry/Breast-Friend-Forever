import streamlit as st
import requests

st.set_page_config(page_title="Educational Resources", page_icon="📚")

st.markdown("# 📚 Educational Resources")
st.caption("Your comprehensive library for breast health information")

# 📁 Sample Resources Data (in real app, this comes from backend)
resources = {
    "articles": [
        {
            "id": 1,
            "title": "Understanding Breast Self-Examination",
            "description": "Learn the proper technique for checking your breasts at home", 
            "category": "self-exam",
            "reading_time": "5 min"
        },
        {
            "id": 2, 
            "title": "Breast Cancer Risk Factors",
            "description": "Understanding what increases your risk and what you can control",
            "category": "education",
            "reading_time": "7 min"
        },
        {
            "id": 3,
            "title": "Nutrition for Breast Health", 
            "description": "Foods and dietary habits that support breast health",
            "category": "lifestyle", 
            "reading_time": "6 min"
        }
    ],
    "pdfs": [
        {
            "id": 1,
            "title": "Breast Self-Examination Guide",
            "description": "Printable step-by-step guide with illustrations", 
            "category": "self-exam"
        },
        {
            "id": 2,
            "title": "Understanding Mammography",
            "description": "What to expect during your mammogram appointment",
            "category": "screening"
        }
    ]
}

# 🏷️ Category Filter
categories = ["all", "self-exam", "education", "lifestyle", "screening"]
selected_category = st.selectbox("Filter by category", categories, index=0)

# 📑 Tabbed Interface for different resource types
tab1, tab2 = st.tabs(["📖 Articles", "📄 PDF Guides"])

with tab1:
    st.subheader("📖 Educational Articles")
    articles = resources["articles"]
    
    # Apply category filter
    if selected_category != "all":
        articles = [article for article in articles if article["category"] == selected_category]
    
    # Display articles as expandable cards
    for article in articles:
        with st.expander(f"**{article['title']}** - {article['reading_time']}"):
            st.write(article["description"])
            st.caption(f"Category: {article['category']}")

with tab2:
    st.subheader("📄 Printable PDF Guides")
    pdfs = resources["pdfs"]
    
    # Apply category filter  
    if selected_category != "all":
        pdfs = [pdf for pdf in pdfs if pdf["category"] == selected_category]
    
    # Display PDFs with download buttons
    for pdf in pdfs:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{pdf['title']}**")
            st.write(pdf["description"])
        with col2:
            st.download_button(
                label="Download",
                data="",  # In real app, this would be PDF data from backend
                file_name=f"{pdf['title']}.pdf",
                mime="application/pdf"
            )

# 📊 Resource Statistics
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Articles", len(resources["articles"]))
with col2:
    st.metric("PDF Guides", len(resources["pdfs"]))
with col3:
    st.metric("Categories", len(categories)-1)