# Backend/app/api/endpoints/chatbot.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import PyPDF2
from typing import List, Optional

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    source: str
    confidence: str

# PDF Search System
class PDFSearcher:
    def __init__(self, pdf_directory="app/data/pdfs"):
        self.pdf_directory = pdf_directory
        os.makedirs(self.pdf_directory, exist_ok=True)
        self.pdf_content = self.load_all_pdfs()
    
    def load_all_pdfs(self):
        """Load and index all PDFs in the PDF directory"""
        content = []
        if not os.path.exists(self.pdf_directory):
            print(f"⚠️ PDF directory not found: {self.pdf_directory}")
            return content
            
        for filename in os.listdir(self.pdf_directory):
            if filename.endswith(".pdf"):
                filepath = os.path.join(self.pdf_directory, filename)
                text = self.extract_pdf_text(filepath)
                content.append({
                    "filename": filename,
                    "content": text,
                    "chunks": self.chunk_text(text)
                })
                print(f"📚 Loaded PDF: {filename} ({len(text)} characters)")
        return content
    
    def extract_pdf_text(self, pdf_path):
        """Extract text from PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"❌ Error reading PDF {pdf_path}: {e}")
            return ""
    
    def chunk_text(self, text, chunk_size=500):
        """Split text into manageable chunks"""
        words = text.split()
        chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
        return chunks
    
    def search(self, query, top_k=3):
        """Search PDFs for relevant information"""
        query = query.lower()
        results = []
        
        for doc in self.pdf_content:
            for chunk in doc['chunks']:
                if query in chunk.lower():
                    # Simple relevance scoring
                    score = chunk.lower().count(query)
                    results.append({
                        "content": chunk,
                        "source": doc['filename'],
                        "score": score
                    })
        
        # Return top results
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]

# Initialize PDF search
pdf_searcher = PDFSearcher()

@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """Chat endpoint that searches PDFs for medical information"""
    try:
        # Search PDFs for relevant information
        pdf_results = pdf_searcher.search(request.message)
        
        if pdf_results:
            # Build response directly from PDF content
            response = build_response_from_pdfs(pdf_results, request.message)
            return ChatResponse(
                response=response,
                source=f"Medical Documents: {', '.join(set(r['source'] for r in pdf_results))}",
                confidence="high"
            )
        else:
            # Use improved fallback without OpenAI
            response = get_improved_fallback(request.message)
            return ChatResponse(
                response=response,
                source="Medical Knowledge Base", 
                confidence="medium"
            )
            
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return ChatResponse(
            response="I'm experiencing technical difficulties. Please try again.",
            source="System",
            confidence="low"
        )

def build_response_from_pdfs(pdf_results, question):
    """Build response directly from PDF content"""
    # Extract the most relevant content
    main_content = pdf_results[0]['content'] if pdf_results else ""
    
    # Format a nice response
    response = f"**Based on medical resources:**\n\n{main_content}\n\n"
    
    # Add additional context from other PDFs if available
    if len(pdf_results) > 1:
        response += "\n**Additional information:**\n"
        for result in pdf_results[1:3]:  # Add up to 2 more sources
            response += f"\n• {result['content'][:200]}...\n"
    
    response += "\n💖 *Remember to consult healthcare professionals for personal medical advice.*"
    return response

def get_improved_fallback(question):
    """Enhanced fallback without OpenAI"""
    question_lower = question.lower()
    
    # Comprehensive medical responses
    medical_responses = {
        "self exam": get_detailed_self_exam(),
        "early sign": get_early_signs(),
        "symptom": get_symptoms(),
        "prevent": get_prevention(),
        "check": get_detailed_self_exam(),
        "lump": "If you find a lump in your breast, it's important not to panic. Many lumps are not cancerous. However, you should schedule an appointment with a healthcare provider for proper evaluation. They may recommend imaging tests like a mammogram or ultrasound.",
        "pain": "Breast pain can have many causes including hormonal changes, cysts, or muscle strain. While most breast pain isn't cancer, persistent pain should be evaluated by a doctor, especially if it's in one specific area.",
        "mammogram": "Mammograms are X-ray images of the breast used to detect early signs of cancer. Most guidelines recommend starting regular mammograms between ages 40-50. African women may need to start earlier if there's family history.",
        "risk": "Breast cancer risk factors include: family history, certain genetic mutations, early menstruation, late menopause, never having children, alcohol consumption, and obesity. African women often face more aggressive subtypes, making early detection crucial."
    }
    
    for key, response in medical_responses.items():
        if key in question_lower:
            return response
    
    return "I understand you're asking about breast health. I'm here to provide information from medical resources. Could you be more specific about what you'd like to know? For example, you could ask about self-examination techniques, early warning signs, or prevention strategies."

def get_detailed_self_exam():
    return """**Step-by-Step Breast Self-Examination:**

1. **Visual Inspection (in mirror):**
   - Stand with arms at your sides, look for changes in size, shape, or contour
   - Raise arms overhead, check for the same changes
   - Look for skin dimpling, redness, rash, or nipple changes

2. **Manual Examination (lying down):**
   - Lie down with pillow under right shoulder, right arm behind head
   - Use left hand fingers to feel right breast in small circular motions
   - Cover entire breast from collarbone to abdomen, armpit to breastbone
   - Repeat on left side

3. **Manual Examination (standing/sitting):**
   - Repeat same process while standing or in shower
   - Many women find wet, soapy skin makes examination easier

**When to examine:** Monthly, 3-5 days after your period ends
**What to look for:** New lumps, thickening, swelling, dimpling, pain, nipple changes
**Important:** This complements but doesn't replace clinical exams!"""

def get_early_signs():
    return """**Early Signs of Breast Cancer:**

• New lump in breast or armpit
• Thickening or swelling of breast tissue
• Irritation or dimpling of breast skin (like orange peel)
• Redness or flaky skin in nipple area or breast
• Pulling in of nipple or pain in nipple area
• Nipple discharge (including blood)
• Any change in size or shape of breast
• Pain in any area of breast

**Important notes:**
- Many breast changes are NOT cancer
- All new or changing symptoms should be checked by a doctor
- Early detection significantly improves outcomes
- African women should be particularly vigilant about changes"""

def get_symptoms():
    return """**Possible Breast Cancer Symptoms:**

🔍 **Common indicators:**
- New lump or mass (often painless, hard, irregular edges)
- Swelling of all or part of breast
- Skin irritation or dimpling
- Breast or nipple pain
- Nipple retraction (turning inward)
- Redness, scaliness, or thickening of nipple/breast skin
- Nipple discharge (especially if bloody or clear)
- Lump in underarm area

🎗️ **For African women:**
- May experience more aggressive subtypes
- Often diagnosed at later stages
- Should be proactive about screening
- Know your family history"""

def get_prevention():
    return """**Breast Cancer Prevention Strategies:**

✅ **Proven methods:**
- Maintain healthy weight
- Exercise regularly (150+ minutes/week moderate activity)
- Limit alcohol consumption
- Avoid smoking
- Breastfeed if possible
- Eat balanced diet rich in fruits/vegetables
- Regular screenings after age 40 (earlier if high risk)

🎗️ **For African women specifically:**
- Know your genetic risk factors
- Start screenings earlier if family history exists
- Advocate for yourself in healthcare settings
- Participate in community awareness programs
- Understand that dense breast tissue may require additional screening

**Remember:** While we can reduce risk, there's no guaranteed prevention. Early detection is key!"""

# Health check for chatbot
@router.get("/health")
async def chat_health():
    return {
        "status": "healthy", 
        "service": "chatbot",
        "pdfs_loaded": len(pdf_searcher.pdf_content)
    }