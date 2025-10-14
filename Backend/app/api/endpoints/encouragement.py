from fastapi import APIRouter, HTTPException
from app.services.data_service import data_service
from app.api.models.schemas import EncouragementMessage, EncouragementResponse
from typing import List
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[EncouragementResponse])
async def get_encouragements():
    """💖 Get all encouragement wall messages"""
    try:
        messages = await data_service.load_encouragement()
        # Sort by timestamp (newest first)
        messages.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error loading messages")

@router.post("/", response_model=EncouragementResponse)
async def create_encouragement(message_data: EncouragementMessage):
    """✍️ Post a new encouragement message (always anonymous)"""
    try:
        # Load existing messages
        messages = await data_service.load_encouragement()
        
        # Create new message with ID and timestamp
        new_id = max([msg.get('id', 0) for msg in messages], default=0) + 1
        new_message = {
            "id": new_id,
            "message": message_data.message,
            "type": message_data.type,
            "author": "Anonymous Friend",  # Always anonymous
            "timestamp": datetime.now().isoformat()
        }
        
        # Add to list and save
        messages.append(new_message)
        success = await data_service.save_encouragement(messages)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save message")
        
        return new_message
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error creating message")