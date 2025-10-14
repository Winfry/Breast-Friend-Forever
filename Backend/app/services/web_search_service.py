# BACKEND/app/services/web_search_service.py
import asyncio
import httpx
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import json
from typing import List, Dict
import re

class WebSearchService:
    """Service to fetch real-time breast health information from the web"""
    
    def __init__(self):
        self.trusted_sources = [
            "who.int", "cdc.gov", "mayoclinic.org", "cancer.org",
            "breastcancer.org", "nhs.uk", "webmd.com", "healthline.com",
            "medicalnewstoday.com", "hopkinsmedicine.org"
        ]
    
    async def search_breast_health_info(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search for breast health information from trusted medical sources"""
        
        # Enhance query with medical context
        enhanced_query = f"breast health {query} medical information 2024"
        
        try:
            # Use DuckDuckGo Search
            search_results = await self._duckduckgo_search(enhanced_query, max_results)
            
            # Filter and rank results
            filtered_results = self._filter_trusted_sources(search_results)
            
            # Fetch content from top results
            detailed_results = []
            for result in filtered_results[:3]:  # Limit to top 3 for performance
                content = await self._extract_page_content(result['url'])
                if content:
                    detailed_results.append({
                        'title': result['title'],
                        'url': result['url'],
                        'content': content[:500] + "..." if len(content) > 500 else content,
                        'source': self._extract_domain(result['url'])
                    })
            
            return detailed_results
            
        except Exception as e:
            print(f"Web search error: {e}")
            return []
    
    async def _duckduckgo_search(self, query: str, max_results: int) -> List[Dict]:
        """Perform DuckDuckGo search"""
        try:
            results = []
            with DDGS() as ddgs:
                for result in ddgs.text(query, max_results=max_results):
                    results.append({
                        'title': result['title'],
                        'url': result['href']
                    })
            return results
        except Exception as e:
            print(f"DuckDuckGo search error: {e}")
            return []
    
    def _filter_trusted_sources(self, results: List[Dict]) -> List[Dict]:
        """Filter results to only trusted medical sources"""
        trusted_results = []
        for result in results:
            if any(source in result['url'].lower() for source in self.trusted_sources):
                trusted_results.append(result)
        return trusted_results or results  # Return all if no trusted sources found
    
    async def _extract_page_content(self, url: str) -> str:
        """Extract main content from webpage"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Get text and clean it
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                return text[:1000]  # Limit content length
                
        except Exception as e:
            print(f"Content extraction error for {url}: {e}")
            return ""
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain name from URL"""
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        return domain.replace("www.", "")

# Create global instance
web_search_service = WebSearchService()