from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AIResultCreate(BaseModel):
    prescription_id: UUID
    medicine_names: list
    abbreviations: dict
    roman_urdu: dict
    medication_schedule: dict
    unreadable_sections: list


class AIResultResponse(BaseModel):
    id: UUID
    prescription_id: UUID
    medicine_names: list
    abbreviations: dict
    roman_urdu: dict
    medication_schedule: dict
    unreadable_sections: list
    generated_at: datetime

    model_config = {
        "from_attributes": True
    }