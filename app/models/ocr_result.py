from typing import TYPE_CHECKING
from sqlalchemy import Column, String, Float, ForeignKey, Index
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.database.base import Base
import uuid
from uuid import UUID

if TYPE_CHECKING:
    from .prescription import Prescription

class OCRResult(Base):
    __tablename__ = "ocr_results"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    prescription_id: Mapped[UUID] = mapped_column(ForeignKey("prescriptions.id", ondelete="CASCADE"), nullable=False, unique=True)
    extracted_text: Mapped[str] = mapped_column(String, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)

    # Relationships
    prescription: Mapped["Prescription"] = relationship("Prescription", back_populates="ocr_result")

    __table_args__ = (
        Index("idx_ocr_prescription_id", "prescription_id"),
    )