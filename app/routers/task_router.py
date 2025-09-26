from typing import List,Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.task_schema import TaskResponse, TaskCreate, TaskListResponse, TaskEditResponse,TaskEdit
from app.services.task_service import create_task, get_tasks, get_task_by_id, edit_task, task_filter,delete_task

'''Declare the router'''
router = APIRouter(
    prefix="/task",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)

'''Get all tasks'''
@router.get("/", response_model= List[TaskListResponse], status_code=status.HTTP_200_OK)
def tasks(
    db: Session = Depends(get_db),
    auth: dict = Depends(get_current_user),
):
    tasks = get_tasks(db, user_id=auth['user_id'])

    return tasks

'''Filter tasks'''
@router.get("/filter", response_model= List[TaskListResponse], status_code=status.HTTP_200_OK)
def filter_tasks(
    name: Optional[str] = None,
    task_id: Optional[int] = None,
    progress: Optional[str] = None,
    db: Session = Depends(get_db),
    auth: dict = Depends(get_current_user),
):
    tasks = task_filter(db, name=name, task_id=task_id, progress=progress)

    return tasks

'''Create a task'''
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=TaskResponse)
def task(
    db: Session = Depends(get_db),
    task: TaskCreate = Body(...),
    auth: dict = Depends(get_current_user)
):
    create = create_task(db, task, user_id=auth['user_id'])
    return create

'''Get a task by id'''
@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def task_by_id(
    task_id: int,
    db: Session = Depends(get_db),
    auth: dict = Depends(get_current_user)
):
    task = get_task_by_id(db, task_id=task_id, user_id=auth['user_id'])

    return task

'''Edit a task by id'''
@router.put("/{task_id}", response_model=TaskEditResponse, status_code=status.HTTP_200_OK)
def edit_task_by_id(
    task_id: int,
    db: Session = Depends(get_db),
    auth: dict = Depends(get_current_user),
    task_update: TaskEdit = Body(...)
):
    return edit_task(db, task_id=task_id, user_id=auth['user_id'], task_update = task_update)

'''Delete a task by id'''
@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task_by_id(
    task_id: int,
    db: Session = Depends(get_db),
    auth: dict = Depends(get_current_user)
):
    return delete_task(db, task_id=task_id, user_id=auth['user_id'])