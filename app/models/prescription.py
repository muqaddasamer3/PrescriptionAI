from typing import TYPE_CHECKING
from sqlalchemy import Column, String, DateTime, ForeignKey, Index, func, text
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.database.base import Base
import uuid
from uuid import UUID

if TYPE_CHECKING:
    from .user import User
    from .ocr_result import OCRResult
    from .ai_result import AIResult
    from .chat_history import ChatHistory

class Prescription(Base):
    __tablename__ = "prescriptions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    image_path: Mapped[str] = mapped_column(String, nullable=False)
    uploaded_at: Mapped[DateTime] = mapped_column(DateTime, server_default=text('NOW()'), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="prescriptions")
    ocr_result: Mapped["OCRResult"] = relationship(
        "OCRResult", back_populates="prescription", uselist=False, cascade="all, delete-orphan"
    )
    ai_result: Mapped["AIResult"] = relationship(
        "AIResult", back_populates="prescription", uselist=False, cascade="all, delete-orphan"
    )
    chat_history: Mapped[list["ChatHistory"]] = relationship(
        "ChatHistory", back_populates="prescription", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_prescription_user_id", "user_id"),
        Index("idx_prescription_uploaded_at", "uploaded_at"),
    )