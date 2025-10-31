from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import random

router = APIRouter()

class MobileChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def mobile_chat(request: MobileChatRequest):
    return {
        "response": f"I understand you're asking about: '{request.message}'. I'm here to help with breast health information! 💖",
        "suggestions": ["Self-exam guide", "Hospital search", "Risk factors"]
    }

@router.get("/hospitals")
async def mobile_hospitals():
    return {
        "hospitals": [
            {"name": "Nairobi Women's Hospital", "phone": "+254 20 272 6000"},
            {"name": "Aga Khan Hospital", "phone": "+254 20 366 2000"}
        ]
    }