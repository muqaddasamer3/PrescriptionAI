from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class MedicineItem(BaseModel):
    name: str
    dosage_instruction_raw: Optional[str] = None  # e.g. "1+0+1"
    frequency_explained: Optional[str] = None      # e.g. "Twice a day (BD)"
    timing_note: Optional[str] = None               # e.g. "After meals"
    form: Optional[str] = None                      # tablet / syrup / injection
    confidence: Optional[str] = None                 # "clear" | "unclear"


class GemmaStructuredResponse(BaseModel):
    medicines: list[MedicineItem] = []
    general_notes: Optional[str] = None
    unclear_sections: list[str] = []
    disclaimer: str = (
        "This explains what appears to be written on your prescription. "
        "It is not medical advice — please confirm with your doctor or pharmacist."
    )


class PrescriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    raw_ocr_text: Optional[str] = None
    gemma_response: Optional[dict[str, Any]] = None
    has_unclear_sections: bool
    status: str
    error_message: Optional[str] = None
    created_at: datetime


class PrescriptionQuery(BaseModel):
    prescription_id: int
    question: str  # e.g. "Which medicine is taken at night?"