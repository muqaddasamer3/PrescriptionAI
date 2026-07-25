from sqlalchemy.orm import Session

from app.models.prescription import Prescription
from app.services.gemma_service import GemmaError, GemmaService
from app.services.ocr_service import OCRError, OCRService
from app.utils.logger import logger


class PrescriptionService:
    @staticmethod
    def process_prescription(image_path: str, db: Session) -> Prescription:
        prescription = Prescription(
            image_path=image_path,
            status="pending",
        )
        db.add(prescription)
        db.commit()
        db.refresh(prescription)

        try:
            extracted_text = OCRService.read(image_path)
            prescription.raw_ocr_text = extracted_text

            gemma_result = GemmaService.explain_prescription(extracted_text)
            prescription.gemma_response = gemma_result
            prescription.explained_text = gemma_result.get("general_notes")
            prescription.has_unclear_sections = bool(gemma_result.get("unclear_sections"))
            prescription.status = "processed"
        except OCRError as exc:
            logger.error("OCR failed: %s", exc)
            prescription.status = "failed"
            prescription.error_message = str(exc)
        except GemmaError as exc:
            logger.error("Gemma failed: %s", exc)
            prescription.status = "failed"
            prescription.error_message = str(exc)
        except Exception as exc:
            logger.exception("Unexpected processing error")
            prescription.status = "failed"
            prescription.error_message = "Unexpected processing error."
        finally:
            db.add(prescription)
            db.commit()
            db.refresh(prescription)

        if prescription.status == "failed":
            raise RuntimeError(prescription.error_message)

        return prescription

    @staticmethod
    def get_prescription(prescription_id: str, db: Session) -> Prescription:
        prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
        if not prescription:
            raise ValueError("Prescription not found.")
        return prescription

    @staticmethod
    def delete_prescription(prescription_id: str, db: Session) -> None:
        prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
        if not prescription:
            raise ValueError("Prescription not found.")
        db.delete(prescription)
        db.commit()
