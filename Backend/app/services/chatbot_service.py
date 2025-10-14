import openai
from app.core.config import settings

class ChatbotService:
    """🧠 AI service for breast health conversations"""
    
    def __init__(self):
        # 🔑 Initialize OpenAI with API key from config
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # 🎭 Define the chatbot's personality and knowledge
        self.system_prompt = """
        You are "Breast Friend Forever" - a compassionate, knowledgeable breast health assistant.

        YOUR ROLE:
        - Provide accurate, evidence-based information about breast health
        - Guide users through self-examination techniques  
        - Offer emotional support and encouragement
        - Share information about screening and prevention
        - Connect users to resources when needed

        YOUR PERSONALITY:
        - Warm, empathetic, and understanding
        - Professional but approachable  
        - Gentle humor when appropriate
        - Always supportive and non-judgmental

        IMPORTANT RULES:
        - NEVER provide medical diagnoses
        - ALWAYS encourage consulting healthcare professionals
        - Be clear about limitations: "I'm an AI assistant, not a doctor"
        - Focus on education and awareness, not treatment advice
        - Maintain user privacy and anonymity

        RESPONSE STYLE:
        - Use simple, clear language
        - Include emojis occasionally for warmth 💖
        - Break complex information into digestible parts
        - Always end with encouragement or next steps
        """
    
    async def get_response(self, message: str, conversation_history: list = None) -> str:
        """💬 Get AI response for user message"""
        try:
            # 📝 Prepare messages for OpenAI
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # 🕒 Add conversation history for context
            if conversation_history:
                messages.extend(conversation_history[-6:])  # Last 6 messages
            
            # ➕ Add current user message
            messages.append({"role": "user", "content": message})
            
            # 🚀 Call OpenAI API
            response = self.client.chat.completions.create(
                model=settings.CHATBOT_MODEL,
                messages=messages,
                temperature=settings.CHATBOT_TEMPERATURE,
                max_tokens=settings.MAX_TOKENS
            )
            
            ai_response = response.choices[0].message.content
            
            # ✅ Ensure response is safe and appropriate
            return self._validate_response(ai_response)
            
        except Exception as e:
            # 🆘 Fallback if API fails
            print(f"❌ OpenAI API error: {e}")
            return "I'm here to help with breast health information! 💖 If you have specific concerns, please consult a healthcare professional. You can ask about self-examination, symptoms, or screening guidelines."
    
    def _validate_response(self, response: str) -> str:
        """🛡️ Ensure AI response is appropriate and safe"""
        response_lower = response.lower()
        
        # ⚠️ Add disclaimer if response sounds diagnostic
        diagnostic_terms = ["you have", "you've got", "diagnosis", "you should take", "treatment"]
        if any(term in response_lower for term in diagnostic_terms):
            response += "\n\n💡 Remember: I'm an AI assistant for education, not a doctor. Please consult healthcare professionals for medical advice."
        
        return response
    
    async def get_greeting(self) -> dict:
        """👋 Get initial greeting and suggested questions"""
        return {
            "message": "Hello! I'm your Breast Friend Forever companion. 🌸 I'm here to provide caring, accurate information about breast health in a safe, supportive space. What would you like to know today?",
            "suggested_questions": [
                "How do I perform a breast self-exam?",
                "What are common breast health concerns?",
                "When should I get screened?",
                "What lifestyle supports breast health?",
                "Can you explain different screening methods?"
            ]
        }

# 🎯 Create global instance
chatbot_service = ChatbotService()