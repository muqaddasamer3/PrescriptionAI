from pydantic import BaseModel
from uuid import UUID

class OCRResultBase(BaseModel):
    extracted_text: str
    confidence: float

class OCRResultCreate(OCRResultBase):
    prescription_id: UUID

class OCRResultResponse(OCRResultBase):
    id: UUID
    prescription_id: UUID

    class Config:
        from_attributes = True