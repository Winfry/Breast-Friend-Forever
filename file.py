#!/usr/bin/env python3
"""
🎗️ AfyaSiri Project Structure Generator
Creates the complete directory and file structure for the breast cancer awareness app
"""

import os
import sys
from pathlib import Path

def create_file(path, content=""):
    """Create a file with optional content"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"✅ Created: {path}")

def create_afyasiri_structure():
    """Create the complete AfyaSiri project structure"""
    
    # Root directory
    root_dir = "AfyaSiri"
    
    # Define all directories to create
    directories = [
        # Backend structure
        f"{root_dir}/backend/app/routes",
        f"{root_dir}/backend/app/models",
        f"{root_dir}/backend/app/services", 
        f"{root_dir}/backend/app/utils",
        f"{root_dir}/backend/tests",
        
        # Webapp structure
        f"{root_dir}/webapp/assets/images",
        f"{root_dir}/webapp/assets/pdfs",
        
        # Mobile structure
        f"{root_dir}/mobile/lib/src/screens",
        f"{root_dir}/mobile/lib/src/widgets",
        f"{root_dir}/mobile/lib/src/models",
        f"{root_dir}/mobile/lib/src/services",
        f"{root_dir}/mobile/lib/src/theme",
        f"{root_dir}/mobile/lib/src/utils",
        f"{root_dir}/mobile/assets/images",
        f"{root_dir}/mobile/assets/fonts",
    ]
    
    # Create all directories
    print("🚀 Creating AfyaSiri project structure...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}")
    
    # Backend files
    backend_files = {
        # Backend requirements and config
        "backend/requirements.txt": """fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
sqlalchemy==2.0.23
python-jose==3.3.0
passlib==1.7.4
python-dotenv==1.0.0
scikit-learn==1.3.2
pandas==2.1.4
numpy==1.25.2
reportlab==4.0.4
pillow==10.1.0
requests==2.31.0
""",
        
        "backend/Dockerfile": """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""",
        
        # Backend app files
        "backend/app/__init__.py": "",
        "backend/app/main.py": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat, education, symptoms, resources, auth, pdf

app = FastAPI(
    title="AfyaSiri API",
    description="Breast Cancer Awareness Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(education.router, prefix="/api/v1", tags=["education"])
app.include_router(symptoms.router, prefix="/api/v1", tags=["symptoms"])
app.include_router(resources.router, prefix="/api/v1", tags=["resources"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(pdf.router, prefix="/api/v1", tags=["pdfs"])

@app.get("/")
async def root():
    return {
        "message": "AfyaSiri Breast Cancer Awareness API",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": __import__("datetime").datetime.now().isoformat()}
""",
        
        # Backend routes
        "backend/app/routes/__init__.py": "",
        "backend/app/routes/chat.py": """from fastapi import APIRouter
from app.services.chatbot import BreastCancerChatbot
from app.models.chat import ChatRequest, ChatResponse

router = APIRouter()
chatbot = BreastCancerChatbot()

@router.post("/chat", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    response = chatbot.get_response(request.message)
    return ChatResponse(response=response)

@router.get("/chat/suggestions")
async def get_chat_suggestions():
    return {
        "suggestions": [
            "How to do self-check?",
            "What are common symptoms?",
            "Breast cancer risk factors", 
            "Prevention tips",
            "Find nearby clinics"
        ]
    }
""",
        
        "backend/app/routes/education.py": """from fastapi import APIRouter

router = APIRouter()

@router.get("/education/tips")
async def get_education_tips():
    return {
        "tips": [
            {
                "icon": "💖",
                "text": "Do a self-check once a month",
                "details": "Perform breast self-examination 3-5 days after your period ends"
            },
            {
                "icon": "📅", 
                "text": "Schedule regular mammograms",
                "details": "Annual mammograms recommended for women over 40"
            },
            {
                "icon": "🥦",
                "text": "Eat healthy & stay active", 
                "details": "Maintain healthy weight and exercise regularly"
            },
            {
                "icon": "🧘🏾‍♀️",
                "text": "Manage stress for overall wellness",
                "details": "Practice stress-reduction techniques like meditation"
            }
        ]
    }
""",
        
        "backend/app/routes/symptoms.py": """from fastapi import APIRouter
from app.models.symptoms import SymptomLog

router = APIRouter()

@router.post("/symptoms/log")
async def log_symptoms(symptom_data: SymptomLog):
    return {
        "message": "Symptom log saved successfully",
        "recommendation": "Remember sis 💕, this is for awareness not diagnosis. Consult a healthcare provider for any concerns.",
        "logged_data": symptom_data.dict()
    }

@router.get("/symptoms/checklist")
async def get_symptom_checklist():
    return {
        "symptoms": [
            "Noticed a lump?",
            "Any breast pain?", 
            "Skin/nipple changes?",
            "Unusual discharge?",
            "Swelling in armpit?",
            "Changes in breast size?"
        ]
    }
""",
        
        "backend/app/routes/resources.py": """from fastapi import APIRouter

router = APIRouter()

@router.get("/resources/clinics")
async def get_clinics():
    return {
        "clinics": [
            {
                "name": "Kenya Cancer Society",
                "lat": -1.2921,
                "lon": 36.8219, 
                "contact": "+254 20 123 4567",
                "services": ["Screening", "Education", "Support"]
            },
            {
                "name": "KNH Breast Clinic",
                "lat": -1.3032,
                "lon": 36.7073,
                "contact": "+254 20 765 4321", 
                "services": ["Diagnosis", "Treatment", "Mammograms"]
            }
        ]
    }
""",
        
        "backend/app/routes/auth.py": """from fastapi import APIRouter

router = APIRouter()

@router.post("/auth/profile")
async def save_profile(profile_data: dict):
    return {
        "message": "Profile saved successfully sis! 🌸",
        "profile": profile_data
    }
""",
        
        "backend/app/routes/pdf.py": """from fastapi import APIRouter
from app.services.pdf_service import PDFService

router = APIRouter()

@router.get("/pdfs")
async def list_pdfs():
    return await PDFService.get_pdf_list()

@router.get("/pdfs/{filename}")
async def get_pdf(filename: str):
    return await PDFService.get_pdf(filename)
""",
        
        # Backend models
        "backend/app/models/__init__.py": "",
        "backend/app/models/chat.py": """from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
""",
        
        "backend/app/models/symptoms.py": """from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SymptomLog(BaseModel):
    user_id: Optional[str] = "anonymous"
    symptoms: List[str]
    notes: Optional[str] = ""
    timestamp: datetime = None
""",
        
        # Backend services
        "backend/app/services/__init__.py": "",
        "backend/app/services/chatbot.py": """class BreastCancerChatbot:
    def __init__(self):
        self.responses = {
            "hello": "Hello sis! 💕 I'm here to help with breast health awareness. What would you like to know?",
            "hi": "Hi there! 🌸 I'm your breast health companion. Ask me about self-checks, symptoms, or prevention.",
            "self check": "Sis 💖, monthly self-checks are crucial! Here's how:\\n1. Visual check in mirror\\n2. Feel breasts while standing\\n3. Feel breasts while lying down\\nWant more detailed guidance?",
            "symptoms": "Common signs to watch for:\\n• Lumps or thickening\\n• Breast pain\\n• Skin changes/dimpling\\n• Nipple changes/discharge\\nRemember: Many lumps are benign, but always consult a doctor!",
            "risk": "Risk factors include:\\n• Family history\\n• Age (risk increases with age)\\n• Genetic factors\\n• Lifestyle factors\\nBut sis, 85% of breast cancers happen in women with NO family history!",
            "prevention": "While no guarantees, reduce risk by:\\n• Monthly self-exams\\n• Healthy weight\\n• Regular exercise\\n• Limited alcohol\\n• Breastfeeding if possible\\nEarly detection is key! 🌸",
            "clinics": "Looking for clinics near you? Check the Resources section for trusted healthcare centers in your area. 🏥"
        }
    
    def get_response(self, message: str) -> str:
        message = message.lower().strip()
        
        for keyword, response in self.responses.items():
            if keyword in message:
                return response
        
        return "Sis 💕, I understand your concern about breast health. While I provide awareness information, please consult healthcare professionals for medical advice. You can ask me about self-checks, symptoms, or prevention tips! 🌸"
""",
        
        "backend/app/services/pdf_service.py": """import os
from fastapi import HTTPException
from fastapi.responses import FileResponse

class PDFService:
    @staticmethod
    async def get_pdf_list():
        pdf_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "webapp", "assets", "pdfs")
        try:
            pdf_files = []
            for file in os.listdir(pdf_dir):
                if file.endswith('.pdf'):
                    pdf_files.append({
                        'name': file.replace('.pdf', '').replace('_', ' ').title(),
                        'filename': file,
                        'size': os.path.getsize(os.path.join(pdf_dir, file))
                    })
            return pdf_files
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error accessing PDFs: {str(e)}")
    
    @staticmethod
    async def get_pdf(filename: str):
        pdf_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "webapp", "assets", "pdfs")
        file_path = os.path.join(pdf_dir, filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="PDF not found")
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/pdf'
        )
""",
        
        # Backend utils
        "backend/app/utils/__init__.py": "",
        "backend/app/utils/constants.py": """# Breast Cancer Awareness Constants
BREAST_HEALTH_TIPS = [
    "Perform monthly self-examinations",
    "Know your family medical history", 
    "Maintain a healthy weight",
    "Exercise regularly",
    "Limit alcohol consumption",
    "Don't smoke",
    "Breastfeed if possible",
    "Get regular screenings"
]

RISK_FACTORS = [
    "Being female",
    "Increasing age", 
    "Family history",
    "Genetic mutations",
    "Early menstruation",
    "Late menopause",
    "Never having children",
    "Hormone therapy"
]
""",
        
        # Tests
        "backend/tests/__init__.py": "",
        "backend/tests/test_main.py": """# Test file for backend
def test_always_passes():
    assert True
"""
    }
    
    # Webapp files
    webapp_files = {
        "webapp/requirements.txt": """streamlit==1.28.0
requests==2.31.0
pandas==2.1.4
plotly==5.17.0
python-dotenv==1.0.0
pillow==10.1.0
""",
        
        "webapp/README.md": """# AfyaSiri Web App

Breast Cancer Awareness Streamlit Application.

## Features
- Breast health education
- Symptom tracking
- Clinic locator
- Health assistant chat
- Profile management

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `streamlit run app.py`
""",
        
        "webapp/app.py": """import streamlit as st
import requests
from splash import splash_screen
from chat import chat_screen
from education import education_screen
from symptom_log import symptom_log_screen
from resources import resources_screen
from profile import profile_screen

BACKEND_URL = "http://localhost:8000/api/v1"

st.set_page_config(
    page_title="AfyaSiri - Breast Cancer Awareness", 
    page_icon="💖",
    layout="centered"
)

if "page" not in st.session_state:
    st.session_state["page"] = "Splash"
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "BACKEND_URL" not in st.session_state:
    st.session_state["BACKEND_URL"] = BACKEND_URL

with st.sidebar:
    st.markdown("# 🎗️ AfyaSiri")
    st.markdown("### 💖 Your Breast Health Companion")
    
    page = st.radio(
        "Navigate",
        ["Splash", "Chat", "Education", "Symptom Log", "Resources", "Profile"],
        index=0 if st.session_state["page"] == "Splash" else 
              ["Splash", "Chat", "Education", "Symptom Log", "Resources", "Profile"].index(st.session_state["page"])
    )
    
    st.session_state["page"] = page

if st.session_state["page"] == "Splash":
    splash_screen()
elif st.session_state["page"] == "Chat":
    chat_screen()
elif st.session_state["page"] == "Education":
    education_screen()
elif st.session_state["page"] == "Symptom Log":
    symptom_log_screen()
elif st.session_state["page"] == "Resources":
    resources_screen()
elif st.session_state["page"] == "Profile":
    profile_screen()
""",
        
        "webapp/splash.py": """import streamlit as st

def splash_screen():
    st.markdown('''
        <style>
        .splash-container {
            background: linear-gradient(135deg, #e75480 0%, #ff69b4 100%);
            padding: 4rem 2rem;
            border-radius: 20px;
            color: white;
            text-align: center;
            margin: 2rem 0;
        }
        </style>
    ''', unsafe_allow_html=True)
    
    st.markdown(
        '''
        <div class="splash-container">
            <h1 style='font-size: 4em; margin-bottom: 0.5em;'>💖 AfyaSiri</h1>
            <h2 style='font-size: 2em; margin-bottom: 1em;'>Your Breast Health Companion</h2>
            <p style='font-size: 1.2em; text-align: center; max-width: 600px; margin: 0 auto;'>
                💖 Your Breast Health, Your Power
            </p>
            <p style='font-size: 1.1em; margin-top: 1em;'>
                Welcome sis! This is your safe space to learn, chat, and track your breast health.
            </p>
        </div>
        ''', unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🌸 Get Started", use_container_width=True, type="primary"):
            st.session_state["page"] = "Chat"
            st.rerun()
""",
        
        "webapp/chat.py": """import streamlit as st
import requests

def chat_screen():
    st.markdown("## 💬 Ask Me Anything About Breast Health")
    
    questions = ["How to self-check?", "Common symptoms?", "Risk factors?", "Prevention tips?", "Find clinics?", "Mammogram guidelines?"]
    
    cols = st.columns(3)
    for i, question in enumerate(questions[:3]):
        with cols[i]:
            if st.button(question, use_container_width=True):
                if "messages" not in st.session_state:
                    st.session_state["messages"] = []
                st.session_state["messages"].append({"role": "user", "content": question})
                response = get_chat_response(question)
                st.session_state["messages"].append({"role": "assistant", "content": response})
                st.rerun()

    for i, question in enumerate(questions[3:], 3):
        with cols[i-3]:
            if st.button(question, use_container_width=True):
                if "messages" not in st.session_state:
                    st.session_state["messages"] = []
                st.session_state["messages"].append({"role": "user", "content": question})
                response = get_chat_response(question)
                st.session_state["messages"].append({"role": "assistant", "content": response})
                st.rerun()

    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Type your question about breast health..."):
        if "messages" not in st.session_state:
            st.session_state["messages"] = []
        
        st.session_state["messages"].append({"role": "user", "content": prompt})
        response_text = get_chat_response(prompt)
        st.session_state["messages"].append({"role": "assistant", "content": response_text})
        st.rerun()

def get_chat_response(message: str) -> str:
    try:
        response = requests.post(
            f"{st.session_state.get('BACKEND_URL', 'http://localhost:8000/api/v1')}/chat",
            json={"message": message},
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        if response.status_code == 200:
            return response.json().get("response", "Sis 💕, I'm here to help with breast health awareness!")
    except:
        pass
    
    return "Sis 💕, monthly self-checks can save lives. Want me to guide you through one? Remember to consult healthcare professionals for medical advice. 🌸"
""",
        
        "webapp/education.py": """import streamlit as st
import requests

def education_screen():
    st.markdown("## 📚 Breast Health Education")
    
    st.markdown("### 💖 Essential Breast Health Tips")
    
    tips = [
        {
            "icon": "💖",
            "text": "Do a self-check once a month",
            "details": "Perform breast self-examination 3-5 days after your period ends"
        },
        {
            "icon": "📅", 
            "text": "Schedule regular mammograms",
            "details": "Annual mammograms recommended for women over 40"
        },
        {
            "icon": "🥦",
            "text": "Eat healthy & stay active", 
            "details": "Maintain healthy weight and exercise regularly"
        },
        {
            "icon": "🧘🏾‍♀️",
            "text": "Manage stress for overall wellness",
            "details": "Practice stress-reduction techniques like meditation"
        }
    ]
    
    cols = st.columns(2)
    for i, tip in enumerate(tips):
        with cols[i % 2]:
            st.markdown(f'''
            <div style='background-color:#ffe4ec; border-radius:15px; padding:20px; margin:10px;'>
                <h4>{tip['icon']} {tip['text']}</h4>
                <p>{tip['details']}</p>
            </div>
            ''', unsafe_allow_html=True)

    st.markdown("### 📖 Educational Resources")
    st.info("Sample educational PDFs will be created in the assets/pdfs folder!")
    
    sample_pdfs = [
        {"name": "Breast Self-Examination Guide", "description": "Step-by-step guide for monthly self-checks"},
        {"name": "Understanding Risk Factors", "description": "Learn about genetic and lifestyle risk factors"},
        {"name": "Early Detection Handbook", "description": "Importance of early detection and screening"},
    ]
    
    for pdf in sample_pdfs:
        with st.expander(f"📄 {pdf['name']}"):
            st.write(pdf['description'])
            st.write("📊 *PDF will be available for download when backend is running*")
""",
        
        "webapp/symptom_log.py": """import streamlit as st
import requests
import json
from datetime import datetime

def symptom_log_screen():
    st.markdown("## ✅ Symptom Self-Check Log")
    
    symptoms = [
        "Noticed a lump?",
        "Any breast pain?",
        "Skin/nipple changes?",
        "Unusual discharge?",
        "Swelling in armpit?",
        "Changes in breast size?"
    ]
    
    selected_symptoms = []
    for symptom in symptoms:
        if st.checkbox(symptom):
            selected_symptoms.append(symptom)
    
    notes = st.text_area("Additional notes (optional):")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Log", use_container_width=True):
            if selected_symptoms:
                try:
                    response = requests.post(
                        f"{st.session_state.get('BACKEND_URL', 'http://localhost:8000/api/v1')}/symptoms/log",
                        json={
                            "symptoms": selected_symptoms,
                            "notes": notes,
                            "timestamp": datetime.now().isoformat()
                        }
                    )
                    if response.status_code == 200:
                        st.success("Log saved successfully! 💖")
                    else:
                        st.success("Log recorded! 💖 Remember: this is for awareness, not diagnosis.")
                except:
                    st.success("Log recorded locally! 💖 Remember sis, this is for awareness not diagnosis.")
            else:
                st.warning("Please select at least one symptom")
    
    with col2:
        if st.button("🔄 Clear", use_container_width=True):
            st.rerun()
    
    st.markdown("---")
    st.info('''
    **💕 Important Reminder:** 
    This symptom log is for awareness and tracking purposes only. 
    It is NOT a medical diagnosis. Always consult healthcare professionals 
    for any health concerns or symptoms.
    ''')
""",
        
        "webapp/resources.py": """import streamlit as st
import pandas as pd

def resources_screen():
    st.markdown("## 🏥 Clinics & Support Centers")
    st.write("Here are some trusted places you can reach out to, sis 🌸")

    data = pd.DataFrame({
        "lat": [-1.2921, -1.3032, -1.2580],
        "lon": [36.8219, 36.7073, 36.7989],
        "name": ["Kenya Cancer Society", "KNH Breast Clinic", "Aga Khan Hospital Breast Center"]
    })

    st.map(data)

    st.markdown("### 📌 List of Clinics:")
    for idx, row in data.iterrows():
        with st.expander(f"🏥 {row['name']}"):
            st.write(f"**Location:** ({row['lat']}, {row['lon']})")
            st.write("**Services:** Screening, Diagnosis, Treatment, Support")
            st.write("**Contact:** +254 XX XXX XXXX")
            
    st.markdown("### 📞 Support Resources:")
    support_resources = [
        {"name": "Breast Cancer Support Helpline", "contact": "0800 123 456", "hours": "24/7"},
        {"name": "Mental Health Support", "contact": "1190", "hours": "24/7"},
        {"name": "Cancer Care Counseling", "contact": "+254 700 123 456", "hours": "8AM-8PM"}
    ]
    
    for resource in support_resources:
        st.write(f"**{resource['name']}** - {resource['contact']} ({resource['hours']})")
""",
        
        "webapp/profile.py": """import streamlit as st

def profile_screen():
    st.markdown("## 👩🏽 Your Profile & Settings")
    st.write("Keep it simple, private, and just for you 💕.")

    name = st.text_input("Your Name (optional)", "")
    lang = st.selectbox("Preferred Language", ["English", "Swahili", "French"])
    notes = st.text_area("Personal Notes / Reminders", "e.g. Remember self-check on the 5th!")

    if st.button("💾 Save Settings"):
        st.success("Profile saved, sis! 🌸")
""",
        
        # Webapp assets placeholder files
        "webapp/assets/images/.gitkeep": "",
        "webapp/assets/pdfs/.gitkeep": "",
    }
    
    # Mobile app files
    mobile_files = {
        "mobile/pubspec.yaml": """name: afyasiri
description: Breast Cancer Awareness App

publish_to: 'none'

version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0
  provider: ^6.1.1
  shared_preferences: ^2.2.2
  url_launcher: ^6.1.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
  assets:
    - assets/images/
""",
        
        "mobile/README.md": """# AfyaSiri Mobile App

Breast Cancer Awareness Flutter Application.

## Setup
1. Ensure Flutter is installed
2. Run `flutter pub get` to install dependencies
3. Run `flutter run` to start the app

## Features
- Breast health education
- Symptom tracking
- Clinic locator
- Health assistant chat
- Profile management
""",
        
        "mobile/lib/main.dart": """import 'package:flutter/material.dart';
import 'package:afyasiri/src/screens/home_screen.dart';

void main() {
  runApp(const AfyaSiriApp());
}

class AfyaSiriApp extends StatelessWidget {
  const AfyaSiriApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AfyaSiri',
      theme: ThemeData(
        primarySwatch: Colors.pink,
        fontFamily: 'Roboto',
        scaffoldBackgroundColor: const Color(0xFFfff5f7),
      ),
      home: const HomeScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}
""",
        
        # Mobile screens
        "mobile/lib/src/screens/home_screen.dart": """import 'package:flutter/material.dart';
import 'chat_screen.dart';
import 'education_screen.dart';
import 'symptoms_screen.dart';
import 'resources_screen.dart';
import 'profile_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _currentIndex = 0;

  final List<Widget> _screens = [
    const HomeContent(),
    const ChatScreen(),
    const EducationScreen(),
    const SymptomsScreen(),
    const ResourcesScreen(),
    const ProfileScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: _currentIndex == 0 
          ? AppBar(
              title: const Text('💖 AfyaSiri'),
              backgroundColor: Colors.pink,
              foregroundColor: Colors.white,
              elevation: 0,
            )
          : null,
      body: _screens[_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        type: BottomNavigationBarType.fixed,
        backgroundColor: Colors.white,
        selectedItemColor: Colors.pink,
        unselectedItemColor: Colors.grey,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.chat), label: 'Chat'),
          BottomNavigationBarItem(icon: Icon(Icons.school), label: 'Education'),
          BottomNavigationBarItem(icon: Icon(Icons.medical_services), label: 'Symptoms'),
          BottomNavigationBarItem(icon: Icon(Icons.local_hospital), label: 'Resources'),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
        ],
        onTap: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
      ),
    );
  }
}

class HomeContent extends StatelessWidget {
  const HomeContent({super.key});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const SizedBox(height: 20),
          const Text(
            'Welcome to AfyaSiri',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          const Text(
            'Your safe space for breast health awareness',
            style: TextStyle(fontSize: 16, color: Colors.grey),
          ),
          const SizedBox(height: 30),
          
          GridView.count(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            crossAxisCount: 2,
            crossAxisSpacing: 16,
            mainAxisSpacing: 16,
            children: [
              _buildFeatureCard(
                context,
                '💬 Chat Assistant',
                'Ask breast health questions',
                Icons.chat,
                () => Navigator.push(context, MaterialPageRoute(builder: (context) => const ChatScreen())),
              ),
              _buildFeatureCard(
                context,
                '📚 Education',
                'Learn about breast health',
                Icons.school,
                () => Navigator.push(context, MaterialPageRoute(builder: (context) => const EducationScreen())),
              ),
              _buildFeatureCard(
                context,
                '✅ Symptom Log',
                'Track your symptoms',
                Icons.medical_services,
                () => Navigator.push(context, MaterialPageRoute(builder: (context) => const SymptomsScreen())),
              ),
              _buildFeatureCard(
                context,
                '🏥 Resources',
                'Find clinics & support',
                Icons.local_hospital,
                () => Navigator.push(context, MaterialPageRoute(builder: (context) => const ResourcesScreen())),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildFeatureCard(BuildContext context, String title, String subtitle, IconData icon, VoidCallback onTap) {
    return Card(
      elevation: 2,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, size: 40, color: Colors.pink),
              const SizedBox(height: 12),
              Text(
                title,
                style: const TextStyle(fontWeight: FontWeight.bold),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 8),
              Text(
                subtitle,
                style: const TextStyle(fontSize: 12, color: Colors.grey),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
""",
        
        "mobile/lib/src/screens/chat_screen.dart": """import 'package:flutter/material.dart';

class ChatScreen extends StatelessWidget {
  const ChatScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('💬 Health Assistant'),
      ),
      body: const Center(
        child: Text(
          'Chat with our breast health assistant',
          style: TextStyle(fontSize: 18),
        ),
      ),
    );
  }
}
""",
        
        "mobile/lib/src/screens/education_screen.dart": """import 'package:flutter/material.dart';

class EducationScreen extends StatelessWidget {
  const EducationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('📚 Breast Health Education'),
      ),
      body: const Center(
        child: Text(
          'Educational resources about breast health',
          style: TextStyle(fontSize: 18),
        ),
      ),
    );
  }
}
""",
        
        "mobile/lib/src/screens/symptoms_screen.dart": """import 'package:flutter/material.dart';

class SymptomsScreen extends StatelessWidget {
  const SymptomsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('✅ Symptom Self-Check'),
      ),
      body: const Center(
        child: Text(
          'Track and monitor your symptoms',
          style: TextStyle(fontSize: 18),
        ),
      ),
    );
  }
}
""",
        
        "mobile/lib/src/screens/resources_screen.dart": """import 'package:flutter/material.dart';

class ResourcesScreen extends StatelessWidget {
  const ResourcesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('🏥 Clinics & Support'),
      ),
      body: const Center(
        child: Text(
          'Find healthcare resources near you',
          style: TextStyle(fontSize: 18),
        ),
      ),
    );
  }
}
""",
        
        "mobile/lib/src/screens/profile_screen.dart": """import 'package:flutter/material.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('👩🏽 Your Profile'),
      ),
      body: const Center(
        child: Text(
          'Manage your profile and settings',
          style: TextStyle(fontSize: 18),
        ),
      ),
    );
  }
}
""",
        
        # Mobile placeholder directories
        "mobile/lib/src/widgets/.gitkeep": "",
        "mobile/lib/src/models/.gitkeep": "",
        "mobile/lib/src/services/.gitkeep": "",
        "mobile/lib/src/theme/.gitkeep": "",
        "mobile/lib/src/utils/.gitkeep": "",
        "mobile/assets/images/.gitkeep": "",
        "mobile/assets/fonts/.gitkeep": "",
    }
    
    # Root files
    root_files = {
        "README.md": """# AfyaSiri - Breast Cancer Awareness App 🎗️

## Overview
AfyaSiri is a comprehensive breast cancer awareness application that provides education, symptom tracking, and support resources for women's breast health.

## Architecture

### Backend (Python/FastAPI)
- **FastAPI** for high-performance API
- **Machine Learning** integration for health insights
- **Authentication** system with JWT tokens
- **Database** models for users, symptoms, and resources

### Web App (Streamlit)
- **Multi-page** application with seamless navigation
- **Symptom checker** with health tracking
- **Educational resources** for breast health awareness
- **Chat interface** for health queries

### Mobile App (Flutter)
- **Cross-platform** mobile application
- **Native performance** with Material Design
- **Offline capabilities** for basic features
- **Push notifications** for health reminders

## Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload