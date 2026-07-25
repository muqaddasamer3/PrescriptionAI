from datetime import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String, Text

from app.core.database import Base


class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    raw_ocr_text = Column(Text, nullable=True)
    gemma_response = Column(JSON, nullable=True)  # structured output: medicines, schedule, warnings
    has_unclear_sections = Column(Boolean, default=False)
    status = Column(String(20), default="pending")  # pending | processed | failed
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)