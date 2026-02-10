# routers/users.py
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import User
from database import get_db
from helpers.security import verify_password, hash_password

router = APIRouter(prefix="/users", tags=["users"])

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

    class Config:
        from_attributes = True 

@router.post("")
def create_user(payload: dict, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload["email"]).first():
        raise HTTPException(400, "Email already registered")

    user = User(
        email=payload["email"],
        name=payload["name"],
        password=hash_password(payload["password"])
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/by-email/{email}")
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(404, "User not found")
    return user

