from sqlalchemy import (
    Column, Integer, String, Boolean, Date, Float, ForeignKey, Text, DateTime
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    priority = Column(String)
    due_date = Column(Date)
    done = Column(Boolean, default=False)


class Subtask(Base):
    __tablename__ = "subtasks"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"))
    title = Column(String, nullable=False)
    estimate = Column(String)
    priority = Column(String)
    completed = Column(Boolean, default=False)
    source = Column(String, default="ai")
    confidence = Column(Float)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)


class AIHistory(Base):
    __tablename__ = "ai_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)

    prompt = Column(Text, nullable=False)
    response = Column(JSONB, nullable=False)


    created_at = Column(DateTime(timezone=True), server_default=func.now())
