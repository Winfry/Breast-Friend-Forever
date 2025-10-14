# chatbot_service.py
import openai
from app.core.config import settings

class ChatbotService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
    async def get_response(self, message: str, conversation_history: list = None) -> str:
        try:
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            if conversation_history:
                messages.extend(conversation_history[-6:])
            
            messages.append({"role": "user", "content": message})
            
            # 🆕 ENABLE WEB SEARCH - This is the key change!
            response = self.client.chat.completions.create(
                model="gpt-4",  # Use GPT-4 for better web search
                messages=messages,
                temperature=settings.CHATBOT_TEMPERATURE,
                max_tokens=settings.MAX_TOKENS,
                # 🎯 THIS ENABLES REAL-TIME WEB ACCESS
                tools=[{
                    "type": "web_search",
                    "web_search": {
                        "search_context_size": "high"
                    }
                }]
            )
            
            ai_response = response.choices[0].message.content
            return self._validate_response(ai_response)
            
        except Exception as e:
            return f"I'm here to help with breast health information! 💖 If you have specific concerns, please consult a healthcare professional. (Error: {str(e)})"