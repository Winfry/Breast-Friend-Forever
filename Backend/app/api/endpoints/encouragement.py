from fastapi import APIRouter, HTTPException
from app.services.data_service import data_service
from app.api.models.schemas import EncouragementMessage, EncouragementResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[EncouragementResponse])
async def get_encouragements():
    try:
        messages = await data_service.load_encouragement()
        messages.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error loading messages")