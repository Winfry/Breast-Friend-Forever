import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings - centralized configuration"""
    
    # 🏷️ App Metadata
    PROJECT_NAME: str = "Breast Friend Forever"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 🔑 API Keys (from environment variables)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # 📁 Data File Paths
    HOSPITALS_CSV: str = "app/data/hospitals.csv"
    RESOURCES_JSON: str = "app/data/resources.json" 
    ENCOURAGEMENT_JSON: str = "app/data/encouragement.json"
    PDF_STORAGE_PATH: str = "app/data/pdfs/"
    
    # ⚙️ Chatbot Settings
    CHATBOT_MODEL: str = "gpt-3.5-turbo"
    CHATBOT_TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 500
    
    # 🔒 Security (for future enhancements)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "breast-friend-forever-secret-key")
    ALGORITHM: str = "HS256"

# Create global settings instance
settings = Settings()