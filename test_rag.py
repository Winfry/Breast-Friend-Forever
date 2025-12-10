import sys
import os

# Add Backend/app to path
sys.path.append(os.path.join(os.getcwd(), 'Backend', 'app'))

try:
    from rag_system import get_rag_system
    
    print("1. Initializing RAG System...")
    rag = get_rag_system()
    print("   ✅ RAG Initialized")
    
    print("\n2. Testing Search...")
    query = "What are early signs of breast cancer?"
    chunks = rag.search(query)
    print(f"   Found {len(chunks)} chunks")
    
    if chunks:
        print("\n3. Testing Answer Generation (LLM)...")
        answer = rag.get_answer(query, chunks)
        print("\n--- ANSWER ---")
        print(answer)
        print("--------------")
    else:
        print("   ❌ No chunks found!")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
