from app.database.session import SessionLocal
from app.models.user import User

db = SessionLocal()

user = User(
    name="Demo User",
    email="demo@example.com"
)

db.add(user)
db.commit()

print("Demo user created!")