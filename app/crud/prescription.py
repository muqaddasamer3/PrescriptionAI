from sqlalchemy.orm import Session

from app.models.prescription import Prescription
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


def get_prescription(db: Session, prescription_id):
    return (
        db.query(Prescription)
        .filter(Prescription.id == prescription_id)
        .first()
    )


def get_user_prescriptions(db: Session, user_id):
    return (
        db.query(Prescription)
        .filter(Prescription.user_id == user_id)
        .all()
    )