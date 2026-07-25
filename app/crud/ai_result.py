from sqlalchemy.orm import Session

from app.models.ai_result import AIResult
from app.schemas.ai_result import AIResultCreate


def create_ai_result(db: Session, result: AIResultCreate):
    db_result = AIResult(
        prescription_id=result.prescription_id,
        medicine_names=result.medicine_names,
        abbreviations=result.abbreviations,
        roman_urdu=result.roman_urdu,
        medication_schedule=result.medication_schedule,
        unreadable_sections=result.unreadable_sections,
    )

    db.add(db_result)
    db.commit()
    db.refresh(db_result)

    return db_result


def get_ai_result(db: Session, prescription_id):
    return (
        db.query(AIResult)
        .filter(AIResult.prescription_id == prescription_id)
        .first()
    )