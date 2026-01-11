from fastapi import APIRouter, Depends
from models.request_models import User, Task, CreateSubtask
from database import Database, get_db
from sqlalchemy.orm import Session
from models.models import Subtask

router = APIRouter(
    prefix = "/create",
    tags = ["create"]
)

@router.post("/user")
async def create_user(user : User):
    db = Database()
    db.connect()
    db.insertUser(user)
    return {"message" : "Inserted user to database successfully !", "status_code" : "200"}


@router.post("/tasks")
async def create_tasks(task : Task):
    db = Database()
    db.connect()
    await db.insertTask(task)
    return {"message" : "Inserted task to database successfully !", "status_code" : "200"}

@router.post("/subtasks")
def create_subtask(payload: dict, db: Session = Depends(get_db)):
    subtask = Subtask(**payload)
    db.add(subtask)
    db.commit()
    db.refresh(subtask)
    return subtask

@router.post("/subtasks/replace")
def replace_subtasks(payload: CreateSubtask, db: Session = Depends(get_db)):
    parent_task_id = payload.parentTaskId
    subtasks = payload.subtasks

    # 1️⃣ Delete existing subtasks
    db.query(Subtask).filter(
        Subtask.task_id == parent_task_id
    ).delete()

    # 2️⃣ Insert new subtasks
    for s in subtasks:
        db.add(Subtask(
            task_id=parent_task_id,
            title=s.title,
            estimate=s.estimate,
            priority=s.priority
        ))

    db.commit()

    return {"status": "ok", "message": "Subtasks replaced"}



