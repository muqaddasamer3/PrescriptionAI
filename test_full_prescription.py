from app.database.session import SessionLocal
from app.crud.user import create_user, get_user_by_email
from app.crud.prescription import create_prescription, get_full_prescription, get_recent_prescriptions_with_ai
from app.crud.ai_result import create_ai_result
from app.crud.ocr_result import create_ocr_result
from app.schemas.user import UserCreate
from app.schemas.prescription import PrescriptionCreate
from app.schemas.ocr_result import OCRResultCreate
from app.schemas.ai_result import AIResultCreate

db = SessionLocal()

try:
    # 1. Create a user
    user = create_user(db, UserCreate(name="Doctor", email="doc@test.com"))
    print(f"✅ User created: {user.id}")

    # 2. Create a prescription
    prescription = create_prescription(db, PrescriptionCreate(
        user_id=user.id,
        image_path="test.jpg"
    ))
    print(f"✅ Prescription created: {prescription.id}")

    # 3. Add OCR result
    ocr = create_ocr_result(db, OCRResultCreate(
        prescription_id=prescription.id,
        extracted_text="Panadol 500mg BD",
        confidence=0.95
    ))
    print(f"✅ OCR created: {ocr.id}")

    # 4. Add AI result
    ai = create_ai_result(db, AIResultCreate(
        prescription_id=prescription.id,
        medicine_names=["Panadol 500mg"],
        abbreviations={"BD": "Twice daily"},
        roman_urdu="Panadol 500mg din mein do baar",
        medication_schedule={"morning": "Panadol", "night": "Panadol"},
        unreadable_sections=[]
    ))
    print(f"✅ AI Result created: {ai.id}")

    # 5. Fetch full prescription (JOIN)
    full = get_full_prescription(db, prescription.id)
    print("\n✅ Full prescription loaded:")
    if full:
        print(f"  - User: {full.user.name}")
        print(f"  - OCR Text: {full.ocr_result.extracted_text}")
        print(f"  - Medicine Names: {full.ai_result.medicine_names}")
        print(f"  - Schedule: {full.ai_result.medication_schedule}")

    # 6. Fetch recent list
    recent = get_recent_prescriptions_with_ai(db, user.id)
    print(f"\n✅ Recent prescriptions count: {len(recent)}")
    for p in recent:
        print(f"  - {p.image_path} -> {p.ai_result.medicine_names if p.ai_result else 'No AI'}")

except Exception as e:
    print(f"❌ Error: {e}")
finally:
    db.close()