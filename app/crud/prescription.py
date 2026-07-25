from sqlalchemy.orm import Session, joinedload, selectinload
from app.models.prescription import Prescription
from app.models.ocr_result import OCRResult
from app.models.ai_result import AIResult
from app.models.chat_history import ChatHistory
from app.schemas.prescription import PrescriptionCreate

def create_prescription(db: Session, prescription: PrescriptionCreate):
    db_prescription = Prescription(
        user_id=prescription.user_id,
        image_path=prescription.image_path
    )
    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    return db_prescription

def get_prescriptions_by_user(db: Session, user_id: str):
    return db.query(Prescription).filter(Prescription.user_id == user_id).all()

def get_full_prescription(db: Session, prescription_id: str):
    """
    Fetch a single prescription with all related data in ONE optimized query:
    - OCR result
    - AI result
    - Chat history (ordered by creation time)
    """
    return db.query(Prescription).options(
        joinedload(Prescription.user),  # Optional: if you want user details too
        joinedload(Prescription.ocr_result),
        joinedload(Prescription.ai_result),
        joinedload(Prescription.chat_history)
    ).filter(Prescription.id == prescription_id).first()

def get_recent_prescriptions_with_ai(db: Session, user_id: str, limit: int = 10):
    """
    Fetch recent prescriptions with their AI results pre-loaded efficiently.
    """
    return db.query(Prescription).options(
        selectinload(Prescription.ai_result)
    ).filter(
        Prescription.user_id == user_id
    ).order_by(
        Prescription.uploaded_at.desc()
    ).limit(limit).all()