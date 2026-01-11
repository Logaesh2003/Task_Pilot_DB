from sqlalchemy.orm import Session
from models.ai_history import AIHistory


def save(db: Session, user_id: int, prompt: str, response: str):
    record = AIHistory(
        user_id=user_id,
        prompt=prompt,
        response=response
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_recent(db: Session, user_id: int, limit: int = 5):
    return (
        db.query(AIHistory)
        .filter(AIHistory.user_id == user_id)
        .order_by(AIHistory.created_at.desc())
        .limit(limit)
        .all()
    )
