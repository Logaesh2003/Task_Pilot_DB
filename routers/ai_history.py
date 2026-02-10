from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from helpers import ai_history_helper

router = APIRouter(prefix="/ai-history", tags=["AI History"])


@router.post("/")
def save_ai_history(payload: dict, db: Session = Depends(get_db)):
    return ai_history_helper.save(
        db=db,
        user_id=payload["user_id"],
        prompt=payload["prompt"],
        response=payload["response"]
    )


@router.get("/{user_id}")
def get_recent_ai_history(user_id: int, limit: int = 5, db: Session = Depends(get_db)):
    history = ai_history_helper.get_recent(db, user_id, limit)
    return [
        {
            "prompt": h.prompt,
            "response": h.response,
            "created_at": h.created_at
        }
        for h in history
    ]
