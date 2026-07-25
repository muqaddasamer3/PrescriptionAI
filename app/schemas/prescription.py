from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PrescriptionCreate(BaseModel):
    user_id: UUID
    image_path: str


class PrescriptionResponse(BaseModel):
    id: UUID
    user_id: UUID
    image_path: str
    uploaded_at: datetime

    model_config = {
        "from_attributes": True
    }