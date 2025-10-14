from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.services.data_service import data_service
from app.api.models.schemas import ArticleResponse, PDFResource
from typing import List, Dict, Any

router = APIRouter()

@router.get("/", response_model=Dict[str, Any])
async def get_all_resources():
    """Get all educational resources (articles, PDFs, links)"""
    try:
        return await data_service.load_resources()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error loading resources")

@router.get("/articles", response_model=List[ArticleResponse])
async def get_articles(category: str = None):
    """Get educational articles, optionally filtered by category"""
    try:
        resources = await data_service.load_resources()
        articles = resources.get("articles", [])
        
        if category and category != "all":
            articles = [article for article in articles if article.get("category") == category]
        
        return articles
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error loading articles")

@router.get("/articles/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: int):
    """Get a specific article by ID"""
    try:
        resources = await data_service.load_resources()
        articles = resources.get("articles", [])
        
        article = next((a for a in articles if a["id"] == article_id), None)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        return article
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error loading article")

@router.get("/pdfs", response_model=List[PDFResource])
async def get_pdfs():
    """Get list of available PDF resources"""
    try:
        resources = await data_service.load_resources()
        return resources.get("pdfs", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error loading PDFs")

@router.get("/pdfs/{filename}")
async def download_pdf(filename: str):
    """Download a PDF resource file"""
    try:
        pdf_path = await data_service.get_pdf_path(filename)
        return FileResponse(
            pdf_path,
            media_type='application/pdf',
            filename=filename
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="PDF not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error downloading PDF")

@router.get("/categories")
async def get_categories():
    """Get all available resource categories"""
    try:
        resources = await data_service.load_resources()
        articles = resources.get("articles", [])
        
        categories = list(set(article.get("category", "general") for article in articles))
        return sorted(categories)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error loading categories")