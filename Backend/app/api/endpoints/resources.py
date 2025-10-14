from fastapi import APIRouter, HTTPException
from app.services.data_service import data_service
from typing import Dict, Any

router = APIRouter()

@router.get("/", response_model=Dict[str, Any])
async def get_all_resources():
    try:
        return await data_service.load_resources()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error loading resources")