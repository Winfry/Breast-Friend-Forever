"""
🤖 AGENTIC RAG SYSTEM FOR BREAST CANCER CHATBOT
================================================

This module implements an Agentic RAG (Retrieval-Augmented Generation) system
that intelligently routes queries to different tools based on the question type.

ARCHITECTURE OVERVIEW:
---------------------
1. STATE: Tracks conversation history, tool results, and decisions
2. TOOLS: Functions the agent can call (RAG search, web search, direct answer)
3. NODES: Processing steps in the workflow
4. ROUTER: Decision-maker that chooses which tool to use
5. GRAPH: The complete workflow connecting all pieces

WHY AGENTIC vs REGULAR RAG:
--------------------------
Regular RAG: Always searches PDFs → Generate answer (dumb, one-size-fits-all)
Agentic RAG: Analyzes question → Chooses best tool → Verifies → Answer (smart, adaptive)

EXAMPLE FLOW:
------------
User: "What are breast cancer symptoms?"
  → Router: "Medical question, use RAG search"
  → RAG Tool: Searches PDFs, finds relevant info
  → Verification: Checks if answer is sufficient
  → Synthesize: Creates final answer with sources

User: "What's the latest breast cancer research in 2024?"
  → Router: "Recent info needed, PDFs are old, use web search"
  → Web Tool: Searches DuckDuckGo for current research
  → Synthesize: Creates answer with disclaimer about sources
"""

import os
from typing import TypedDict, Annotated, Literal
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
import operator

# Import our existing services
from app.rag_system import BreastCancerRAG
from app.services.web_search_service import WebSearchService


# ============================================================================
# STEP 1: DEFINE THE STATE (What the agent remembers)
# ============================================================================
"""
STATE EXPLANATION:
The State is like the agent's "working memory". It tracks:
- messages: Full conversation history (user questions + AI responses)
- tool_results: What each tool returned
- current_step: Where we are in the workflow
- confidence: How confident we are in the answer
- sources: Where the information came from
"""

class AgentState(TypedDict):
    """
    The state that flows through our LangGraph workflow.
    Each node can read from and write to this state.
    """
    messages: Annotated[list, operator.add]  # Conversation history (grows over time)
    tool_results: dict  # What tools have returned
    current_step: str  # Current node in the graph
    confidence: float  # How confident we are (0.0 to 1.0)
    sources: list  # Source documents/URLs used
    query_type: str  # What kind of question this is (medical, general, recent)


# ============================================================================
# STEP 2: DEFINE THE TOOLS (What the agent can do)
# ============================================================================
"""
TOOLS EXPLANATION:
Tools are functions the agent can call. Think of them as specialized helpers:
- RAG Search Tool: Expert at searching medical PDFs
- Web Search Tool: Expert at finding recent online information
- Direct Answer Tool: Uses agent's own knowledge for simple questions

Each tool is decorated with @tool which tells LangGraph:
1. What the tool does (description)
2. What inputs it needs
3. How to call it
"""

# Initialize our existing RAG system and web search
rag_system = BreastCancerRAG()
web_searcher = WebSearchService()


@tool
def rag_search_tool(query: str) -> dict:
    """
    Search medical PDF knowledge base for breast cancer information.

    USE THIS WHEN:
    - Question is about breast cancer symptoms, prevention, screening
    - Question is medical/educational in nature
    - Information is likely in medical documents

    Args:
        query: The user's question about breast cancer

    Returns:
        dict with 'answer', 'sources', and 'confidence' score
    """
    print(f"🔍 RAG TOOL: Searching PDFs for: {query}")

    # Load PDFs if not already loaded
    if not rag_system.knowledge_base:
        print("   📚 Loading PDFs for the first time...")
        rag_system.load_all_pdfs()

    # Use existing RAG system - search for relevant chunks
    chunks = rag_system.search(query, top_k=5)

    # Generate answer from chunks
    answer = rag_system.get_answer(query, chunks)

    # Extract confidence from similarity scores
    confidence = 0.0
    if chunks:
        # Average similarity of top chunks
        similarities = [chunk['similarity'] for chunk in chunks]
        confidence = float(sum(similarities) / len(similarities))

    # Extract unique sources
    sources = list(set([chunk['source'] for chunk in chunks])) if chunks else []

    return {
        "answer": answer,
        "sources": sources if sources else ["Medical PDF Database"],
        "confidence": confidence,
        "tool_used": "rag_search"
    }


@tool
def web_search_tool(query: str) -> dict:
    """
    Search the web for current breast cancer information.

    USE THIS WHEN:
    - Question asks about recent/current information (2023+)
    - Question is about latest research, statistics, or news
    - RAG search returned low confidence results

    Args:
        query: The search query

    Returns:
        dict with 'answer', 'sources', and 'confidence' score
    """
    print(f"🌐 WEB TOOL: Searching web for: {query}")

    # Use existing web search service
    results = web_searcher.search(query, max_results=3)

    # Format results
    if results:
        answer = "\n\n".join([
            f"**{r['title']}**\n{r['snippet']}\nSource: {r['link']}"
            for r in results
        ])
        sources = [r['link'] for r in results]
        confidence = 0.7  # Web results are generally relevant but need verification
    else:
        answer = "No recent web information found."
        sources = []
        confidence = 0.0

    return {
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
        "tool_used": "web_search"
    }


@tool
def direct_answer_tool(query: str) -> dict:
    """
    Answer general questions using the LLM's own knowledge.

    USE THIS WHEN:
    - Question is general/conversational (greetings, thanks, etc.)
    - Question doesn't require specific medical facts
    - Question is about the chatbot itself

    Args:
        query: The user's question

    Returns:
        dict with 'answer' and metadata
    """
    print(f"💬 DIRECT TOOL: Answering directly with LLM: {query}")

    # Use Ollama to generate a helpful response
    try:
        from langchain_ollama import ChatOllama
        llm_direct = ChatOllama(model="llama3.2:1b", temperature=0.7)

        prompt = f"""You are a helpful and caring breast health assistant. Answer this question conversationally and warmly:

Question: {query}

Provide a brief, helpful answer in 2-3 sentences."""

        response = llm_direct.invoke(prompt)
        answer = response.content if hasattr(response, 'content') else str(response)

        return {
            "answer": answer,
            "sources": ["AI Assistant"],
            "confidence": 0.6,
            "tool_used": "direct_answer"
        }
    except Exception as e:
        print(f"❌ Error in direct_answer_tool: {e}")
        return {
            "answer": "I'm here to help! Could you please rephrase your question or ask about breast cancer screening, prevention, or symptoms?",
            "sources": ["AI Assistant"],
            "confidence": 0.3,
            "tool_used": "direct_answer"
        }


# Combine all tools into a list for LangGraph
tools = [rag_search_tool, web_search_tool, direct_answer_tool]


# ============================================================================
# STEP 3: INITIALIZE THE LLM (The agent's brain)
# ============================================================================
"""
LLM EXPLANATION:
This is the "brain" that makes decisions. We use Ollama with llama3.2:1b.
The LLM:
- Reads the conversation history
- Decides which tool to call
- Synthesizes final answers
- Verifies if more information is needed
"""

llm = ChatOllama(
    model="llama3.2:1b",  # Small, fast, runs locally
    temperature=0.2,  # Low temperature = more focused, less creative
)

# Bind tools to the LLM so it knows what functions it can call
llm_with_tools = llm.bind_tools(tools)


# ============================================================================
# STEP 4: DEFINE THE NODES (Steps in the workflow)
# ============================================================================
"""
NODES EXPLANATION:
Nodes are processing steps in the graph. Each node:
1. Reads the current state
2. Does some processing
3. Updates the state
4. Returns the new state

Think of nodes as assembly line stations - each does one job.
"""

def router_node(state: AgentState) -> AgentState:
    """
    ROUTER NODE: The decision-maker

    This node analyzes the user's question and decides which tool to use.
    It's like a traffic controller directing queries to the right destination.

    DECISION LOGIC:
    - Keywords like "latest", "recent", "2024" → Web search
    - Medical keywords (symptoms, screening, prevention) → RAG search
    - General conversation → Direct answer
    """
    print("🚦 ROUTER: Analyzing query and deciding which tool to use...")

    messages = state["messages"]
    last_message = messages[-1].content if messages else ""

    # Simple keyword-based routing (can be enhanced with LLM decision)
    query_lower = last_message.lower()

    # Check for recent/current info requests
    if any(word in query_lower for word in ["latest", "recent", "2024", "2025", "current", "new"]):
        query_type = "recent_info"
        print("   → Decision: Use WEB SEARCH (query asks for recent info)")

    # Check for medical/educational questions (expanded keywords)
    elif any(word in query_lower for word in [
        "symptom", "sign", "screening", "prevention", "risk", "exam", "treatment",
        "cancer", "breast", "mammogram", "tumor", "lump", "diagnosis", "doctor",
        "hospital", "health", "medical", "test", "biopsy", "self-exam", "check",
        "detect", "early", "stage", "types", "kind", "disease", "condition"
    ]):
        query_type = "medical"
        print("   → Decision: Use RAG SEARCH (medical question)")

    # General conversation
    else:
        query_type = "general"
        print("   → Decision: Use DIRECT ANSWER (general question)")

    state["query_type"] = query_type
    state["current_step"] = "router"

    return state


def tool_execution_node(state: AgentState) -> AgentState:
    """
    TOOL EXECUTION NODE: Runs the chosen tool

    Based on the router's decision, this node:
    1. Gets the appropriate tool
    2. Calls it with the user's query
    3. Stores the results in state
    """
    print("⚙️ TOOL EXECUTOR: Running the selected tool...")

    query_type = state["query_type"]
    last_message = state["messages"][-1].content

    # Execute the appropriate tool
    if query_type == "medical":
        result = rag_search_tool.invoke({"query": last_message})
    elif query_type == "recent_info":
        result = web_search_tool.invoke({"query": last_message})
    else:
        result = direct_answer_tool.invoke({"query": last_message})

    # Store results in state
    state["tool_results"] = result
    state["confidence"] = result["confidence"]
    state["sources"] = result["sources"]
    state["current_step"] = "tool_execution"

    print(f"   ✅ Tool completed with confidence: {result['confidence']:.2f}")

    return state


def verification_node(state: AgentState) -> AgentState:
    """
    VERIFICATION NODE: Checks if we have a good answer

    This node evaluates:
    - Is confidence high enough? (> 0.5)
    - Do we have sources?
    - Is the answer complete?

    If not satisfied, it can trigger another search.
    """
    print("✓ VERIFICATION: Checking if answer is sufficient...")

    confidence = state["confidence"]
    sources = state["sources"]

    # Decision criteria
    if confidence >= 0.5 and sources:
        print(f"   ✅ Answer is good (confidence: {confidence:.2f})")
        state["current_step"] = "verified"
    else:
        print(f"   ⚠️ Answer is weak (confidence: {confidence:.2f}), may need more sources")
        state["current_step"] = "needs_improvement"

    return state


def synthesize_node(state: AgentState) -> AgentState:
    """
    SYNTHESIZE NODE: Creates the final answer

    This node:
    1. Takes tool results
    2. Formats them nicely
    3. Adds source citations
    4. Creates a coherent, helpful response
    """
    print("✨ SYNTHESIZE: Creating final answer...")

    tool_results = state["tool_results"]
    query_type = state["query_type"]

    # Build the final answer with context
    answer = tool_results["answer"]
    sources = tool_results["sources"]

    # Add helpful context based on query type
    if query_type == "medical":
        final_answer = f"{answer}\n\n📚 **Sources:** Medical knowledge base"
    elif query_type == "recent_info":
        final_answer = f"{answer}\n\n🌐 **Sources:** {', '.join(sources[:2])}\n\n⚠️ *Note: Please verify current medical information with healthcare providers.*"
    else:
        final_answer = answer

    # Add AI message to conversation
    state["messages"].append(AIMessage(content=final_answer))
    state["current_step"] = "complete"

    print("   ✅ Final answer ready!")

    return state


# ============================================================================
# STEP 5: BUILD THE GRAPH (Connect everything together)
# ============================================================================
"""
GRAPH EXPLANATION:
The graph is the flowchart that connects all nodes.
It defines:
- Which node runs first
- What happens after each node
- When to end

Think of it as a roadmap for the agent to follow.
"""

def create_agent_graph():
    """
    Creates and returns the complete agentic RAG workflow graph.

    GRAPH FLOW:
    START → Router → Tool Execution → Verification → Synthesize → END
    """
    print("🏗️ Building LangGraph workflow...")

    # Create the graph with our state schema
    workflow = StateGraph(AgentState)

    # Add all nodes
    workflow.add_node("router", router_node)
    workflow.add_node("tool_execution", tool_execution_node)
    workflow.add_node("verification", verification_node)
    workflow.add_node("synthesize", synthesize_node)

    # Define the flow (edges between nodes)
    workflow.set_entry_point("router")  # Start here
    workflow.add_edge("router", "tool_execution")  # Router → Tool execution
    workflow.add_edge("tool_execution", "verification")  # Tool → Verify
    workflow.add_edge("verification", "synthesize")  # Verify → Synthesize
    workflow.add_edge("synthesize", END)  # Synthesize → End

    # Add memory so the agent remembers conversation history
    memory = MemorySaver()

    # Compile the graph
    app = workflow.compile(checkpointer=memory)

    print("   ✅ Graph built successfully!")

    return app


# ============================================================================
# STEP 6: MAIN INTERFACE (How to use the agent)
# ============================================================================
"""
USAGE EXPLANATION:
This is the main function you'll call from your API.
It handles:
- Creating the initial state
- Running the graph
- Extracting the final answer
"""

def query_agentic_rag(user_question: str, conversation_id: str = "default") -> dict:
    """
    Main function to query the agentic RAG system.

    Args:
        user_question: The user's question
        conversation_id: Unique ID for this conversation (for memory)

    Returns:
        dict with 'answer', 'sources', 'confidence', 'tool_used'

    Example:
        >>> result = query_agentic_rag("What are breast cancer symptoms?")
        >>> print(result["answer"])
    """
    print(f"\n{'='*60}")
    print(f"🤖 NEW QUERY: {user_question}")
    print(f"{'='*60}\n")

    # Create the agent graph
    agent = create_agent_graph()

    # Initialize state
    initial_state = {
        "messages": [HumanMessage(content=user_question)],
        "tool_results": {},
        "current_step": "start",
        "confidence": 0.0,
        "sources": [],
        "query_type": ""
    }

    # Run the graph
    config = {"configurable": {"thread_id": conversation_id}}

    try:
        # Execute the workflow
        final_state = agent.invoke(initial_state, config)

        # Extract results
        last_message = final_state["messages"][-1].content

        result = {
            "answer": last_message,
            "sources": final_state["sources"],
            "confidence": final_state["confidence"],
            "tool_used": final_state["tool_results"].get("tool_used", "unknown"),
            "query_type": final_state["query_type"]
        }

        print(f"\n{'='*60}")
        print(f"✅ COMPLETE: Answered using {result['tool_used']}")
        print(f"{'='*60}\n")

        return result

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return {
            "answer": "I apologize, but I encountered an error processing your question. Please try again.",
            "sources": [],
            "confidence": 0.0,
            "tool_used": "error",
            "error": str(e)
        }


# ============================================================================
# TESTING (Run this file directly to test)
# ============================================================================

if __name__ == "__main__":
    """
    Test the agentic RAG system with sample questions.
    Run: python -m app.agentic_rag
    """
    print("\n🧪 TESTING AGENTIC RAG SYSTEM\n")

    # Test questions covering different scenarios
    test_questions = [
        "What are the early signs of breast cancer?",  # Medical → RAG
        "What's the latest breast cancer research in 2024?",  # Recent → Web
        "Hello, how are you?",  # General → Direct
    ]

    for question in test_questions:
        result = query_agentic_rag(question)
        print(f"\nQ: {question}")
        print(f"A: {result['answer'][:200]}...")
        print(f"Tool: {result['tool_used']}, Confidence: {result['confidence']:.2f}")
        print("-" * 60)
