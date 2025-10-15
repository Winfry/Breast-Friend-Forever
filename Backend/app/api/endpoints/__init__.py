from fastapi import APIRouter

router = APIRouter()

@router.get("/steps")
async def get_steps():
    return {"steps": "coming soon"}
