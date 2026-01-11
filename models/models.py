from sqlalchemy import (
    Column, Integer, String, Boolean, Date, Float, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    priority = Column(String)
    due_date = Column(Date)
    completed = Column(Boolean, default=False)


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
