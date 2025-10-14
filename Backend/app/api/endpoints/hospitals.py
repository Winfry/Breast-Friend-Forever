from fastapi import APIRouter, HTTPException
from app.services.data_service import data_service
from app.api.models.schemas import HospitalResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[HospitalResponse])
async def get_hospitals(city: str = None, state: str = None):
    """
    Get breast cancer screening locations
    - **city**: Filter by city name
    - **state**: Filter by state/region
    """
    try:
        hospitals = await data_service.load_hospitals(city, state)
        return hospitals
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="Unable to load hospital data at this time"
        )

@router.get("/search")
async def search_hospitals(query: str):
    """Search hospitals by name, city, or services"""
    try:
        all_hospitals = await data_service.load_hospitals()
        
        # Simple search across multiple fields
        results = [
            hospital for hospital in all_hospitals
            if query.lower() in hospital.get('name', '').lower()
            or query.lower() in hospital.get('city', '').lower()
            or query.lower() in hospital.get('services', '').lower()
        ]
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail="Search failed")