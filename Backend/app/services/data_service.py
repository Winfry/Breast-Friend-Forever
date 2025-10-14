import pandas as pd
import json
import aiofiles
import os
from typing import List, Dict, Any
from app.core.config import settings

class DataService:
    """Service for handling data file operations"""
    
    async def load_hospitals(self, city: str = None, state: str = None) -> List[Dict]:
        """Load hospitals from CSV with optional filtering"""
        try:
            df = pd.read_csv(settings.HOSPITALS_CSV)
            
            # Apply filters if provided
            if city:
                df = df[df['city'].str.contains(city, case=False, na=False)]
            if state:
                df = df[df['state'].str.contains(state, case=False, na=False)]
            
            return df.to_dict('records')
        except Exception as e:
            print(f"Error loading hospitals: {e}")
            return []
    
    async def load_resources(self) -> Dict[str, Any]:
        """Load all resources from JSON file"""
        try:
            async with aiofiles.open(settings.RESOURCES_JSON, 'r', encoding='utf-8') as f:
                content = await f.read()
                return json.loads(content)
        except Exception as e:
            print(f"Error loading resources: {e}")
            return {"articles": [], "pdfs": [], "external_links": []}
    
    async def load_encouragement(self) -> List[Dict]:
        """Load encouragement messages from JSON"""
        try:
            async with aiofiles.open(settings.ENCOURAGEMENT_JSON, 'r', encoding='utf-8') as f:
                content = await f.read()
                return json.loads(content)
        except Exception as e:
            print(f"Error loading encouragement: {e}")
            return []
    
    async def save_encouragement(self, messages: List[Dict]) -> bool:
        """Save encouragement messages to JSON"""
        try:
            async with aiofiles.open(settings.ENCOURAGEMENT_JSON, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(messages, indent=2, ensure_ascii=False))
            return True
        except Exception as e:
            print(f"Error saving encouragement: {e}")
            return False
    
    async def get_pdf_path(self, filename: str) -> str:
        """Get full path to PDF file"""
        pdf_path = os.path.join(settings.PDF_STORAGE_PATH, filename)
        if os.path.exists(pdf_path):
            return pdf_path
        raise FileNotFoundError(f"PDF not found: {filename}")

# Create global instance
data_service = DataService()