"""
🤖 AGENTIC CHATBOT ENDPOINT
===========================

This endpoint uses the Agentic RAG system to provide intelligent,
context-aware responses about breast cancer.

FEATURES:
- Intelligent routing (RAG search, web search, or direct answer)
- Multi-step reasoning and verification
- Conversation memory
- Source citations
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import time

router = APIRouter()

# ============================================================================
# LAZY LOADING: Import agentic RAG only when needed
# ============================================================================
"""
Why lazy loading?
- sentence_transformers has heavy dependencies (TensorFlow, Keras)
- Loading it at server startup slows down the server
- We only load it when someone actually uses the agentic endpoint
"""

def get_agentic_rag_function():
    """Lazy load the agentic RAG query function"""
    try:
        from app.agentic_rag import query_agentic_rag
        return query_agentic_rag
    except Exception as e:
        print(f"❌ Error loading agentic RAG: {e}")
        return None


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class AgenticChatRequest(BaseModel):
    """
    Request model for agentic chat.

    Fields:
    - message: The user's question
    - conversation_id: Optional ID to track conversation history (for memory)
    """
    message: str
    conversation_id: Optional[str] = "default"


class AgenticChatResponse(BaseModel):
    """
    Response model for agentic chat.

    Fields:
    - response: The AI's answer
    - sources: List of sources used
    - confidence: How confident the AI is (0.0 to 1.0)
    - tool_used: Which tool was used (rag_search, web_search, direct_answer)
    - query_type: Type of query (medical, recent_info, general)
    - processing_time: How long it took to generate the response
    """
    response: str
    sources: list
    confidence: float
    tool_used: str
    query_type: str
    processing_time: float


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/agentic/message", response_model=AgenticChatResponse)
async def agentic_chat_message(request: AgenticChatRequest):
    """
    🤖 AGENTIC CHAT ENDPOINT

    This endpoint processes user messages using the Agentic RAG system.

    FLOW:
    1. User sends a question
    2. Agent analyzes the question type
    3. Agent routes to appropriate tool (RAG, web search, or direct answer)
    4. Agent verifies the answer quality
    5. Agent synthesizes the final response

    Example usage:
    ```
    POST /api/chatbot/agentic/message
    {
        "message": "What are the early signs of breast cancer?",
        "conversation_id": "user123_session1"
    }
    ```

    Returns:
    ```
    {
        "response": "Early signs include...",
        "sources": ["Medical PDF Database"],
        "confidence": 0.85,
        "tool_used": "rag_search",
        "query_type": "medical",
        "processing_time": 2.3
    }
    ```
    """
    start_time = time.time()

    try:
        print(f"\n{'='*60}")
        print(f"📨 NEW AGENTIC CHAT REQUEST")
        print(f"Message: {request.message}")
        print(f"Conversation ID: {request.conversation_id}")
        print(f"{'='*60}\n")

        # Lazy load the agentic RAG function
        query_agentic_rag = get_agentic_rag_function()
        if query_agentic_rag is None:
            raise Exception("Agentic RAG system failed to load")

        # Query the agentic RAG system
        result = query_agentic_rag(
            user_question=request.message,
            conversation_id=request.conversation_id
        )

        # Calculate processing time
        processing_time = time.time() - start_time

        print(f"\n{'='*60}")
        print(f"✅ RESPONSE GENERATED")
        print(f"Tool used: {result['tool_used']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Processing time: {processing_time:.2f}s")
        print(f"{'='*60}\n")

        return AgenticChatResponse(
            response=result['answer'],
            sources=result['sources'],
            confidence=result['confidence'],
            tool_used=result['tool_used'],
            query_type=result['query_type'],
            processing_time=processing_time
        )

    except Exception as e:
        print(f"\n❌ ERROR in agentic chat: {repr(e)}")
        import traceback
        traceback.print_exc()

        # Return a graceful fallback response
        return AgenticChatResponse(
            response="I apologize, but I encountered an error processing your question. Please try rephrasing your question or ask about breast cancer symptoms, screening, or prevention.",
            sources=[],
            confidence=0.0,
            tool_used="error",
            query_type="error",
            processing_time=time.time() - start_time
        )


@router.get("/agentic/health")
async def agentic_health():
    """
    Health check endpoint for the agentic chatbot.

    Returns:
    - status: "healthy" if the service is running
    - service: "agentic_chatbot"
    - features: List of features available
    """
    return {
        "status": "healthy",
        "service": "agentic_chatbot",
        "features": [
            "Intelligent routing",
            "Multi-step reasoning",
            "RAG search",
            "Web search",
            "Direct answers",
            "Conversation memory",
            "Source verification"
        ],
        "version": "1.0.0"
    }


@router.get("/agentic/info")
async def agentic_info():
    """
    Get information about the agentic RAG system.

    Returns details about:
    - How the agent works
    - What tools are available
    - When to use which tool
    """
    return {
        "description": "Agentic RAG system for breast cancer information",
        "how_it_works": {
            "step_1": "Router analyzes the user's question",
            "step_2": "Agent decides which tool to use based on question type",
            "step_3": "Tool executes and returns results",
            "step_4": "Verification checks if answer is sufficient",
            "step_5": "Synthesizer creates final, well-formatted response"
        },
        "tools": {
            "rag_search": {
                "description": "Searches medical PDF knowledge base",
                "use_when": "Question is about breast cancer symptoms, prevention, screening",
                "sources": "10 medical PDF documents"
            },
            "web_search": {
                "description": "Searches the web for current information",
                "use_when": "Question asks for recent/latest information (2023+)",
                "sources": "DuckDuckGo search results"
            },
            "direct_answer": {
                "description": "Answers using AI's general knowledge",
                "use_when": "Question is conversational or doesn't need specific facts",
                "sources": "AI knowledge"
            }
        },
        "example_queries": {
            "medical": "What are the early signs of breast cancer?",
            "recent": "What's the latest breast cancer research in 2024?",
            "general": "Hello, how can you help me?"
        }
    }
