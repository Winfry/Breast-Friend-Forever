# I Built an AI Breast Cancer Assistant That Works on Your Phone — Here's How

## Using Agentic RAG to Make Healthcare Information Accessible

![Cover Image - Your app screenshot or relevant healthcare illustration]

---

## The Problem

Breast cancer affects millions of women worldwide, but access to reliable information remains a challenge. Women need:
- Accurate medical information on-demand
- Private, judgment-free guidance
- Easy access to healthcare resources
- Community support

So I built **Breast Friend Forever** — an AI-powered breast cancer awareness assistant designed for African women.

---

## What It Does

### 1. Smart AI Chatbot
Unlike basic chatbots, this uses **Agentic RAG** — an intelligent system that:
- Searches medical PDFs for verified information
- Searches the web for latest research
- Decides which source is best for each question
- Cites sources and shows confidence scores

### 2. Self-Exam Guide
Step-by-step visual instructions with reminders and tips.

### 3. Hospital Finder
Searchable database of healthcare facilities with filters for location and services.

### 4. Community Support
Anonymous encouragement wall where women can share hope and solidarity.

### 5. Works on Mobile
Progressive Web App that installs like a native app on any phone.

---

## The Innovation: Agentic RAG

**Traditional RAG:**
```
Question → Search PDFs → Answer
```

**My Agentic RAG:**
```
Question → AI Analyzes → Picks Best Tool → Verifies Quality → Answer
                ↓
    [PDF Search | Web Search | Direct Answer]
```

**Example 1:**
- **Question**: "What are early signs of breast cancer?"
- **Agent decides**: Use PDF search
- **Result**: Medical answer from verified sources

**Example 2:**
- **Question**: "What's the latest 2024 breast cancer research?"
- **Agent decides**: Use web search
- **Result**: Current research with links

---

## Tech Stack

**Why It's Special:**
- ✅ **100% Free** - Uses local AI (Ollama), no API costs
- ✅ **Private** - Health data stays on your device
- ✅ **Works Offline** - Cached content available without internet
- ✅ **No App Store** - Progressive Web App installs directly

**Backend:**
- FastAPI (REST API)
- LangGraph (Agentic workflows)
- Ollama (Local LLM - llama3.2:1b)
- SentenceTransformers (Semantic search)

**Frontend:**
- Streamlit (Web app)
- PWA (Mobile installation)

---

## How to Use It on Your Phone

1. Start backend: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
2. Start frontend: `streamlit run app.py --server.address 0.0.0.0`
3. Get your computer's IP: `ipconfig`
4. On phone (same WiFi): Open `http://YOUR_IP:8501`
5. Add to home screen!

---

## The Architecture

**20+ API Endpoints:**
- Standard chatbot (fast)
- Agentic chatbot (intelligent)
- Hospital search
- Self-exam guides
- Emergency contacts
- Health tips
- Community wall

**Smart Decision Making:**
1. **Router** - Analyzes question type
2. **Tool Executor** - Runs appropriate tool
3. **Verifier** - Checks answer quality
4. **Synthesizer** - Formats final response

---

## Real Impact

**Accessibility:**
- 24/7 availability
- No cost to use
- Private and confidential
- Works on any device

**Empowerment:**
- Self-paced learning
- Confidence through knowledge
- Community support
- Direct links to help

---

## Technical Highlights

### Why Agentic RAG?
Traditional chatbots are one-size-fits-all. Agentic systems:
- Make intelligent decisions
- Choose appropriate information sources
- Verify answer quality
- Adapt to different questions

### Why Local AI?
Using Ollama instead of cloud APIs means:
- Zero ongoing costs
- Complete privacy
- Works offline
- No API rate limits

### Code Sample: The Router
```python
def router_node(state: AgentState):
    question = state["messages"][-1].lower()

    # Recent info → Web search
    if 'latest' in question or '2024' in question:
        return "web_search"

    # Medical info → PDF search
    elif 'symptom' in question or 'screening' in question:
        return "rag_search"

    # Everything else → Direct answer
    else:
        return "direct_answer"
```

---

## Challenges Solved

**1. Accuracy vs Speed**
- Solution: 3-tier system (instant/fast/intelligent)

**2. Handling Diverse Questions**
- Solution: Agentic routing to appropriate tools

**3. Privacy & Cost**
- Solution: Local AI with Ollama

**4. Mobile Access**
- Solution: Progressive Web App

---

## Future Plans

- **Multi-language support** (Swahili, Amharic, Yoruba)
- **Voice interface** for accessibility
- **Image analysis** for visual checks
- **Appointment booking** integration
- **Native mobile apps** (iOS/Android)

---

## Lessons Learned

1. **AI augments, doesn't replace** healthcare professionals
2. **Privacy is paramount** in healthcare
3. **Simplicity wins** - hide technical complexity
4. **Cultural sensitivity** matters in design
5. **Open source** multiplies impact

---

## Try It Yourself

- **GitHub**: [Add your repo link]
- **Demo**: [Add demo link if available]
- **API Docs**: Available at `/docs` endpoint

---

## The Vision

Technology shouldn't be a barrier to healthcare — it should be a bridge. By combining:

- AI intelligence (agentic RAG)
- Privacy protection (local inference)
- Cultural sensitivity (African women-focused)
- Cost accessibility (free and open source)

We can empower women to take charge of their health, one conversation at a time.

---

**Early detection saves lives. Stay informed, stay vigilant, stay empowered.**

---

**Tags**: #AI #HealthTech #BreastCancer #Python #FastAPI #AgenticAI #RAG #OpenSource #WomensHealth

**Disclaimer**: For educational purposes only. Always consult healthcare professionals for medical advice.

---

**About the Author**
[Your bio here]
