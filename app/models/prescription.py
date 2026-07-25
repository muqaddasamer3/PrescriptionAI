import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Prescription(Base):
    __tablename__ = "prescriptions"

    # Primary Key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # Foreign Key to Users table
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    # Path of uploaded prescription image
    image_path: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # Upload timestamp
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # -------------------------
    # Relationships
    # -------------------------

    # Many Prescriptions -> One User
    user = relationship(
        "User",
        back_populates="prescriptions"
    )

    # One Prescription -> One OCR Result
    ocr_result = relationship(
        "OCRResult",
        back_populates="prescription",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # One Prescription -> One AI Result
    ai_result = relationship(
        "AIResult",
        back_populates="prescription",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # One Prescription -> Many Chat Messages
    chat_history = relationship(
        "ChatHistory",
        back_populates="prescription",
        cascade="all, delete-orphan"
    )