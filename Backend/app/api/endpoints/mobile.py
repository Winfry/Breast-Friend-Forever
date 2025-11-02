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

class HospitalSearch(BaseModel):
    county: Optional[str] = None
    service: Optional[str] = None
    name: Optional[str] = None

# Sample Data
HEALTH_TIPS = [
    "Perform breast self-exams monthly 5-7 days after your period starts",
    "Maintain a healthy weight and exercise 30 minutes daily", 
    "Know your family history of breast and ovarian cancer",
    "Women 40+ should get mammograms yearly",
    "Limit alcohol to 1 drink per day and avoid smoking",
    "Breastfeed if possible - it reduces breast cancer risk",
    "Eat more fruits, vegetables and whole grains",
    "Wear comfortable, supportive bras during exercise"
]

HOSPITAL_FACILITIES = [
    {
        "name": "Nairobi Women's Hospital",
        "county": "Nairobi",
        "phone": "+254 20 272 6000",
        "services": ["Mammography", "Ultrasound", "Consultation", "Screening", "Biopsy"],
        "hours": "24/7",
        "emergency": True
    },
    {
        "name": "Aga Khan University Hospital", 
        "county": "Nairobi",
        "phone": "+254 20 366 2000",
        "services": ["Mammography", "Screening", "Consultation", "Oncology", "Surgery"],
        "hours": "24/7",
        "emergency": True
    },
    {
        "name": "Mombasa Hospital",
        "county": "Mombasa", 
        "phone": "+254 41 222 1600",
        "services": ["Consultation", "Ultrasound", "Basic Screening", "Lab Services"],
        "hours": "6:00 AM - 10:00 PM",
        "emergency": True
    },
    {
        "name": "Kisumu Medical Center",
        "county": "Kisumu",
        "phone": "+254 57 202 4174", 
        "services": ["Consultation", "Screening", "Referral Services"],
        "hours": "8:00 AM - 8:00 PM",
        "emergency": False
    }
]

SYMPTOM_GUIDE = {
    "lump": "Most breast lumps are not cancer, but any new lump should be checked by a doctor",
    "pain": "Breast pain is common and usually not cancer-related, but persistent pain should be evaluated",
    "discharge": "Nipple discharge can have various causes - see a doctor if it's bloody or from one breast only",
    "skin_changes": "Redness, dimpling, or puckering of breast skin should be examined promptly"
}

# Enhanced Chat Endpoint
@router.post("/chat")
async def mobile_chat(request: ChatRequest):
    """Enhanced chat with symptom detection and contextual responses"""
    
    message_lower = request.message.lower()
    response = ""
    suggestions = []
    
    # Symptom detection
    if any(word in message_lower for word in ['lump', 'bump', 'mass']):
        response = SYMPTOM_GUIDE["lump"] + " I can help you find a healthcare provider for evaluation. 🏥"
        suggestions = ["Find hospitals", "Self-exam steps", "When to see doctor"]
    
    elif any(word in message_lower for word in ['pain', 'hurt', 'sore', 'ache']):
        response = SYMPTOM_GUIDE["pain"] + " Tracking your symptoms can help your doctor. 📝"
        suggestions = ["Symptom tracker", "Pain management", "Find clinics"]
    
    elif any(word in message_lower for word in ['discharge', 'leak', 'nipple']):
        response = SYMPTOM_GUIDE["discharge"] + " Schedule an appointment for proper diagnosis. 🩺"
        suggestions = ["Hospital search", "Prepare for appointment", "Questions to ask doctor"]
    
    elif any(word in message_lower for word in ['red', 'dimple', 'orange', 'skin']):
        response = SYMPTOM_GUIDE["skin_changes"] + " This requires prompt medical attention. ⚠️"
        suggestions = ["Emergency contacts", "Find specialists", "Document changes"]
    
    elif any(word in message_lower for word in ['prevent', 'healthy', 'diet', 'exercise']):
        response = "Great focus on prevention! Regular screenings, healthy lifestyle, and awareness are your best defenses. 🌱"
        suggestions = ["Health tips", "Exercise guide", "Nutrition advice", "Risk factors"]
    
    elif any(word in message_lower for word in ['hospital', 'clinic', 'doctor', 'appointment']):
        response = "I can help you find healthcare facilities! Use the hospital search to filter by location and services. 🗺️"
        suggestions = ["Search hospitals", "Emergency contacts", "Prepare for visit"]
    
    else:
        response = "Thanks for reaching out about breast health! I'm here to provide information, support, and resources. How can I help you today? 💖"
        suggestions = ["Self-exam guide", "Hospital search", "Health tips", "Symptom check"]
    
    return {
        "response": response,
        "suggestions": suggestions,
        "timestamp": datetime.utcnow().isoformat(),
        "quick_actions": ["Find hospitals", "Health tips", "Self-exam", "Emergency"]
    }

# Enhanced Hospital Search
@router.post("/hospitals/search")
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
            detail="No hospitals found matching your criteria. Try broadening your search."
        )
    
    return {
        "facilities": filtered_facilities,
        "count": len(filtered_facilities),
        "search_filters": search.dict()
    }

@router.get("/hospitals/counties")
async def get_available_counties():
    """Get list of counties with available hospitals"""
    counties = list(set(hospital["county"] for hospital in HOSPITAL_FACILITIES))
    return {"counties": sorted(counties)}

@router.get("/hospitals/services")
async def get_available_services():
    """Get list of all available medical services"""
    all_services = set()
    for hospital in HOSPITAL_FACILITIES:
        all_services.update(hospital["services"])
    return {"services": sorted(list(all_services))}

# Enhanced Health Tips
@router.get("/health-tips")
async def get_health_tips(count: int = 1, category: Optional[str] = None):
    """Get random health tips with quantity control"""
    if count > len(HEALTH_TIPS) or count < 1:
        raise HTTPException(
            status_code=400, 
            detail=f"Please request between 1 and {len(HEALTH_TIPS)} tips"
        )
    
    selected_tips = random.sample(HEALTH_TIPS, min(count, len(HEALTH_TIPS)))
    
    return {
        "tips": selected_tips,
        "total_available": len(HEALTH_TIPS),
        "category": "Breast Health Awareness",
        "frequency": "Check daily for new tips!"
    }

@router.get("/health-tips/daily")
async def daily_health_tip():
    """Get one consistent daily tip (based on date)"""
    today = datetime.now().day
    tip_index = today % len(HEALTH_TIPS)
    return {
        "tip": HEALTH_TIPS[tip_index],
        "is_daily_tip": True,
        "date": datetime.now().date().isoformat()
    }

# Emergency Features
@router.get("/emergency/contacts")
async def emergency_contacts():
    """Get emergency contact information"""
    return {
        "emergency_contacts": [
            {"service": "National Cancer Helpline", "phone": "0800 221 212", "hours": "24/7"},
            {"service": "Emergency Services", "phone": "999", "hours": "24/7"},
            {"service": "Medical Ambulance", "phone": "0700 395 395", "hours": "24/7"},
            {"service": "Mental Health Support", "phone": "0800 723 725", "hours": "24/7"}
        ],
        "message": "In case of emergency, contact healthcare professionals immediately. For life-threatening situations, call 999."
    }

# Self-Exam Guide
@router.get("/self-exam/guide")
async def self_exam_guide():
    """Step-by-step self-examination guide"""
    return {
        "title": "Breast Self-Examination Guide",
        "frequency": "Monthly, 5-7 days after your period starts",
        "steps": [
            {
                "step": 1,
                "title": "Visual Inspection",
                "description": "Stand before a mirror with shoulders straight and arms on hips. Look for any changes in size, shape, color, or visible distortion.",
                "duration": "1-2 minutes"
            },
            {
                "step": 2, 
                "title": "Arm Raise Check",
                "description": "Raise arms and look for the same changes. Check for any fluid coming from nipples.",
                "duration": "1 minute"
            },
            {
                "step": 3,
                "title": "Lying Down Exam", 
                "description": "While lying down, feel breasts using a firm, smooth touch with the first few finger pads.",
                "duration": "3-5 minutes per breast"
            },
            {
                "step": 4,
                "title": "Pattern Coverage",
                "description": "Follow a pattern (circular, vertical, or wedge) to cover entire breast and armpit area.",
                "duration": "2-3 minutes per breast"
            },
            {
                "step": 5,
                "title": "Repeat Standing", 
                "description": "Repeat examination while standing or sitting. Many women find this easiest in the shower.",
                "duration": "2-3 minutes per breast"
            }
        ],
        "when_to_consult": [
            "New lump or hard knot",
            "Swelling, warmth, or redness",
            "Nipple discharge (especially bloody)",
            "Skin dimpling or puckering",
            "Persistent breast pain"
        ],
        "reminder": "Regular self-exams help you become familiar with how your breasts normally look and feel."
    }

@router.get("/self-exam/reminder")
async def set_exam_reminder():
    """Get reminder settings for self-exams"""
    return {
        "recommended_frequency": "monthly",
        "best_time": "5-7 days after period starts",
        "reminder_options": ["push", "email", "sms"],
        "next_recommended_date": "Calculate based on user's cycle"
    }

# Risk Assessment (Basic)
@router.get("/risk-assessment/questions")
async def risk_assessment_questions():
    """Basic risk assessment questions"""
    return {
        "questions": [
            {
                "id": 1,
                "question": "Do you have a mother, sister, or daughter who had breast cancer?",
                "category": "family_history"
            },
            {
                "id": 2, 
                "question": "What is your current age?",
                "category": "age"
            },
            {
                "id": 3,
                "question": "Have you ever had children?",
                "category": "reproductive_history" 
            },
            {
                "id": 4,
                "question": "Do you drink alcohol regularly?",
                "category": "lifestyle"
            }
        ],
        "disclaimer": "This is a basic assessment. Consult healthcare providers for comprehensive evaluation."
    }