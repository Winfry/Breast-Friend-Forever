from fastapi import APIRouter, HTTPException
from app.services.data_service import data_service
from app.api.models.schemas import HospitalResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[HospitalResponse])
async def get_hospitals(city: str = None, state: str = None):
    try:
        hospitals = await data_service.load_hospitals(city, state)
        return hospitals
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unable to load hospital data")