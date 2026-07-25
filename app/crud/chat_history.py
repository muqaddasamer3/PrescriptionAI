from sqlalchemy.orm import Session

from app.models.chat_history import ChatHistory
from app.schemas.chat_history import ChatHistoryCreate


def create_chat(db: Session, chat: ChatHistoryCreate):
    db_chat = ChatHistory(
        prescription_id=chat.prescription_id,
        question=chat.question,
        answer=chat.answer
    )

    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)

    return db_chat


def get_chat_history(db: Session, prescription_id):
    return (
        db.query(ChatHistory)
        .filter(ChatHistory.prescription_id == prescription_id)
        .all()
    )