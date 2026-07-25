import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class AIResult(Base):
    __tablename__ = "ai_results"

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

    medicine_names: Mapped[list] = mapped_column(JSON)

    abbreviations: Mapped[dict] = mapped_column(JSON)

    roman_urdu: Mapped[str] = mapped_column(JSON)

    medication_schedule: Mapped[dict] = mapped_column(JSON)

    unreadable_sections: Mapped[list] = mapped_column(JSON)

    generated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    prescription = relationship(
        "Prescription",
        back_populates="ai_result"
    )