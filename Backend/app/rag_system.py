import os
import PyPDF2
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import streamlit as st

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
            st.warning(f"PDF folder not found: {self.pdf_folder}")
            return False
            
        pdf_files = [f for f in os.listdir(self.pdf_folder) if f.endswith('.pdf')]
        
        if not pdf_files:
            st.warning("No PDF files found in the pdfs folder")
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
                            chunks = self._split_text(text, chunk_size=500)  # Increased chunk size
                            for chunk in chunks:
                                self.knowledge_base.append({
                                    'text': chunk,
                                    'source': pdf_file,
                                    'page': page_num + 1
                                })
                print(f"✅ Loaded {pdf_file}")  # Use print instead of st for backend
            except Exception as e:
                print(f"❌ Error loading {pdf_file}: {e}")
        
        # Create embeddings
        if self.knowledge_base:
            texts = [item['text'] for item in self.knowledge_base]
            self.embeddings = self.embedding_model.encode(texts)
            print(f"✅ Created embeddings for {len(self.knowledge_base)} text chunks")
            return True
        return False
    
    def _split_text(self, text, chunk_size=500, overlap=50):
        """Split text into manageable chunks with overlap"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
            
        return chunks
    
    def search(self, question, top_k=5):  # Increased top_k
        """Find most relevant text chunks for a question"""
        if not self.knowledge_base or self.embeddings is None:
            return []
        
        question_embedding = self.embedding_model.encode([question])
        similarities = cosine_similarity(question_embedding, self.embeddings)[0]
        
        # Get top matches
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        results = []
        
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Lowered threshold to get more results
                results.append({
                    'text': self.knowledge_base[idx]['text'],
                    'source': self.knowledge_base[idx]['source'],
                    'page': self.knowledge_base[idx]['page'],
                    'similarity': similarities[idx]
                })
        
        return results
    
    def get_answer(self, question, context_chunks):
        """Generate answer using the retrieved context"""
        if not context_chunks:
            return "I couldn't find specific information about that in our medical resources. Could you please rephrase your question or ask about breast self-exams, risk factors, symptoms, or screening guidelines?"
        
        # Build context string with better formatting
        context_parts = []
        for i, chunk in enumerate(context_chunks[:3]):  # Use top 3 chunks
            context_parts.append(f"{chunk['text']}")
        
        context = "\n\n".join(context_parts)
        
        # Better response template
        response = f"""Based on our medical resources:

{context}

**💡 Remember:** This information is educational. Always consult healthcare professionals for personal medical advice."""

        return response

# Initialize RAG system
@st.cache_resource
def get_rag_system():
    rag = BreastCancerRAG()
    success = rag.load_all_pdfs()
    if success:
        print("✅ RAG system initialized successfully")
    else:
        print("❌ RAG system initialization failed - no PDFs found")
    return rag