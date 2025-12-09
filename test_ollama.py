from langchain_ollama import ChatOllama
import sys

def test_ollama():
    print("Testing Ollama connection...")
    try:
        llm = ChatOllama(model="llama3.2:latest", temperature=0.3)
        print("Invoking model...")
        response = llm.invoke("Hi, are you working?")
        print(f"Success! Response: {response.content}")
    except Exception as e:
        print(f"Error: {e}")
        print("\nPossible causes:")
        print("1. Ollama is not installed.")
        print("2. Ollama is not running.")
        print("3. The model 'llama3.2:latest' is not pulled.")

if __name__ == "__main__":
    test_ollama()
