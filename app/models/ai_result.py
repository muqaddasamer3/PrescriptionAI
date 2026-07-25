from typing import TYPE_CHECKING
from sqlalchemy import Column, String, DateTime, ForeignKey, Index, func, JSON
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.database.base import Base
import uuid
from uuid import UUID

if TYPE_CHECKING:
    from .prescription import Prescription

class AIResult(Base):
    __tablename__ = "ai_results"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    prescription_id: Mapped[UUID] = mapped_column(ForeignKey("prescriptions.id", ondelete="CASCADE"), nullable=False, unique=True)
    medicine_names: Mapped[list] = mapped_column(JSON, nullable=True)
    abbreviations: Mapped[dict] = mapped_column(JSON, nullable=True)
    roman_urdu: Mapped[str] = mapped_column(String, nullable=True)
    medication_schedule: Mapped[dict] = mapped_column(JSON, nullable=True)
    unreadable_sections: Mapped[list] = mapped_column(JSON, nullable=True)
    generated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    prescription: Mapped["Prescription"] = relationship("Prescription", back_populates="ai_result")

    __table_args__ = (
        Index("idx_ai_prescription_id", "prescription_id"),
    )