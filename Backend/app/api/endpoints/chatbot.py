from fastapi import APIRouter, HTTPException
from app.services.chatbot_service import chatbot_service
from app.api.models.schemas import ChatMessage, ChatResponse

router = APIRouter()

@router.post("/message", response_model=ChatResponse)
async def chat_message(chat_data: ChatMessage):
    """
    Send a message to the breast health chatbot
    - **message**: User's question or message
    - **conversation_id**: Anonymous session ID (optional)
    """
    try:
        response_text = await chatbot_service.get_response(
            chat_data.message, 
            conversation_history=[]  # In production, store/retrieve history
        )
        
        return ChatResponse(
            response=response_text,
            conversation_id=chat_data.conversation_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="Sorry, I'm having trouble responding. Please try again. 💖"
        )

@router.get("/greeting")
async def get_greeting():
    """Get the initial chatbot greeting and suggested questions"""
    try:
        return await chatbot_service.get_greeting()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error loading greeting")