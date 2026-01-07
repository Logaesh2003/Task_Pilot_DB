from fastapi import APIRouter
from .request_models import UpdateTask, ToggleTask
from database import Database
import logging 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix = "/update",
    tags = ["update"]
)

@router.put("/task")
def updateTask(task : UpdateTask):
    logger.info(task)
    db = Database()
    db.connect()
    result = db.updateTask(task)
    return result

@router.put("/toggleTask")
def toggleTask(task : ToggleTask):
    logger.info(task)
    db = Database()
    db.connect()
    result = db.toggleTask(task)
    return result

@router.put("/toggleSubtask")
def toggleTask(task : ToggleTask):
    logger.info(task)
    db = Database()
    db.connect()
    result = db.toggleSubtask(task)
    return result