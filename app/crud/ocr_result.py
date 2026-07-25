from sqlalchemy.orm import Session
from app.models.ocr_result import OCRResult
from app.schemas.ocr_result import OCRResultCreate

def create_ocr_result(db: Session, ocr: OCRResultCreate):
    db_ocr = OCRResult(
        prescription_id=ocr.prescription_id,
        extracted_text=ocr.extracted_text,
        confidence=ocr.confidence
    )
    db.add(db_ocr)
    db.commit()
    db.refresh(db_ocr)
    return db_ocr

def get_ocr_by_prescription(db: Session, prescription_id: str):
    return db.query(OCRResult).filter(OCRResult.prescription_id == prescription_id).first()