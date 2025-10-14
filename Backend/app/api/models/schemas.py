from pydantic import BaseModel, Field
from typing import Optional, List

# 💬 CHAT MODELS
class ChatMessage(BaseModel):
    """📨 What users send to the chatbot"""
    message: str = Field(..., min_length=1, max_length=1000, description="User's question")
    conversation_id: str = Field(default="anonymous", description="Session ID")

class ChatResponse(BaseModel):
    """📤 What the chatbot sends back"""
    response: str = Field(..., description="AI's answer")
    conversation_id: str = Field(..., description="Session ID")

# 🏥 HOSPITAL MODELS  
class HospitalBase(BaseModel):
    """🏥 Hospital information structure"""
    name: str
    address: str
    city: str
    state: str
    phone: Optional[str] = None
    services: Optional[str] = None

class HospitalResponse(HospitalBase):
    """📊 Hospital data for API responses"""
    id: int

# 💖 ENCOURAGEMENT MODELS
class EncouragementMessage(BaseModel):
    """💌 Support message from users"""
    message: str = Field(..., min_length=5, max_length=500)
    type: str = Field(default="💖 General Support")
    author: str = Field(default="Anonymous Friend")

class EncouragementResponse(EncouragementMessage):
    """📨 Support message with ID and timestamp"""
    id: int
    timestamp: str