from fastapi import APIRouter

router = APIRouter()

@router.get("/steps")
async def get_self_exam_steps():
    """🖐️ Get breast self-examination steps"""
    return {
        "steps": [
            {
                "id": 1,
                "title": "Visual Inspection", 
                "description": "Stand in front of a mirror with your shoulders straight and your arms on your hips. Look for any changes in size, shape, color, or visible distortion.",
                "icon": "👀",
                "tip": "Look for dimpling, puckering, or changes in skin texture"
            },
            {
                "id": 2,
                "title": "Raise Arms",
                "description": "Raise your arms overhead and look for the same changes.",
                "icon": "🙆",
                "tip": "Check for any fluid coming from the nipples"
            },
            {
                "id": 3,
                "title": "Check for Fluid",
                "description": "While still in front of the mirror, look for any signs of fluid coming out of one or both nipples.",
                "icon": "💧",
                "tip": "Note any discharge that is watery, milky, or yellow fluid, or blood"
            },
            {
                "id": 4,
                "title": "Lying Down Position",
                "description": "Lie down and feel your breasts using a firm, smooth touch. Keep fingers flat and together, use a circular motion about the size of a quarter.",
                "icon": "🛌",
                "tip": "Use the pads of your fingers, not the tips"
            },
            {
                "id": 5,
                "title": "Cover Entire Breast",
                "description": "Cover the entire breast from top to bottom, side to side — from your collarbone to the top of your abdomen, and from your armpit to your cleavage.",
                "icon": "🔄",
                "tip": "Follow a pattern to ensure you cover the whole breast"
            },
            {
                "id": 6,
                "title": "Repeat in Shower",
                "description": "Repeat the same steps while standing or sitting in the shower. Soapy hands make it easier to feel the breast tissue.",
                "icon": "🚿",
                "tip": "Many women find this the easiest way to perform the exam"
            }
        ]
    }