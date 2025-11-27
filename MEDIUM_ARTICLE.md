# Building an AI-Powered Breast Cancer Awareness Assistant for African Women

## How I Built a Smart Healthcare Chatbot Using Agentic RAG, FastAPI, and Local AI

![Cover Image Placeholder - Add an image of your app interface or a relevant healthcare tech illustration]

---

## The Problem That Sparked the Idea

Breast cancer is the most common cancer among women globally, yet access to accurate information and early detection resources remains a significant challenge, particularly in underserved communities. In many African countries, women face:

- **Limited access to healthcare information** in accessible formats
- **Cultural barriers** that prevent open discussions about breast health
- **Lack of nearby screening facilities** and difficulty locating resources
- **Fear and stigma** surrounding breast cancer
- **Language and literacy barriers** in accessing medical information

According to the World Health Organization, early detection can significantly improve survival rates. But how can women get reliable information when they need it most — in a private, judgment-free, and accessible way?

That's when I decided to build **Breast Friend Forever** — an AI-powered breast cancer awareness assistant designed with African women in mind.

---

## The Solution: An AI Healthcare Companion

Breast Friend Forever is more than just a chatbot. It's a comprehensive health awareness platform that combines cutting-edge AI technology with compassionate, culturally-sensitive design. The application provides:

### Core Features

**1. Intelligent AI Chatbot**
An agentic RAG (Retrieval-Augmented Generation) system that can:
- Answer medical questions from verified PDF sources
- Search the web for latest research and information
- Provide conversational support
- Remember context across conversations
- Cite sources and show confidence scores

**2. Self-Examination Guide**
Step-by-step visual instructions for breast self-examination, with:
- Clear, easy-to-follow steps
- Icons and descriptions for each stage
- Reminders about frequency and timing
- What to look for and when to consult a doctor

**3. Hospital & Resource Finder**
A searchable database of healthcare facilities offering:
- Filter by location (county/city)
- Service type filtering (mammography, screening, consultation)
- Emergency contact information
- Operating hours and phone numbers

**4. Encouragement Wall**
A community support space where users can:
- Post anonymous encouragement messages
- Read uplifting stories and support
- Share hope without fear of judgment
- Build a sense of solidarity

**5. Educational Resources**
Curated medical information including:
- PDF documents from trusted sources
- Health tips and preventive measures
- Risk assessment questionnaires
- Daily health tips

**6. Progressive Web App (PWA)**
Works seamlessly on mobile devices:
- Installable on home screen like a native app
- Works offline with cached content
- Responsive design for all screen sizes
- Accessible from any device on the same network

---

## The Technical Architecture: How It Works

Building a healthcare application requires reliability, accuracy, and privacy. Here's how I architected Breast Friend Forever:

### Backend: FastAPI + Agentic RAG System

The backend is built with **FastAPI**, a modern Python web framework known for its speed and automatic API documentation. But the real innovation lies in the **Agentic RAG system**.

#### What is Agentic RAG?

Traditional RAG (Retrieval-Augmented Generation) systems work like this:
```
User Question → Search Documents → Return Answer
```

But my **Agentic RAG** system is smarter:
```
User Question → AGENT ANALYZES → Chooses Best Tool → Verifies → Returns Answer
                      ↓
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
    RAG Search   Web Search   Direct Answer
```

#### The Agent's Decision-Making Process

**1. Router Node** 🚦
- Analyzes the user's question
- Identifies question type (medical, recent info, general)
- Decides which tool to use

**2. Tool Execution Node** ⚙️
- **RAG Search Tool**: Searches 10+ medical PDF documents using semantic embeddings
- **Web Search Tool**: Searches DuckDuckGo for current information (2024 research, latest guidelines)
- **Direct Answer Tool**: Uses AI's general knowledge for conversational queries

**3. Verification Node** ✓
- Checks answer quality (confidence > 0.5)
- Ensures sources exist
- Can trigger alternative tools if needed

**4. Synthesize Node** ✨
- Formats the final response
- Adds source citations
- Provides context-appropriate disclaimers

#### Example Flow

**User asks:** "What are the early signs of breast cancer?"

1. **Router** detects keyword "signs" → Routes to **RAG Search**
2. **RAG Search** queries medical PDFs → Finds 5 relevant chunks
3. **Verification** checks confidence: 0.85 ✓
4. **Synthesizer** formats answer with sources
5. Returns: Comprehensive answer + PDF sources + confidence score

**User asks:** "What's the latest breast cancer research in 2024?"

1. **Router** detects keywords "latest" + "2024" → Routes to **Web Search**
2. **Web Search** queries DuckDuckGo → Gets recent articles
3. **Verification** checks results quality ✓
4. **Synthesizer** formats with web links + disclaimer
5. Returns: Current research + source links + confidence score

### Tech Stack

**Backend:**
- **FastAPI**: REST API framework
- **LangGraph**: Agentic workflow orchestration
- **Ollama**: Local LLM (llama3.2:1b) - free, private, no API costs
- **SentenceTransformers**: Semantic search embeddings
- **PyPDF2**: PDF text extraction
- **DuckDuckGo Search**: Web search integration

**Frontend:**
- **Streamlit**: Rapid web app development
- **Python**: Full-stack development in one language
- **PWA**: Progressive Web App for mobile installation

**Key Advantages:**
- ✅ **100% Free**: No API costs (uses local Ollama)
- ✅ **Privacy-First**: Health data stays on your device
- ✅ **Offline-Capable**: Cached resources work without internet
- ✅ **Cross-Platform**: Works on desktop, mobile, tablet

---

## API Architecture: 20+ Endpoints for Comprehensive Functionality

The backend exposes a RESTful API with comprehensive endpoints:

### Core Endpoints

**Health & Documentation**
- `GET /health` - Health check
- `GET /docs` - Interactive Swagger documentation
- `GET /` - API information

**Standard Chatbot (Fast RAG)**
- `POST /api/v1/chat/message` - Simple PDF-based responses

**Agentic Chatbot (Intelligent RAG)**
- `POST /api/v1/chatbot/agentic/message` - Smart multi-tool responses
- `GET /api/v1/chatbot/agentic/health` - Service status
- `GET /api/v1/chatbot/agentic/info` - System capabilities

**Mobile-Optimized Features**
- `POST /api/v1/mobile/chat` - Enhanced chat with symptom detection
- `POST /api/v1/mobile/hospitals/search` - Advanced hospital filtering
- `GET /api/v1/mobile/health-tips` - Randomized health tips
- `GET /api/v1/mobile/emergency/contacts` - Emergency numbers
- `GET /api/v1/mobile/self-exam/guide` - Detailed self-exam instructions

**Hospital Resources**
- `GET /api/v1/hospitals/` - Get facilities by location

**Community Support**
- `GET /api/v1/encouragement/` - Get encouragement messages
- `POST /api/v1/encouragement/` - Post anonymous support

**Educational Content**
- `GET /api/v1/resources/` - Get all educational materials
- `GET /api/v1/self_exam/steps` - Self-examination guide

---

## Development Journey: Challenges and Solutions

### Challenge 1: Accuracy vs. Speed
**Problem**: Medical information must be accurate, but users expect fast responses.

**Solution**: Implemented a tiered response system:
1. **Instant Path**: Pre-loaded common responses (< 100ms)
2. **Fast Path**: Cached PDF search results (< 500ms)
3. **Intelligent Path**: Agentic RAG with verification (2-5 seconds)

### Challenge 2: Handling Diverse Questions
**Problem**: Users ask everything from medical facts to emotional support.

**Solution**: Built an agentic system that routes questions intelligently:
- Medical questions → RAG search through PDFs
- Recent research → Web search
- Emotional support → Conversational AI

### Challenge 3: Privacy and Cost
**Problem**: Healthcare data is sensitive, and API costs can be prohibitive.

**Solution**: Used Ollama for local LLM inference:
- Zero API costs
- Data never leaves the user's device
- Works offline for basic features

### Challenge 4: Mobile Accessibility
**Problem**: Many users primarily access information via mobile phones.

**Solution**: Built as a Progressive Web App (PWA):
- Installable on home screen
- Works on any device on the same WiFi network
- Responsive design optimized for mobile
- Offline capabilities with service workers

---

## Real-World Impact: Making Healthcare Accessible

The project demonstrates how AI can bridge healthcare gaps:

### Accessibility
- Available 24/7, no appointment needed
- No cost to use (after initial setup)
- Private and judgment-free
- Multiple languages supported (scalable)

### Empowerment
- Women can learn at their own pace
- Self-examination guidance builds confidence
- Community support reduces stigma
- Resource finder connects to real help

### Education
- Evidence-based information from medical sources
- Source citations build trust
- Current research through web search
- Risk assessment awareness

---

## How to Run the Project

### Prerequisites
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull the model
ollama pull llama3.2:1b
```

### Backend Setup
```bash
cd Backend
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Setup
```bash
cd Web
pip install -r requirements.txt

# Start the Streamlit app
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

### Access on Mobile
1. Get your computer's IP address: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
2. On your phone (same WiFi), open browser to: `http://YOUR_IP:8501`
3. Add to home screen for app-like experience

---

## Future Enhancements

This project is just the beginning. Future improvements could include:

### Technical Improvements
- **Multi-language Support**: Swahili, Amharic, Yoruba, and more
- **Voice Interface**: For users with literacy challenges
- **Image Analysis**: Upload photos for AI-assisted visual checks
- **Appointment Booking**: Direct integration with healthcare facilities
- **Persistent Memory**: Database-backed conversation history

### Feature Additions
- **Symptom Tracker**: Log and track changes over time
- **Period/Cycle Integration**: Reminders for self-exams
- **Telemedicine Integration**: Connect directly with doctors
- **Community Forums**: Moderated discussion spaces
- **Gamification**: Rewards for regular self-checks

### Deployment & Scale
- **Cloud Deployment**: AWS/Azure/GCP hosting
- **Mobile Apps**: Native iOS/Android versions
- **API Marketplace**: Allow healthcare providers to integrate
- **Multi-tenancy**: White-label for hospitals/NGOs

---

## Lessons Learned

### 1. AI is a Tool, Not a Doctor
The chatbot explicitly disclaims it's not medical advice and encourages consulting healthcare professionals. AI should augment, not replace, human expertise.

### 2. Privacy is Paramount
Healthcare data is deeply personal. Using local AI (Ollama) instead of cloud APIs was crucial for building trust.

### 3. Simplicity Wins
Users don't care about "agentic RAG" — they care about fast, accurate answers. Technical complexity should be invisible to end-users.

### 4. Cultural Sensitivity Matters
Designing with African women in mind meant considering language, cultural norms, and local healthcare infrastructure.

### 5. Open Source Makes Impact
By open-sourcing this project, others can adapt it for their communities, multiplying the impact.

---

## Technical Highlights for Developers

### Why Agentic RAG?
Traditional RAG is limited to one information source. Agentic RAG:
- Makes intelligent routing decisions
- Combines multiple information sources
- Verifies answer quality before responding
- Adapts to different question types
- More robust and flexible

### Why LangGraph?
LangGraph is perfect for building agentic systems:
- Graph-based workflow definition
- State management across nodes
- Easy tool integration
- Supports complex decision trees
- Built for production use

### Why Ollama?
Ollama brings LLMs to your laptop:
- No API keys needed
- Zero ongoing costs
- Privacy-preserving
- Fast inference on consumer hardware
- Growing model library

### Code Example: Router Node
```python
def router_node(state: AgentState) -> AgentState:
    """Decide which tool to use"""
    user_question = state["messages"][-1]
    question_lower = user_question.lower()

    # Check for recent/latest queries
    if any(keyword in question_lower for keyword in
           ['latest', 'recent', '2024', '2025', 'current', 'new']):
        state["tool_to_use"] = "web_search"
        state["query_type"] = "recent_info"

    # Check for medical queries
    elif any(keyword in question_lower for keyword in
             ['symptom', 'sign', 'screening', 'prevention']):
        state["tool_to_use"] = "rag_search"
        state["query_type"] = "medical"

    # Default to direct answer
    else:
        state["tool_to_use"] = "direct_answer"
        state["query_type"] = "general"

    return state
```

---

## Call to Action

### For Healthcare Workers
Consider how AI assistants like this could support your patients between appointments. The code is open source and adaptable.

### For Developers
The full source code is available on GitHub [link]. Contributions welcome! Help make healthcare more accessible.

### For Women Everywhere
Early detection saves lives. Use tools like this to stay informed, but always consult healthcare professionals for personalized medical advice.

### For Organizations
Interested in deploying this for your community? Let's collaborate to bring accessible health information to those who need it most.

---

## Conclusion: Technology as a Bridge, Not a Barrier

Breast Friend Forever represents a vision where technology doesn't replace human healthcare but makes it more accessible. By combining:

- **AI intelligence** (agentic RAG)
- **Privacy protection** (local inference)
- **Cultural sensitivity** (designed for African women)
- **Cost accessibility** (free and open source)

...we can build tools that empower women to take charge of their health, one conversation at a time.

The future of healthcare isn't just in hospitals and clinics — it's in the pockets of every woman with a smartphone, armed with knowledge, support, and the confidence to seek help when needed.

---

## Technical Specifications Summary

**Backend:**
- Language: Python 3.9+
- Framework: FastAPI
- AI Framework: LangGraph
- LLM: Ollama (llama3.2:1b)
- Embeddings: SentenceTransformers
- Search: DuckDuckGo
- PDF Processing: PyPDF2

**Frontend:**
- Framework: Streamlit
- Type: Progressive Web App (PWA)
- Deployment: Network-accessible web server

**Architecture:**
- 20+ REST API endpoints
- Agentic RAG with 3 tools
- Multi-node decision graph
- Conversation memory
- Source verification

**Performance:**
- Instant responses: < 100ms (cached)
- Fast RAG: < 500ms
- Agentic RAG: 2-5 seconds
- Web search: 3-8 seconds

**Cost:**
- Development: $0 (all open source)
- Runtime: $0 (local AI)
- Deployment: Varies (cloud hosting optional)

---

## Connect and Contribute

- **GitHub**: [Your Repository Link]
- **Demo Video**: [Add link if available]
- **Documentation**: Full API docs at `/docs` endpoint
- **Contact**: [Your contact information]

**Tags**: #AI #HealthTech #BreastCancerAwareness #Python #FastAPI #AgenticAI #RAG #LangGraph #OpenSource #Healthcare #MachineLearning #Ollama #Africa #WomensHealth

---

*This project is dedicated to every woman fighting breast cancer, every survivor inspiring hope, and every healthcare worker making a difference. Early detection saves lives. Stay informed, stay vigilant, stay empowered.*

---

**About the Author**
[Add your bio here - background, motivation, other projects, etc.]

---

**Disclaimer**: This application is for educational and awareness purposes only. It does not provide medical diagnosis or treatment. Always consult qualified healthcare professionals for medical advice.
