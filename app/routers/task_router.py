from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.task_schema import TaskResponse, TaskCreate
from app.services.task_service import create_task


router = APIRouter(
      prefix="/task",
      tags=["tasks"],
      responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_tasks():
    return [{"task": "Task 1"}, {"task": "Task 2"}]

from fastapi import Body

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=TaskResponse)
async def task(
    db: Session = Depends(get_db),
    task: TaskCreate = Body(...),
    auth: dict = Depends(get_current_user)
):
    create = await create_task(db, task, user_id=auth['user_id'])
    return create