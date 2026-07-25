from typing import TYPE_CHECKING
from sqlalchemy import Column, String, DateTime, ForeignKey, Index, func
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.database.base import Base
import uuid
from uuid import UUID

if TYPE_CHECKING:
    from .prescription import Prescription

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    prescription_id: Mapped[UUID] = mapped_column(ForeignKey("prescriptions.id", ondelete="CASCADE"), nullable=False)
    question: Mapped[str] = mapped_column(String, nullable=False)
    answer: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    prescription: Mapped["Prescription"] = relationship("Prescription", back_populates="chat_history")

    __table_args__ = (
        Index("idx_chat_prescription_id", "prescription_id"),
        Index("idx_chat_created_at", "created_at"),
    )