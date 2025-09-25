from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user


router = APIRouter(
      prefix="/tasks",
      tags=["tasks"],
      responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_tasks():
    return [{"task": "Task 1"}, {"task": "Task 2"}]