from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.models import task_models, user_models
from app.schemas.task_schema import TaskCreate, TaskEdit
from typing import Optional


def create_task(db: Session, task: TaskCreate, user_id: int):
    get_user = db.query(user_models.User).filter(user_models.User.id == user_id).first()
    if not get_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    create = task_models.Task(title=task.title, description=task.description, progress=task.progress_status, user_id=user_id)

    db.add(create)
    db.commit()
    db.refresh(create)

    return create


def get_tasks(db: Session, user_id: int):

    get_user = db.query(user_models.User).filter(user_models.User.id == user_id).first()

    if not get_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    tasks = db.query(task_models.Task).filter(task_models.Task.user_id == user_id).all()

    
        
    return tasks




def task_filter(db: Session, name: Optional[str] = None, task_id: Optional[int] = None, progress: Optional[str] = None):
    query = db.query(task_models.Task)

    if name:
        query = query.filter(task_models.Task.title.ilike(f"%{name}%"))
    if task_id:
        query = query.filter(task_models.Task.id == task_id)
    if progress:
        query = query.filter(task_models.Task.progress == progress)

    return query.all()


def get_task_by_id(db: Session, task_id: int, user_id: int):
    get_user = db.query(user_models.User).filter(user_models.User.id == user_id).first()

    if not get_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    task = db.query(task_models.Task).filter(task_models.Task.id == task_id, task_models.Task.user_id == user_id).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    return task

def edit_task(db: Session, task_id: int, user_id: int, task_update: TaskEdit) -> task_models.Task:
    user = db.query(user_models.User).filter(user_models.User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    task = db.query(task_models.Task).filter(
        task_models.Task.id == task_id, task_models.Task.user_id == user_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    # Update fields only if they are provided
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task