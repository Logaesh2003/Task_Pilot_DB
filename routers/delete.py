from fastapi import APIRouter
from .request_models import DeleteTask, DeleteSubtask
from database import Database

router = APIRouter(
    prefix = "/delete",
    tags = ["delete"]
)

@router.post("/task")
async def deleteTask(payload : DeleteTask):
    db = Database()
    db.connect()
    task_id = payload.task_id
    result = db.deleteTask(task_id)
    return result

@router.post("/subtask")
async def deleteSubTask(payload : DeleteSubtask):
    db = Database()
    db.connect()
    task_id = payload.id
    result = db.deleteSubtask(task_id)
    return result