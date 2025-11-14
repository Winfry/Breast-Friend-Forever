import os
import PyPDF2
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import re

class BreastCancerRAG:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.knowledge_base = []
        self.embeddings = None
        
        # ✅ FIXED: Correct path to PDFs
        current_dir = os.path.dirname(__file__)
        self.pdf_folder = os.path.join(current_dir, "data", "pdfs")
        
        # Create PDF folder if it doesn't exist
        os.makedirs(self.pdf_folder, exist_ok=True)
        
    def load_all_pdfs(self):
        """Load and process all PDFs in the pdfs folder"""
        if not os.path.exists(self.pdf_folder):
            print(f"PDF folder not found: {self.pdf_folder}")
            return False

        pdf_files = [f for f in os.listdir(self.pdf_folder) if f.endswith('.pdf')]

        if not pdf_files:
            print("No PDF files found in the pdfs folder")
            return False
            
        self.knowledge_base = []
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(self.pdf_folder, pdf_file)
            try:
                with open(pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    for page_num, page in enumerate(reader.pages):
                        text = page.extract_text()
                        if text.strip():
                            # Clean and chunk the text
                            chunks = self._split_text(text, chunk_size=400)
                            for chunk in chunks:
                                self.knowledge_base.append({
                                    'text': chunk,
                                    'source': pdf_file,
                                    'page': page_num + 1
                                })
                print(f"✅ Loaded {pdf_file}")
            except Exception as e:
                print(f"❌ Error loading {pdf_file}: {e}")
        
        # Create embeddings
        if self.knowledge_base:
            texts = [item['text'] for item in self.knowledge_base]
            self.embeddings = self.embedding_model.encode(texts)
            print(f"✅ Created embeddings for {len(self.knowledge_base)} text chunks")
            return True
        return False
    
    def _split_text(self, text, chunk_size=400, overlap=50):
        """Split text into manageable chunks with overlap"""
        # Clean the text first
        text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
            
        return chunks
    
    def search(self, question, top_k=5):
        """Find most relevant text chunks for a question"""
        if not self.knowledge_base or self.embeddings is None:
            return []
        
        question_embedding = self.embedding_model.encode([question])
        similarities = cosine_similarity(question_embedding, self.embeddings)[0]
        
        # Get top matches
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        results = []
        
        for idx in top_indices:
            if similarities[idx] > 0.2:  # Moderate threshold
                results.append({
                    'text': self.knowledge_base[idx]['text'],
                    'source': self.knowledge_base[idx]['source'],
                    'page': self.knowledge_base[idx]['page'],
                    'similarity': similarities[idx]
                })
        
        return results
    
    def _summarize_chunks(self, chunks, question):
        """Summarize and structure the response for better readability"""
        if not chunks:
            return "I couldn't find specific information about that in our medical resources."
        
        # Extract key information based on question type
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['self exam', 'self-exam', 'check', 'examine']):
            return self._format_self_exam_response(chunks)
        elif any(word in question_lower for word in ['symptom', 'sign', 'early detection', 'warning']):
            return self._format_symptoms_response(chunks)
        elif any(word in question_lower for word in ['risk', 'prevent', 'reduce']):
            return self._format_prevention_response(chunks)
        elif any(word in question_lower for word in ['screening', 'mammogram', 'when', 'how often']):
            return self._format_screening_response(chunks)
        else:
            return self._format_general_response(chunks)
    
    def _format_self_exam_response(self, chunks):
        """Format self-examination information"""
        key_points = []
        
        for chunk in chunks:
            text = chunk['text'].lower()
            
            # Extract timing information
            if any(word in text for word in ['monthly', 'every month', 'regular']):
                if 'when' not in str(key_points).lower():
                    key_points.append("📅 **When to check:** Monthly, 3-5 days after your period ends")
            
            # Extract technique information
            if any(word in text for word in ['visual inspection', 'mirror', 'look']):
                if 'visual' not in str(key_points).lower():
                    key_points.append("👀 **Visual check:** Look for changes in size, shape, skin dimpling, or nipple changes")
            
            if any(word in text for word in ['lying down', 'palpation', 'feel']):
                if 'manual' not in str(key_points).lower():
                    key_points.append("🖐️ **Manual check:** Use finger pads in circular motions while lying down")
            
            if any(word in text for word in ['shower', 'standing', 'armpit']):
                if 'shower' not in str(key_points).lower():
                    key_points.append("🚿 **Standing check:** Repeat examination while standing, include armpit area")
        
        # Add default points if not found
        default_points = [
            "📅 **When to check:** Monthly, 3-5 days after your period ends",
            "👀 **Visual check:** Look for changes in breasts before mirror with arms at sides and raised",
            "🖐️ **Manual check:** Use finger pads in circular motions while lying down - cover entire breast",
            "🚿 **Standing check:** Repeat in shower - wet skin can make examination easier",
            "🎯 **What to look for:** New lumps, thickening, swelling, dimpling, pain, nipple changes"
        ]
        
        if not key_points:
            key_points = default_points[:3]
        
        response = "**🔍 Breast Self-Examination Guide:**\n\n" + "\n\n".join(key_points[:5])
        response += "\n\n**💡 Important:** This complements but doesn't replace clinical exams with healthcare professionals."
        
        return response
    
    def _format_symptoms_response(self, chunks):
        """Format symptoms information"""
        symptoms_found = []
        
        for chunk in chunks:
            text = chunk['text'].lower()
            
            # Extract common symptoms
            if any(word in text for word in ['lump', 'mass']):
                if 'lump' not in str(symptoms_found).lower():
                    symptoms_found.append("• **New lump or mass** - Often painless with irregular edges")
            
            if any(word in text for word in ['swelling', 'thickening']):
                if 'swelling' not in str(symptoms_found).lower():
                    symptoms_found.append("• **Swelling** - Of all or part of the breast")
            
            if any(word in text for word in ['dimpling', 'puckering', 'skin change']):
                if 'skin' not in str(symptoms_found).lower():
                    symptoms_found.append("• **Skin changes** - Dimpling, puckering, redness, or rash")
            
            if any(word in text for word in ['nipple change', 'nipple retraction']):
                if 'nipple' not in str(symptoms_found).lower():
                    symptoms_found.append("• **Nipple changes** - Pain, turning inward, redness, discharge")
            
            if any(word in text for word in ['pain', 'tenderness']):
                if 'pain' not in str(symptoms_found).lower():
                    symptoms_found.append("• **Pain** - In breast or nipple that persists")
        
        # Default symptoms if none found
        if not symptoms_found:
            symptoms_found = [
                "• **New lump or mass** - Often painless with irregular edges",
                "• **Swelling** - Of all or part of the breast",
                "• **Skin changes** - Dimpling, puckering, or redness",
                "• **Nipple changes** - Pain, discharge, or turning inward",
                "• **Pain** - That doesn't go away"
            ]
        
        response = "**🚨 Early Signs to Watch For:**\n\n" + "\n".join(symptoms_found[:6])
        response += "\n\n**⚡ When to see a doctor:** Any new breast change that persists through your menstrual cycle"
        response += "\n\n**💡 Remember:** 80% of breast lumps are NOT cancerous, but always get changes checked"
        
        return response
    
    def _format_prevention_response(self, chunks):
        """Format risk reduction information"""
        prevention_points = []
        
        for chunk in chunks:
            text = chunk['text'].lower()
            
            if any(word in text for word in ['exercise', 'physical activity']):
                if 'exercise' not in str(prevention_points).lower():
                    prevention_points.append("• **Stay active** - 150+ minutes of moderate exercise weekly")
            
            if any(word in text for word in ['weight', 'obesity', 'bmi']):
                if 'weight' not in str(prevention_points).lower():
                    prevention_points.append("• **Maintain healthy weight** - Obesity increases risk")
            
            if any(word in text for word in ['alcohol', 'drink']):
                if 'alcohol' not in str(prevention_points).lower():
                    prevention_points.append("• **Limit alcohol** - 1 drink or less per day")
            
            if any(word in text for word in ['breastfeed', 'breast feeding']):
                if 'breastfeed' not in str(prevention_points).lower():
                    prevention_points.append("• **Breastfeed if possible** - Reduces breast cancer risk")
            
            if any(word in text for word in ['diet', 'nutrition', 'food']):
                if 'diet' not in str(prevention_points).lower():
                    prevention_points.append("• **Healthy diet** - Rich in fruits, vegetables, whole grains")
        
        if not prevention_points:
            prevention_points = [
                "• **Stay active** - Regular exercise reduces risk",
                "• **Maintain healthy weight** - Especially after menopause",
                "• **Limit alcohol** - Each drink increases risk",
                "• **Healthy diet** - Rich in plant-based foods",
                "• **Breastfeed if possible** - Protective effect"
            ]
        
        response = "**🛡️ Ways to Reduce Breast Cancer Risk:**\n\n" + "\n".join(prevention_points[:6])
        response += "\n\n**🌍 For African women:** Know your family history and discuss personalized risk with your doctor"
        
        return response
    
    def _format_screening_response(self, chunks):
        """Format screening information"""
        screening_info = []
        
        for chunk in chunks:
            text = chunk['text'].lower()
            
            if any(word in text for word in ['self exam', 'monthly']):
                if 'self exam' not in str(screening_info).lower():
                    screening_info.append("• **Self-examination:** Monthly, 3-5 days after period ends")
            
            if any(word in text for word in ['clinical', 'cbe', 'health professional']):
                if 'clinical' not in str(screening_info).lower():
                    screening_info.append("• **Clinical exam:** Every 1-3 years (20-39), annually (40+)")
            
            if any(word in text for word in ['mammogram', 'mammography']):
                if 'mammogram' not in str(screening_info).lower():
                    screening_info.append("• **Mammogram:** Start at 40-50, continue based on risk")
            
            if any(word in text for word in ['high risk', 'family history']):
                if 'high risk' not in str(screening_info).lower():
                    screening_info.append("• **High risk:** Earlier screening, consider genetic counseling")
        
        if not screening_info:
            screening_info = [
                "• **Self-examination:** Monthly breast awareness",
                "• **Clinical exam:** Regular checks by healthcare provider",
                "• **Mammogram:** Starting at age 40-50 for average risk",
                "• **High risk:** Earlier and additional screening"
            ]
        
        response = "**📅 Breast Cancer Screening Guidelines:**\n\n" + "\n".join(screening_info)
        response += "\n\n**💡 Important:** Discuss personalized screening schedule with your healthcare provider"
        
        return response
    
    def _format_general_response(self, chunks):
        """Format general responses"""
        # Extract key sentences from top chunks
        key_sentences = []
        used_texts = set()
        
        for chunk in chunks[:3]:  # Use top 3 chunks
            text = chunk['text'].strip()
            # Take first meaningful sentence (avoid very short or header-like text)
            sentences = re.split(r'[.!?]+', text)
            for sentence in sentences:
                clean_sentence = sentence.strip()
                if (len(clean_sentence) > 20 and 
                    len(clean_sentence) < 200 and
                    clean_sentence not in used_texts):
                    key_sentences.append(clean_sentence)
                    used_texts.add(clean_sentence)
                    break
            if len(key_sentences) >= 2:  # Limit to 2 key points
                break
        
        if key_sentences:
            response = "**Based on medical resources:**\n\n" + "\n\n".join(key_sentences)
        else:
            response = "I found some general information about breast health in our resources."
        
        response += "\n\n**💡 Remember:** Consult healthcare professionals for personalized medical advice."
        
        return response
    
    def get_answer(self, question, context_chunks):
        """Generate concise, well-structured answer using the retrieved context"""
        if not context_chunks:
            return "I couldn't find specific information about that in our medical resources. Could you please rephrase your question or ask about breast self-exams, risk factors, symptoms, or screening guidelines?"
        
        # Use smart summarization based on question type
        response = self._summarize_chunks(context_chunks, question)
        
        return response

# Initialize RAG system
def get_rag_system():
    """
    Initialize and return the RAG system.
    Note: In production, cache this globally to avoid reloading PDFs on each request.
    """
    rag = BreastCancerRAG()
    success = rag.load_all_pdfs()
    if success:
        print("✅ RAG system initialized successfully with summarization")
    else:
        print("❌ RAG system initialization failed - no PDFs found")
    return rag