# BACKEND/app/services/chatbot_service.py
import openai
from app.core.config import settings

class ChatbotService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Enhanced system prompt for web search
        self.system_prompt = """
        You are "Breast Friend Forever" - a compassionate breast health assistant with REAL-TIME web access.
        
        IMPORTANT CAPABILITIES:
        - You can search the web for latest breast health information
        - You have access to current medical guidelines and research
        - You can provide up-to-date statistics and treatment information
        
        When users ask about:
        - Latest research/studies → USE WEB SEARCH
        - Current statistics → USE WEB SEARCH
        - Recent guidelines → USE WEB SEARCH  
        - New treatments → USE WEB SEARCH
        - Time-sensitive info → USE WEB SEARCH
        
        For general education (self-exams, basic info), use your knowledge.
        
        ALWAYS:
        - Be compassionate and supportive
        - Encourage professional medical consultation
        - Provide evidence-based information
        - Stay current with latest medical knowledge
        """
    
    async def get_response(self, message: str, conversation_history: list = None) -> str:
        """Get AI response with web search capability"""
        try:
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            if conversation_history:
                messages.extend(conversation_history[-6:])
            
            messages.append({"role": "user", "content": message})
            
            # 🎯 ENABLE WEB SEARCH - Simple and effective!
            response = self.client.chat.completions.create(
                model="gpt-4",  # Use GPT-4 for web search capability
                messages=messages,
                temperature=settings.CHATBOT_TEMPERATURE,
                max_tokens=settings.MAX_TOKENS,
                # 🔍 THIS ENABLES BUILT-IN WEB SEARCH
                tools=[{
                    "type": "web_search_preview",
                    "web_search_preview": {
                        "search_context_size": "high"
                    }
                }]
            )
            
            ai_response = response.choices[0].message.content
            return self._validate_response(ai_response)
            
        except Exception as e:
            print(f"Chatbot error: {e}")
            return "I'm here to help with breast health information! 💖 For the most current information, please consult healthcare professionals or trusted medical websites."
    
    def _validate_response(self, response: str) -> str:
        """Ensure AI response is appropriate and safe"""
        response_lower = response.lower()
        
        # Add disclaimer if response sounds diagnostic
        diagnostic_terms = ["you have", "you've got", "diagnosis", "you should take", "treatment"]
        if any(term in response_lower for term in diagnostic_terms):
            response += "\n\n💡 Remember: I'm an AI assistant for education, not a doctor. Please consult healthcare professionals for medical advice."
        
        return response

# Create global instance
chatbot_service = ChatbotService()