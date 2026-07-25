from uuid import UUID
from pydantic import BaseModel


class OCRResultCreate(BaseModel):
    prescription_id: UUID
    extracted_text: str
    confidence: float


class OCRResultResponse(BaseModel):
    id: UUID
    prescription_id: UUID
    extracted_text: str
    confidence: float

    model_config = {
        "from_attributes": True
    }