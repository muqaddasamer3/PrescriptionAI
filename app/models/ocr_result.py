import uuid

from sqlalchemy import Float, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class OCRResult(Base):
    __tablename__ = "ocr_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    prescription_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("prescriptions.id"),
        unique=True
    )

    extracted_text: Mapped[str] = mapped_column(Text)

    confidence: Mapped[float] = mapped_column(Float)

    prescription = relationship(
        "Prescription",
        back_populates="ocr_result"
    )