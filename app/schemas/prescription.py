from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class PrescriptionBase(BaseModel):
    image_path: str

class PrescriptionCreate(PrescriptionBase):
    user_id: UUID

class PrescriptionResponse(PrescriptionBase):
    id: UUID
    user_id: UUID
    uploaded_at: datetime

    class Config:
        from_attributes = True