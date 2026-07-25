import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.prescription import Prescription
from app.schemas.prescription import PrescriptionResponse, PrescriptionQuery
from app.services import ocr_service, gemma_service

router = APIRouter()

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=PrescriptionResponse)
async def upload_prescription(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Full pipeline: save image -> OCR (or skip if using gemma_vision) ->
    send to Gemma -> parse structured response -> store in DB.
    """
    if not any(file.filename.lower().endswith(ext) for ext in settings.ALLOWED_EXTENSIONS):
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, or PDF files are supported.")

    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > settings.MAX_UPLOAD_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File too large ({size_mb:.1f}MB). Max is {settings.MAX_UPLOAD_SIZE_MB}MB.",
        )

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(file.filename)[1] or ".jpg"
    saved_filename = f"{uuid.uuid4().hex}{ext}"
    saved_path = os.path.join(settings.UPLOAD_DIR, saved_filename)
    with open(saved_path, "wb") as f:
        f.write(contents)

    record = Prescription(filename=file.filename, status="pending")
    db.add(record)
    db.commit()
    db.refresh(record)

    try:
        if settings.OCR_ENGINE == "gemma_vision":
            gemma_result = await gemma_service.analyze_prescription_image(saved_path)
            record.raw_ocr_text = None
        else:
            ocr_text = ocr_service.extract_text(saved_path)
            record.raw_ocr_text = ocr_text
            gemma_result = await gemma_service.analyze_prescription_text(ocr_text)

        record.gemma_response = gemma_result
        record.has_unclear_sections = bool(gemma_result.get("unclear_sections"))
        record.status = "processed"

    except ocr_service.OCRError as e:
        record.status = "failed"
        record.error_message = f"OCR error: {e}"
    except gemma_service.GemmaError as e:
        record.status = "failed"
        record.error_message = f"Gemma error: {e}"
    except Exception as e:
        record.status = "failed"
        record.error_message = f"Unexpected error: {e}"
    finally:
        db.commit()
        db.refresh(record)

    if record.status == "failed":
        raise HTTPException(status_code=502, detail=record.error_message)

    return record


@router.get("/{prescription_id}", response_model=PrescriptionResponse)
def get_prescription(prescription_id: int, db: Session = Depends(get_db)):
    record = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Prescription not found.")
    return record


@router.get("/", response_model=list[PrescriptionResponse])
def list_prescriptions(db: Session = Depends(get_db)):
    return db.query(Prescription).order_by(Prescription.created_at.desc()).all()


@router.post("/ask")
async def ask_question(query: PrescriptionQuery, db: Session = Depends(get_db)):
    """e.g. 'Which medicine is taken at night?' / 'Which medicine is a syrup?'"""
    record = db.query(Prescription).filter(Prescription.id == query.prescription_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Prescription not found.")
    if not record.gemma_response:
        raise HTTPException(status_code=400, detail="This prescription hasn't been processed yet.")

    try:
        answer = await gemma_service.answer_question(record.gemma_response, query.question)
    except gemma_service.GemmaError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return {"prescription_id": query.prescription_id, "question": query.question, "answer": answer}