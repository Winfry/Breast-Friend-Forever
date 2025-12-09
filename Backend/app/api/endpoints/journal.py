from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

router = APIRouter()

# In-memory database for MVP (Replace with SQLite/Postgres later)
journal_db = []

class JournalEntry(BaseModel):
    id: Optional[str] = None
    date: str  # YYYY-MM-DD
    symptoms: List[str]
    notes: str
    mood: str

@router.get("/", response_model=List[JournalEntry])
async def get_entries():
    """📖 Get all journal entries"""
    return sorted(journal_db, key=lambda x: x.date, reverse=True)

@router.post("/", response_model=JournalEntry)
async def add_entry(entry: JournalEntry):
    """✍️ Add a new journal entry"""
    entry.id = str(uuid.uuid4())
    journal_db.append(entry)
    return entry

@router.delete("/{entry_id}")
async def delete_entry(entry_id: str):
    """🗑️ Delete a journal entry"""
    global journal_db
    journal_db = [e for e in journal_db if e.id != entry_id]
    return {"message": "Entry deleted"}
