from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class User(BaseModel):
    user_name : str
    email : str
    password : str

class Task(BaseModel):
    user_id : Optional[int] = None
    title : str
    description : Optional[str] = None
    dueDate : date
    priority : str
    completed : bool = False

class FetchTask(BaseModel):
    user_id : int

class DeleteTask(BaseModel):
    task_id : int

class UpdateTask(BaseModel):
    task_id : Optional[int] = None
    title : str
    description : Optional[str] = None
    dueDate : date
    priority : str
    completed : bool = False

class ToggleTask(BaseModel):
    task_id : Optional[int] | None

class ToggleSubtask(BaseModel):
    id : Optional[int] | None

class DeleteSubtask(BaseModel):
    id : Optional[int] | None

class subTaskContext(BaseModel):
    estimate : Optional[str] | None
    priority : Optional[str] | None
    title : Optional[str] | None

class CreateSubtask(BaseModel):
    parentTaskId: Optional[int] | None
    subtasks: List[subTaskContext]
