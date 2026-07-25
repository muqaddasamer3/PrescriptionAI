from sqlalchemy.orm import Session

from app.models.ocr_result import OCRResult
from app.schemas.ocr_result import OCRResultCreate


def create_ocr_result(db: Session, result: OCRResultCreate):
    db_result = OCRResult(
        prescription_id=result.prescription_id,
        extracted_text=result.extracted_text,
        confidence=result.confidence
    )

    db.add(db_result)
    db.commit()
    db.refresh(db_result)

    return db_result


def get_ocr_result(db: Session, prescription_id):
    return (
        db.query(OCRResult)
        .filter(OCRResult.prescription_id == prescription_id)
        .first()
    )