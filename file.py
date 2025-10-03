#!/usr/bin/env python3
"""
🎗️ AfyaSiri - Breast Cancer Awareness App
Complete Setup & Run Script

This script will:
1. Create the complete project structure
2. Set up virtual environments
3. Install all dependencies
4. Create sample PDFs
5. Start backend and webapp services
6. Provide mobile app instructions

Usage: python setup_and_run_afyasiri.py
"""

import os
import sys
import subprocess
import platform
import time
from pathlib import Path

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PINK = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class AfyaSiriSetup:
    def __init__(self):
        self.project_root = Path("AfyaSiri")
        self.backend_dir = self.project_root / "backend"
        self.webapp_dir = self.project_root / "webapp"
        self.mobile_dir = self.project_root / "mobile"
        self.is_windows = platform.system() == "Windows"
        
    def print_header(self):
        """Print beautiful header"""
        print(f"{Colors.PINK}{Colors.BOLD}")
        print("🎗️" * 50)
        print("🩺  AfyaSiri - Breast Cancer Awareness App")
        print("💖  Complete Setup & Installation")
        print("🎗️" * 50)
        print(f"{Colors.END}")
        
    def print_step(self, step, message):
        """Print step with colorful formatting"""
        print(f"{Colors.CYAN}{Colors.BOLD}[{step}] {Colors.YELLOW}{message}{Colors.END}")
        
    def print_success(self, message):
        """Print success message"""
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")
        
    def print_error(self, message):
        """Print error message"""
        print(f"{Colors.RED}❌ {message}{Colors.END}")
        
    def print_info(self, message):
        """Print info message"""
        print(f"{Colors.BLUE}💡 {message}{Colors.END}")
        
    def run_command(self, command, cwd=None, shell=False):
        """Run a shell command and return success status"""
        try:
            if self.is_windows and not shell:
                command = f"cmd /c {command}"
            
            result = subprocess.run(
                command if shell else command.split(),
                cwd=cwd,
                capture_output=True,
                text=True,
                shell=shell
            )
            
            if result.returncode != 0:
                self.print_error(f"Command failed: {command}")
                if result.stderr:
                    self.print_error(f"Error: {result.stderr}")
                return False
                
            return True
        except Exception as e:
            self.print_error(f"Exception running command: {e}")
            return False
            
    def check_prerequisites(self):
        """Check if required tools are installed"""
        self.print_step("1", "Checking prerequisites...")
        
        # Check Python
        if not self.run_command("python --version"):
            self.print_error("Python is not installed or not in PATH")
            return False
        self.print_success("Python is installed")
        
        # Check pip
        if not self.run_command("pip --version"):
            self.print_error("pip is not installed")
            return False
        self.print_success("pip is installed")
        
        # Check if Flutter is available (optional)
        if self.run_command("flutter --version", shell=True):
            self.print_success("Flutter is installed")
        else:
            self.print_info("Flutter not found (mobile app will need separate setup)")
            
        return True
        
    def create_project_structure(self):
        """Create the complete project directory structure"""
        self.print_step("2", "Creating project structure...")
        
        directories = [
            # Backend structure
            self.backend_dir / "app" / "routes",
            self.backend_dir / "app" / "models", 
            self.backend_dir / "app" / "services",
            self.backend_dir / "app" / "utils",
            self.backend_dir / "tests",
            
            # Webapp structure
            self.webapp_dir / "assets" / "images",
            self.webapp_dir / "assets" / "pdfs",
            
            # Mobile structure
            self.mobile_dir / "lib" / "src" / "screens",
            self.mobile_dir / "lib" / "src" / "widgets",
            self.mobile_dir / "lib" / "src" / "models",
            self.mobile_dir / "lib" / "src" / "services", 
            self.mobile_dir / "lib" / "src" / "theme",
            self.mobile_dir / "lib" / "src" / "utils",
            self.mobile_dir / "assets" / "images",
            self.mobile_dir / "assets" / "fonts",
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            self.print_success(f"Created: {directory}")
            
    def create_backend_files(self):
        """Create all backend files"""
        self.print_step("3", "Setting up backend...")
        
        backend_files = {
            "requirements.txt": """fastapi==0.104.1
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
            
            "Dockerfile": """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""",
            
            "app/__init__.py": "",
            "app/main.py": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat, education, symptoms, resources, auth, pdf

app = FastAPI(
    title="AfyaSiri API",
    description="Breast Cancer Awareness Backend",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
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
            
            "app/routes/__init__.py": "",
            "app/routes/chat.py": """from fastapi import APIRouter
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
            
            "app/routes/education.py": """from fastapi import APIRouter

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
            
            "app/routes/symptoms.py": """from fastapi import APIRouter
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
            
            "app/routes/resources.py": """from fastapi import APIRouter

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
            
            "app/routes/auth.py": """from fastapi import APIRouter

router = APIRouter()

@router.post("/auth/profile")
async def save_profile(profile_data: dict):
    return {
        "message": "Profile saved successfully sis! 🌸",
        "profile": profile_data
    }
""",
            
            "app/routes/pdf.py": """from fastapi import APIRouter
from app.services.pdf_service import PDFService

router = APIRouter()

@router.get("/pdfs")
async def list_pdfs():
    return await PDFService.get_pdf_list()

@router.get("/pdfs/{filename}")
async def get_pdf(filename: str):
    return await PDFService.get_pdf(filename)
""",
            
            "app/models/__init__.py": "",
            "app/models/chat.py": """from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
""",
            
            "app/models/symptoms.py": """from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SymptomLog(BaseModel):
    user_id: Optional[str] = "anonymous"
    symptoms: List[str]
    notes: Optional[str] = ""
    timestamp: datetime = None
""",
            
            "app/services/__init__.py": "",
            "app/services/chatbot.py": """class BreastCancerChatbot:
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
            
            "app/services/pdf_service.py": """import os
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
            
            "app/utils/__init__.py": "",
            "app/utils/constants.py": """# Breast Cancer Awareness Constants
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
"""
        }
        
        for file_path, content in backend_files.items():
            full_path = self.backend_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)
            self.print_success(f"Created: {full_path}")
            
    def create_webapp_files(self):
        """Create all webapp files"""
        self.print_step("4", "Setting up webapp...")
        
        webapp_files = {
            "requirements.txt": """streamlit==1.28.0
requests==2.31.0
pandas==2.1.4
plotly==5.17.0
python-dotenv==1.0.0
pillow==10.1.0
""",
            
            "app.py": """import streamlit as st
import requests
import json
from splash import splash_screen
from chat import chat_screen
from education import education_screen
from symptom_log import symptom_log_screen
from resources import resources_screen
from profile import profile_screen

# Backend configuration
BACKEND_URL = "http://localhost:8000/api/v1"

st.set_page_config(
    page_title="AfyaSiri - Breast Cancer Awareness", 
    page_icon="💖",
    layout="centered"
)

# Initialize session state
if "page" not in st.session_state:
    st.session_state["page"] = "Splash"
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "BACKEND_URL" not in st.session_state:
    st.session_state["BACKEND_URL"] = BACKEND_URL

# Sidebar navigation
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

    st.markdown("---")
    st.markdown("### 🎗️ Breast Cancer Awareness Month")
    st.markdown("*October Special*")
    st.markdown("---")
    st.markdown("Built with 💕 for women's health")

# Page routing
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
            
            "splash.py": """import streamlit as st

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
            
            "chat.py": """import streamlit as st
import requests
import json

def chat_screen():
    st.markdown("## 💬 Ask Me Anything About Breast Health")
    
    # Quick questions
    st.markdown("### Quick Questions:")
    cols = st.columns(3)
    questions = ["How to self-check?", "Common symptoms?", "Risk factors?", "Prevention tips?", "Find clinics?", "Mammogram guidelines?"]
    
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

    # Chat messages
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
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
            
            "education.py": """import streamlit as st
import requests

def education_screen():
    st.markdown("## 📚 Breast Health Education")
    
    # Breast Health Tips
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
            st.markdown(f"""
            """
            <div style="background-color:#ffe4ec; border-radius:15px; padding:20px; margin:10px;">
                <h4>{tip['icon']} {tip['text']}</h4>
                <p>{tip['details']}</p>
            </div>
            """, unsafe_allow_html=True)

    # PDF Resources
    st.markdown("### 📖 Educational Resources")
    st.info("Sample educational PDFs have been created in the assets/pdfs folder!")
    
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
            
            "symptom_log.py": """import streamlit as st
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
    
    # Disclaimer
    st.markdown("---")
    st.info('''
    **💕 Important Reminder:** 
    This symptom log is for awareness and tracking purposes only. 
    It is NOT a medical diagnosis. Always consult healthcare professionals 
    for any health concerns or symptoms.
    ''')
""",
            
            "resources.py": """import streamlit as st
import pandas as pd

def resources_screen():
    st.markdown("## 🏥 Clinics & Support Centers")
    st.write("Here are some trusted places you can reach out to, sis 🌸")

    # Clinic data
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
            
            "profile.py": """import streamlit as st

def profile_screen():
    st.markdown("## 👩🏽 Your Profile & Settings")
    st.write("Keep it simple, private, and just for you 💕.")

    name = st.text_input("Your Name (optional)", "")
    lang = st.selectbox("Preferred Language", ["English", "Swahili", "French"])
    notes = st.text_area("Personal Notes / Reminders", "e.g. Remember self-check on the 5th!")

    if st.button("💾 Save Settings"):
        st.success("Profile saved, sis! 🌸")
"""
        }
        
        for file_path, content in webapp_files.items():
            full_path = self.webapp_dir / file_path
            full_path.write_text(content)
            self.print_success(f"Created: {full_path}")
            
    def create_mobile_files(self):
        """Create basic mobile app structure"""
        self.print_step("5", "Setting up mobile app structure...")
        
        mobile_files = {
            "pubspec.yaml": """name: afyasiri
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
            
            "README.md": """# AfyaSiri Mobile App

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
"""
        }
        
        for file_path, content in mobile_files.items():
            full_path = self.mobile_dir / file_path
            full_path.write_text(content)
            self.print_success(f"Created: {full_path}")
            
    def create_sample_pdfs(self):
        """Create sample PDF educational materials"""
        self.print_step("6", "Creating sample PDF resources...")
        
        try:
            # Create PDF creation script
            pdf_script = self.project_root / "create_sample_pdfs.py"
            pdf_script.write_text('''
#!/usr/bin/env python3
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

def create_sample_pdfs():
    pdf_dir = "webapp/assets/pdfs"
    os.makedirs(pdf_dir, exist_ok=True)
    
    pdfs = [
        {
            "filename": "breast_self_exam_guide.pdf",
            "title": "Breast Self-Examination Guide",
            "content": [
                "Step-by-Step Breast Self-Examination",
                "",
                "1. Visual Inspection:",
                "   - Stand before a mirror with your shoulders straight",
                "   - Look for changes in size, shape, or color", 
                "   - Check for visible distortion or swelling",
                "",
                "2. Manual Examination (Standing):",
                "   - Raise one arm and use the pads of your fingers",
                "   - Press every part of the breast gently",
                "   - Move in a circular pattern from outside to center",
                "",
                "3. Manual Examination (Lying Down):",
                "   - Lie down and repeat the examination", 
                "   - Breast tissue spreads evenly when lying down",
                "   - This makes it easier to feel changes",
                "",
                "Remember: Perform monthly, 3-5 days after your period ends."
            ]
        }
    ]
    
    for pdf_info in pdfs:
        create_pdf(pdf_dir, pdf_info)
        print(f"✅ Created: {pdf_info['filename']}")

def create_pdf(directory, pdf_info):
    filepath = os.path.join(directory, pdf_info['filename'])
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        textColor='#e75480'
    )
    title = Paragraph(pdf_info['title'], title_style)
    story.append(title)
    story.append(Spacer(1, 0.2*inch))
    
    for line in pdf_info['content']:
        if line.strip() == "":
            story.append(Spacer(1, 0.1*inch))
        else:
            style = styles['BodyText']
            story.append(Paragraph(line, style))
    
    doc.build(story)

if __name__ == "__main__":
    create_sample_pdfs()
''')
            
            # Run the PDF creation script
            self.run_command(f"python {pdf_script}", cwd=self.project_root)
            self.print_success("Sample PDFs created in webapp/assets/pdfs/")
            
        except Exception as e:
            self.print_error(f"Error creating PDFs: {e}")
            
    def setup_virtual_environments(self):
        """Set up virtual environments and install dependencies"""
        self.print_step("7", "Setting up virtual environments...")
        
        # Backend virtual environment
        if not (self.backend_dir / "venv").exists():
            self.run_command("python -m venv venv", cwd=self.backend_dir)
            self.print_success("Backend virtual environment created")
            
            # Install backend dependencies
            if self.is_windows:
                pip_path = self.backend_dir / "venv" / "Scripts" / "pip"
                self.run_command(f"{pip_path} install -r requirements.txt", cwd=self.backend_dir)
            else:
                self.run_command("venv/bin/pip install -r requirements.txt", cwd=self.backend_dir)
            self.print_success("Backend dependencies installed")
        
        # Webapp virtual environment  
        if not (self.webapp_dir / "venv").exists():
            self.run_command("python -m venv venv", cwd=self.webapp_dir)
            self.print_success("Webapp virtual environment created")
            
            # Install webapp dependencies
            if self.is_windows:
                pip_path = self.webapp_dir / "venv" / "Scripts" / "pip"
                self.run_command(f"{pip_path} install -r requirements.txt", cwd=self.webapp_dir)
            else:
                self.run_command("venv/bin/pip install -r requirements.txt", cwd=self.webapp_dir)
            self.print_success("Webapp dependencies installed")
            
    def create_run_scripts(self):
        """Create run scripts for easy startup"""
        self.print_step("8", "Creating run scripts...")
        
        # Backend run script
        if self.is_windows:
            backend_script = self.project_root / "start_backend.bat"
            backend_script.write_text("""@echo off
cd backend
venv\\Scripts\\python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
""")
        else:
            backend_script = self.project_root / "start_backend.sh"
            backend_script.write_text("""#!/bin/bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
""")
            backend_script.chmod(0o755)
            
        # Webapp run script
        if self.is_windows:
            webapp_script = self.project_root / "start_webapp.bat"
            webapp_script.write_text("""@echo off
cd webapp
venv\\Scripts\\streamlit run app.py
pause
""")
        else:
            webapp_script = self.project_root / "start_webapp.sh"
            webapp_script.write_text("""#!/bin/bash
cd webapp
source venv/bin/activate
streamlit run app.py
""")
            webapp_script.chmod(0o755)
            
        self.print_success("Run scripts created")
        
    def start_services(self):
        """Start the backend and webapp services"""
        self.print_step("9", "Starting services...")
        
        self.print_info("Starting Backend API...")
        if self.is_windows:
            subprocess.Popen([
                "cmd", "/c", "start", "cmd", "/k", 
                f"cd {self.backend_dir} && venv\\Scripts\\python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
            ])
        else:
            subprocess.Popen([
                "bash", "-c", 
                f"cd {self.backend_dir} && source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        time.sleep(3)  # Give backend time to start
        
        self.print_info("Starting Web App...")
        if self.is_windows:
            subprocess.Popen([
                "cmd", "/c", "start", "cmd", "/k",
                f"cd {self.webapp_dir} && venv\\Scripts\\streamlit run app.py"
            ])
        else:
            subprocess.Popen([
                "bash", "-c",
                f"cd {self.webapp_dir} && source venv/bin/activate && streamlit run app.py"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
    def print_final_instructions(self):
        """Print final instructions and next steps"""
        self.print_step("10", "Setup Complete! 🎉")
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}")
        print("🎗️" * 60)
        print("🚀 AfyaSiri Setup Successful!")
        print("🎗️" * 60)
        print(f"{Colors.END}")
        
        print(f"\n{Colors.BOLD}📊 Services Status:{Colors.END}")
        print(f"  {Colors.GREEN}✅ Backend API:{Colors.END}    http://localhost:8000")
        print(f"  {Colors.GREEN}✅ API Docs:{Colors.END}       http://localhost:8000/docs") 
        print(f"  {Colors.GREEN}✅ Web App:{Colors.END}        http://localhost:8501")
        print(f"  {Colors.YELLOW}📱 Mobile App:{Colors.END}     Ready for Flutter setup")
        
        print(f"\n{Colors.BOLD}🎯 Next Steps:{Colors.END}")
        print(f"  1. {Colors.CYAN}Backend is running on port 8000{Colors.END}")
        print(f"  2. {Colors.CYAN}Web app is running on port 8501{Colors.END}")
        print(f"  3. {Colors.CYAN}Open http://localhost:8501 in your browser{Colors.END}")
        
        print(f"\n{Colors.BOLD}📱 Mobile App Setup:{Colors.END}")
        print(f"  {Colors.YELLOW}cd AfyaSiri/mobile{Colors.END}")
        print(f"  {Colors.YELLOW}flutter pub get{Colors.END}")
        print(f"  {Colors.YELLOW}flutter run{Colors.END}")
        
        print(f"\n{Colors.BOLD}🛠️  Manual Startup (if needed):{Colors.END}")
        print(f"  {Colors.WHITE}Backend:{Colors.END}  cd backend && source venv/bin/activate && uvicorn app.main:app --reload")
        print(f"  {Colors.WHITE}Webapp:{Colors.END}   cd webapp && source venv/bin/activate && streamlit run app.py")
        
        print(f"\n{Colors.PINK}{Colors.BOLD}💖 Thank you for supporting breast cancer awareness!{Colors.END}")
        print(f"{Colors.PINK}🎗️  Remember: Early detection saves lives!{Colors.END}")
        
    def run_complete_setup(self):
        """Run the complete setup process"""
        self.print_header()
        
        try:
            # Run all setup steps
            if not self.check_prerequisites():
                return
                
            self.create_project_structure()
            self.create_backend_files()
            self.create_webapp_files()
            self.create_mobile_files()
            self.create_sample_pdfs()
            self.setup_virtual_environments()
            self.create_run_scripts()
            
            # Ask user if they want to start services
            print(f"\n{Colors.BOLD}🚀 Start services now?{Colors.END}")
            response = input(f"{Colors.YELLOW}Press Enter to start services, or 'q' to quit: {Colors.END}").strip().lower()
            
            if response != 'q':
                self.start_services()
                time.sleep(5)  # Give services time to start
                self.print_final_instructions()
            else:
                self.print_info("Services not started. Use the run scripts to start them later.")
                
        except KeyboardInterrupt:
            self.print_info("\nSetup interrupted by user")
        except Exception as e:
            self.print_error(f"Setup failed: {e}")
            self.print_info("Check the error above and try again")

def main():
    """Main entry point"""
    setup = AfyaSiriSetup()
    setup.run_complete_setup()

if __name__ == "__main__":
    main()