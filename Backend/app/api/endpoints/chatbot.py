from fastapi import APIRouter, HTTPException
from app.services.chatbot_service import chatbot_service
from app.api.models.schemas import ChatMessage, ChatResponse

router = APIRouter()

@router.post("/message", response_model=ChatResponse)
async def chat_message(chat_data: ChatMessage):
    try:
        response_text = await chatbot_service.get_response(chat_data.message)
        return ChatResponse(
            response=response_text,
            conversation_id=chat_data.conversation_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Sorry, I'm having trouble responding. Please try again. 💖")

@router.get("/greeting")
async def get_greeting():
    try:
        return await chatbot_service.get_greeting()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error loading greeting")