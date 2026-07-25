from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ChatHistoryCreate(BaseModel):
    prescription_id: UUID
    question: str
    answer: str


class ChatHistoryResponse(BaseModel):
    id: UUID
    prescription_id: UUID
    question: str
    answer: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }