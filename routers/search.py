from fastapi import APIRouter, Depends
from .request_models import User, Task, FetchTask, DeleteTask
from database import Database, get_db
import logging 
from sqlalchemy.orm import Session
from .models import Task, Subtask

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix = "/search",
    tags = ["search"]
)

@router.get("/user")
def searchUser(user : User):
    db = Database()
    db.connect()
    user_id = db.searchUser()
    return {"user_id" : user_id}

@router.post("/userTasks")
def searchUserTasks(payload : FetchTask):
    db = Database()
    db.connect()
    user_id = payload.user_id
    tasks = db.searchUserTasks(user_id)
    logger.info(f"Tasks : {tasks}")
    return { "tasks" : tasks }

@router.post("/task")
def searchTask(payload : DeleteTask):
    db = Database()
    db.connect()
    task_id = payload.task_id
    task = db.searchTask(task_id)
    logger.info(f"Task : {task}")
    return { "task" : task }


@router.get("/tasks/{task_id}/subtasks")
def get_subtasks(task_id: int, db: Session = Depends(get_db)):
    subtasks = (
        db.query(Subtask)
        .filter(Subtask.task_id == task_id)
        .order_by(Subtask.id.asc())
        .all()
    )

    return [
        {
            "id": s.id,
            "task_id": s.task_id,
            "title": s.title,
            "estimate": s.estimate,
            "priority": s.priority,
            "completed": s.completed,
            "source": s.source,
            "confidence": s.confidence
        }
        for s in subtasks
    ]