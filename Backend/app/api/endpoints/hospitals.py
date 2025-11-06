from fastapi import APIRouter, HTTPException
from app.services.data_service import data_service
from app.api.models.schemas import HospitalResponse
from typing import List

router = APIRouter()

@router.get("/")
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
        print(f"[ERROR] Hospitals endpoint error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail="Unable to load hospital data at this time"
        )