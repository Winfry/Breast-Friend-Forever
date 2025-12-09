from fastapi import APIRouter, HTTPException
from app.services.expert_system_service import expert_system, SymptomInput, AnalysisResult

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResult)
async def analyze_symptoms(data: SymptomInput):
    """
    🔍 Analyze breast health symptoms using the Expert System.
    Returns a risk assessment and educational guidance.
    """
    try:
        result = expert_system.analyze(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/options")
async def get_symptom_options():
    """
    📋 Get list of common symptoms for the frontend UI.
    """
    return {
        "lumps": ["Hard lump", "Soft lump", "Movable lump", "Fixed lump", "No lump"],
        "skin": ["Redness", "Dimpling", "Orange peel skin", "Rash", "Normal"],
        "nipple": ["Inverted nipple", "Bloody discharge", "Clear discharge", "Crusting", "Normal"],
        "pain": ["Constant pain", "Cyclical pain (comes/goes)", "No pain"]
    }
