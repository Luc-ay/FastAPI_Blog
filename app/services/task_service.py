from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.models import task_models, user_models
from app.schemas.task_schema import TaskCreate


async def create_task(db: Session, task: TaskCreate, user_id: int):
    get_user = db.query(user_models.User).filter(user_models.User.id == user_id).first()
    if not get_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    create = task_models.Task(title=task.title, description=task.description, progress=task.progress_status, user_id=user_id)

    db.add(create)
    db.commit()
    db.refresh(create)

    return create