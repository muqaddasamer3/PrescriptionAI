from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ChatHistoryBase(BaseModel):
    question: str
    answer: str

class ChatHistoryCreate(ChatHistoryBase):
    prescription_id: UUID

class ChatHistoryResponse(ChatHistoryBase):
    id: UUID
    prescription_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True