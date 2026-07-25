from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict

class AIResultBase(BaseModel):
    medicine_names: Optional[List[str]] = None
    abbreviations: Optional[Dict[str, str]] = None
    roman_urdu: Optional[str] = None
    medication_schedule: Optional[Dict[str, str]] = None
    unreadable_sections: Optional[List[str]] = None

class AIResultCreate(AIResultBase):
    prescription_id: UUID

class AIResultResponse(AIResultBase):
    id: UUID
    prescription_id: UUID
    generated_at: datetime

    class Config:
        from_attributes = True