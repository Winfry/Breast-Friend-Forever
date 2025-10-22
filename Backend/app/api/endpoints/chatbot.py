# Backend/app/api/endpoints/chatbot.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import PyPDF2
from typing import List, Optional
from functools import lru_cache
import time

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    source: str
    confidence: str

# PDF Search System with Caching
class PDFSearcher:
    def __init__(self, pdf_directory="app/data/pdfs"):
        self.pdf_directory = pdf_directory
        os.makedirs(self.pdf_directory, exist_ok=True)
        self.pdf_content = self.load_all_pdfs()
    
    def load_all_pdfs(self):
        """Load and index all PDFs in the PDF directory"""
        content = []
        print(f"🔍 Looking for PDFs in: {os.path.abspath(self.pdf_directory)}")
        
        if not os.path.exists(self.pdf_directory):
            print(f"❌ PDF directory doesn't exist: {self.pdf_directory}")
            return content
            
        files = os.listdir(self.pdf_directory)
        print(f"📄 Files found: {files}")
        
        for filename in files:
            if filename.endswith(".pdf"):
                filepath = os.path.join(self.pdf_directory, filename)
                print(f"📖 Processing PDF: {filename}")
                text = self.extract_pdf_text(filepath)
                if text.strip():
                    content.append({
                        "filename": filename,
                        "content": text,
                        "chunks": self.chunk_text(text)
                    })
                    print(f"✅ Loaded PDF: {filename} ({len(text)} characters)")
                else:
                    print(f"❌ Failed to read PDF: {filename}")
        return content
    
    def extract_pdf_text(self, pdf_path):
        """Extract text from PDF file with encryption handling"""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                # Handle encrypted PDFs gracefully
                if reader.is_encrypted:
                    try:
                        reader.decrypt("")  # try to decrypt with empty password
                        print(f"🔓 Decrypted PDF: {os.path.basename(pdf_path)}")
                    except Exception as e:
                        print(f"⚠️ Skipping encrypted PDF (needs password): {pdf_path} — {e}")
                        return ""

                text = ""
                for page in reader.pages:
                    try:
                        page_text = page.extract_text() or ""
                        text += page_text + "\n"
                    except Exception as e:
                        print(f"⚠️ Could not read a page in {pdf_path}: {e}")
                        continue
                
                return text.strip()
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            return ""

    def chunk_text(self, text, chunk_size=300):
        """Split text into manageable chunks"""
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < chunk_size:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks
    
    def search(self, query, top_k=3):
        """Search PDFs for relevant information"""
        query = query.lower()
        results = []
        
        for doc in self.pdf_content:
            for chunk in doc['chunks']:
                if query in chunk.lower():
                    score = chunk.lower().count(query)
                    results.append({
                        "content": chunk,
                        "source": doc['filename'],
                        "score": score
                    })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]

# Initialize PDF search
pdf_searcher = PDFSearcher()

# Pre-loaded common responses for INSTANT answers
COMMON_RESPONSES = {
    "self exam": """**Step-by-Step Breast Self-Examination:**

1. **Visual Inspection (in mirror):**
   - Stand with arms at your sides, look for changes in size, shape
   - Raise arms overhead, check for same changes
   - Look for skin dimpling, redness, rash, or nipple changes

2. **Manual Examination (lying down):**
   - Lie down with pillow under right shoulder, right arm behind head
   - Use left hand fingers to feel right breast in small circular motions
   - Cover entire breast from collarbone to abdomen
   - Repeat on left side

3. **Manual Examination (standing):**
   - Repeat in shower with wet, soapy skin
   - Many women find this easier

**When:** Monthly, 3-5 days after period ends
**What to look for:** New lumps, thickening, swelling, dimpling, pain, nipple changes""",

    "early sign": """**Early Signs of Breast Cancer:**

• New lump in breast or armpit
• Thickening or swelling of breast tissue
• Irritation or dimpling of breast skin
• Redness or flaky skin in nipple area
• Pulling in of nipple or nipple pain
• Nipple discharge (including blood)
• Any change in breast size or shape
• Pain in any area of breast

**Note:** Many breast changes are NOT cancer, but all should be checked.""",

    "symptom": """**Breast Cancer Symptoms:**

• New lump or mass (often painless, hard, irregular edges)
• Swelling of all or part of breast
• Skin irritation or dimpling
• Breast or nipple pain
• Nipple retraction (turning inward)
• Redness or thickening of nipple/breast skin
• Nipple discharge
• Lump in underarm area""",

    "risk factor": """**Breast Cancer Risk Factors:**

• Family history of breast cancer
• Certain genetic mutations (BRCA1, BRCA2)
• Early menstruation (before age 12)
• Late menopause (after age 55)
• Never having children
• Alcohol consumption
• Obesity
• Radiation exposure

**For African women:** May face more aggressive subtypes, making early detection crucial.""",

    "prevent": """**Breast Cancer Prevention:**

• Maintain healthy weight
• Exercise regularly (150+ mins/week)
• Limit alcohol consumption
• Avoid smoking
• Breastfeed if possible
• Eat balanced diet
• Regular screenings after age 40

**Remember:** While we can reduce risk, early detection is key!"""
}

@lru_cache(maxsize=100)
def cached_search(query: str):
    """Cache search results for faster responses"""
    return pdf_searcher.search(query)

def get_instant_response(question: str) -> Optional[str]:
    """Check for instant pre-loaded response"""
    question_lower = question.lower()
    for key, response in COMMON_RESPONSES.items():
        if key in question_lower:
            return response
    return None

def build_response_from_pdfs(pdf_results, question):
    """Build response directly from PDF content"""
    main_content = pdf_results[0]['content'] if pdf_results else ""
    
    response = f"**Based on medical resources:**\n\n{main_content}\n\n"
    
    if len(pdf_results) > 1:
        response += "\n**Additional information:**\n"
        for result in pdf_results[1:3]:
            response += f"\n• {result['content'][:200]}...\n"
    
    response += "\n💖 *Remember to consult healthcare professionals for personal medical advice.*"
    return response

@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """Optimized chat endpoint with caching"""
    start_time = time.time()
    
    try:
        # 1. INSTANT PATH: Check pre-loaded responses
        instant_response = get_instant_response(request.message)
        if instant_response:
            processing_time = time.time() - start_time
            print(f"⚡ INSTANT response in {processing_time:.3f}s")
            return ChatResponse(
                response=instant_response,
                source="Pre-loaded Medical Knowledge",
                confidence="high"
            )
        
        # 2. FAST PATH: Cached PDF search
        pdf_results = cached_search(request.message.lower())
        
        if pdf_results:
            response = build_response_from_pdfs(pdf_results, request.message)
            processing_time = time.time() - start_time
            print(f"🚀 FAST response in {processing_time:.3f}s")
            return ChatResponse(
                response=response,
                source=f"Medical Documents: {', '.join(set(r['source'] for r in pdf_results))}",
                confidence="high"
            )
        
        # 3. FALLBACK PATH
        response = "I understand you're asking about breast health. I can help with self-examination techniques, early warning signs, risk factors, or prevention strategies. What specific information would you like?"
        processing_time = time.time() - start_time
        print(f"🐢 SLOW fallback in {processing_time:.3f}s")
        return ChatResponse(
            response=response,
            source="Medical Knowledge Base",
            confidence="medium"
        )
        
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return ChatResponse(
            response="I'm here to help with breast health information. What would you like to know?",
            source="System",
            confidence="low"
        )

@router.get("/health")
async def chat_health():
    return {
        "status": "healthy", 
        "service": "chatbot",
        "pdfs_loaded": len(pdf_searcher.pdf_content),
        "common_responses": len(COMMON_RESPONSES)
    }