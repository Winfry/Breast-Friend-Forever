from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import random
from datetime import datetime

router = APIRouter()

# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    suggestions: List[str]
    timestamp: str

class HospitalSearch(BaseModel):
    county: Optional[str] = None
    service: Optional[str] = None
    name: Optional[str] = None

class HospitalResponse(BaseModel):
    name: str
    county: str
    phone: str
    services: List[str]
    distance: Optional[str] = None

# Sample Data
HEALTH_TIPS = [
    "Perform breast self-exams monthly after your period ends",
    "Maintain a healthy weight and exercise regularly", 
    "Know your family history of breast cancer",
    "Attend regular clinical exams as recommended",
    "Limit alcohol consumption and avoid smoking",
    "Breastfeed if possible to reduce cancer risk"
]

HOSPITAL_FACILITIES = [
    {
        "name": "Nairobi Women's Hospital",
        "county": "Nairobi",
        "phone": "+254 20 272 6000",
        "services": ["Mammography", "Ultrasound", "Consultation", "Screening"],
        "distance": "5km"
    },
    {
        "name": "Aga Khan Hospital", 
        "county": "Nairobi",
        "phone": "+254 20 366 2000",
        "services": ["Mammography", "Screening", "Consultation", "Biopsy"],
        "distance": "7km"
    },
    {
        "name": "Mombasa Hospital",
        "county": "Mombasa", 
        "phone": "+254 41 222 1600",
        "services": ["Consultation", "Ultrasound", "Basic Screening"],
        "distance": "2km"
    }
]

# Enhanced Chat Endpoint
@router.post("/chat", response_model=ChatResponse)
async def mobile_chat(request: ChatRequest):
    """Enhanced chat endpoint with contextual responses"""
    
    # Simple intent detection
    message_lower = request.message.lower()
    
    if any(word in message_lower for word in ['symptom', 'pain', 'lump', 'hurt']):
        response = "I understand you're mentioning symptoms. It's important to consult a healthcare professional for proper evaluation. Would you like me to help find nearby hospitals? 🏥"
        suggestions = ["Find hospitals", "Self-exam guide", "Emergency contacts"]
    
    elif any(word in message_lower for word in ['hospital', 'clinic', 'doctor']):
        response = "I can help you find healthcare facilities! Try using our hospital search feature to find locations near you. 🗺️"
        suggestions = ["Hospital search", "Contact information", "Services offered"]
    
    elif any(word in message_lower for word in ['prevent', 'healthy', 'exercise', 'diet']):
        response = "Great focus on prevention! Regular self-exams, healthy lifestyle, and screenings are key to breast health. 🌱"
        suggestions = ["Health tips", "Self-exam guide", "Risk factors"]
    
    else:
        response = f"Thanks for your question about breast health! I'm here to provide helpful information and support. 💖"
        suggestions = ["Self-exam guide", "Hospital search", "Health tips", "Risk factors"]
    
    return ChatResponse(
        response=response,
        suggestions=suggestions,
        timestamp=datetime.utcnow().isoformat()
    )

# Enhanced Hospital Search
@router.post("/hospitals", response_model=List[HospitalResponse])
async def search_hospitals(search: HospitalSearch):
    """Advanced hospital search with multiple filters"""
    
    filtered_facilities = HOSPITAL_FACILITIES.copy()
    
    # Apply filters
    if search.county:
        filtered_facilities = [f for f in filtered_facilities 
                             if search.county.lower() in f["county"].lower()]
    
    if search.service and search.service != "any":
        filtered_facilities = [f for f in filtered_facilities 
                             if any(search.service.lower() in s.lower() 
                                  for s in f["services"])]
    
    if search.name:
        filtered_facilities = [f for f in filtered_facilities 
                             if search.name.lower() in f["name"].lower()]
    
    if not filtered_facilities:
        raise HTTPException(
            status_code=404, 
            detail="No hospitals found matching your criteria"
        )
    
    return filtered_facilities

@router.get("/hospitals", response_model=List[HospitalResponse])
async def get_all_hospitals():
    """Get all available hospitals"""
    return HOSPITAL_FACILITIES

# Enhanced Health Tips
@router.get("/health-tips")
async def get_health_tips(count: Optional[int] = 1):
    """Get random health tips with quantity control"""
    if count > len(HEALTH_TIPS):
        raise HTTPException(
            status_code=400, 
            detail=f"Maximum {len(HEALTH_TIPS)} tips available"
        )
    
    selected_tips = random.sample(HEALTH_TIPS, min(count, len(HEALTH_TIPS)))
    return {
        "tips": selected_tips,
        "total_available": len(HEALTH_TIPS),
        "category": "Breast Health Awareness"
    }

# New Emergency Feature
@router.get("/emergency-contacts")
async def emergency_contacts():
    """Get emergency contact information"""
    return {
        "emergency_contacts": [
            {"service": "National Cancer Hotline", "phone": "0800 221 212"},
            {"service": "Emergency Services", "phone": "999"},
            {"service": "Medical Ambulance", "phone": "0700 395 395"}
        ],
        "message": "In case of emergency, contact healthcare professionals immediately"
    }

# New Self-Exam Guide
@router.get("/self-exam-guide")
async def self_exam_guide():
    """Step-by-step self-examination guide"""
    return {
        "title": "Breast Self-Examination Guide",
        "steps": [
            "Stand before a mirror with shoulders straight and arms on hips",
            "Look for any changes in size, shape, color, or visible distortion",
            "Raise arms and look for the same changes",
            "While lying down, feel breasts using a firm, smooth touch",
            "Follow a pattern to cover entire breast and armpit area",
            "Repeat examination while standing or sitting"
        ],
        "frequency": "Monthly, after menstrual period ends",
        "when_to_consult": "If you notice lumps, pain, discharge, or skin changes"
    }