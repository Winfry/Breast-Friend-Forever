from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date, timedelta
from typing import Optional

router = APIRouter()

class CycleInput(BaseModel):
    last_period_date: date
    cycle_length_days: int = 28

class ReminderResult(BaseModel):
    best_exam_date: date
    next_period_date: date
    message: str

@router.post("/calculate", response_model=ReminderResult)
async def calculate_reminders(data: CycleInput):
    """
    📅 Calculate the best date for breast self-exam based on menstrual cycle.
    Best time is usually 3-5 days after the period ENDS (approx day 7-10 of cycle).
    """
    try:
        # Calculate next period
        next_period = data.last_period_date + timedelta(days=data.cycle_length_days)
        
        # Best exam date: Day 7 of the cycle (Start of period is Day 1)
        # Assuming period lasts ~5 days, Day 7 is 2 days after it ends.
        best_exam_date = data.last_period_date + timedelta(days=7)
        
        # If the calculated date is in the past, calculate for the NEXT cycle
        today = date.today()
        if best_exam_date < today:
             best_exam_date = next_period + timedelta(days=7)
             next_period = next_period + timedelta(days=data.cycle_length_days)

        return ReminderResult(
            best_exam_date=best_exam_date,
            next_period_date=next_period,
            message=f"Your hormones are most stable around {best_exam_date.strftime('%B %d')}. This is the best time for a self-exam."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
