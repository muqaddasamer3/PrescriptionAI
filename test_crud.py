from app.database.session import SessionLocal
from app.crud.user import create_user, get_user_by_email
from app.schemas.user import UserCreate

db = SessionLocal()

try:
    # Use a unique email each time
    user_data = UserCreate(name="Test Doctor", email="doctor_test_unique@example.com")
    new_user = create_user(db, user_data)
    print(f"✅ Created user: {new_user.id}")

    # Test fetch
    fetched = get_user_by_email(db, "doctor_test_unique@example.com")
    print(f"✅ Fetched user: {fetched.name}")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    db.close()