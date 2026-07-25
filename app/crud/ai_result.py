from sqlalchemy.orm import Session
from app.models.ai_result import AIResult
from app.schemas.ai_result import AIResultCreate

def create_ai_result(db: Session, ai: AIResultCreate):
    db_ai = AIResult(
        prescription_id=ai.prescription_id,
        medicine_names=ai.medicine_names,
        abbreviations=ai.abbreviations,
        roman_urdu=ai.roman_urdu,
        medication_schedule=ai.medication_schedule,
        unreadable_sections=ai.unreadable_sections
    )
    db.add(db_ai)
    db.commit()
    db.refresh(db_ai)
    return db_ai

def get_ai_by_prescription(db: Session, prescription_id: str):
    return db.query(AIResult).filter(AIResult.prescription_id == prescription_id).first()