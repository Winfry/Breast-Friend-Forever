from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# 💬 Chat Models
class ChatMessage(BaseModel):
    """Schema for sending chat messages"""
    message: str = Field(..., min_length=1, max_length=1000, description="User message")
    conversation_id: str = Field(default="anonymous", description="Anonymous session ID")

class ChatResponse(BaseModel):
    """Schema for chatbot responses"""
    response: str = Field(..., description="AI response message")
    conversation_id: str = Field(..., description="Session identifier")

# 🏥 Hospital Models
class HospitalBase(BaseModel):
    """Base schema for hospital data"""
    name: str
    address: str
    city: str
    state: str
    phone: Optional[str] = None
    services: Optional[str] = None

class HospitalResponse(HospitalBase):
    """Schema for hospital API responses"""
    id: int
    
    class Config:
        from_attributes = True

# 📚 Resource Models
class ArticleBase(BaseModel):
    """Schema for educational articles"""
    title: str
    description: str
    content: str
    category: str
    reading_time: str
    author: Optional[str] = "Breast Health Team"

class ArticleResponse(ArticleBase):
    """Schema for article API responses"""
    id: int
    last_updated: str
    
    class Config:
        from_attributes = True

class PDFResource(BaseModel):
    """Schema for PDF resources"""
    id: int
    title: str
    description: str
    filename: str
    file_size: str
    pages: int
    category: str

# 💕 Encouragement Models
class EncouragementMessage(BaseModel):
    """Schema for encouragement wall messages"""
    message: str = Field(..., min_length=5, max_length=500, description="Message content")
    type: str = Field(default="💖 General Support", description="Message category")
    author: str = Field(default="Anonymous Friend", description="Always anonymous")

class EncouragementResponse(EncouragementMessage):
    """Schema for encouragement API responses"""
    id: int
    timestamp: str
    
    class Config:
        from_attributes = True