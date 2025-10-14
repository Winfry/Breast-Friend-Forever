import pandas as pd
import json
import aiofiles
import os
from typing import List, Dict, Any

class DataService:
    """📂 Service for reading/writing data files"""
    
    async def load_hospitals(self, city: str = None, state: str = None) -> List[Dict]:
        """🏥 Load hospitals from CSV, optionally filter by city/state"""
        try:
            df = pd.read_csv("app/data/hospitals.csv")
            
            # 🔍 Filter if city/state provided
            if city:
                df = df[df['city'].str.contains(city, case=False, na=False)]
            if state:
                df = df[df['state'].str.contains(state, case=False, na=False)]
            
            return df.to_dict('records')
        except Exception as e:
            print(f"❌ Error loading hospitals: {e}")
            return []  # Return empty list instead of crashing

    async def load_resources(self) -> Dict[str, Any]:
        """📚 Load educational resources from JSON"""
        try:
            async with aiofiles.open("app/data/resources.json", 'r', encoding='utf-8') as f:
                content = await f.read()
                return json.loads(content)
        except Exception as e:
            print(f"❌ Error loading resources: {e}")
            return {"articles": [], "pdfs": [], "external_links": []}

    async def load_encouragement(self) -> List[Dict]:
        """💖 Load encouragement messages from JSON"""
        try:
            async with aiofiles.open("app/data/encouragement.json", 'r', encoding='utf-8') as f:
                content = await f.read()
                return json.loads(content)
        except Exception as e:
            print(f"❌ Error loading encouragement: {e}")
            return []

    async def save_encouragement(self, messages: List[Dict]) -> bool:
        """💾 Save encouragement messages to JSON"""
        try:
            async with aiofiles.open("app/data/encouragement.json", 'w', encoding='utf-8') as f:
                await f.write(json.dumps(messages, indent=2, ensure_ascii=False))
            return True
        except Exception as e:
            print(f"❌ Error saving encouragement: {e}")
            return False

# 🎯 Create a global instance
data_service = DataService()