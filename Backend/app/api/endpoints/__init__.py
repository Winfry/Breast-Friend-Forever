# backend/app/api/endpoints/__init__.py
# Now serving BOTH frontends with same endpoints

# backend/app/api/endpoints/self_exam.py
@router.get("/steps")
async def get_self_exam_steps():
    return {
        "steps": [
            {
                "id": 1,
                "title": "Visual Inspection", 
                "description": "Stand in front of a mirror...",
                "icon": "👀",
                "tip": "Look for dimpling or puckering"
            },
            # ... same steps for both apps
        ]
    }

# backend/app/api/endpoints/chatbot.py  
@router.post("/message")
async def chat_message(message: ChatRequest):
    # Same AI response for both apps
    return await chatbot_service.get_response(message)

# backend/app/api/endpoints/hospitals.py
@router.get("/")
async def get_hospitals(city: str = None, state: str = None):
    # Same hospital data for both
    return await data_service.get_hospitals(city, state)