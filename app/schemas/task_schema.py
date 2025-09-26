from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ProgressStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class TaskBase(BaseModel):
    title: str = Field(min_length=3, max_length=100, default="Complete API Documentation")
    description: str = Field(default="Detailed documentation for the new API endpoints")
    progress:ProgressStatus 

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(min_length=3, max_length=100)
    description: Optional[str]
    progress: Optional[ProgressStatus]

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    progress: str

    class Config:
        from_attributes = True

class TaskListResponse(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


class TaskEdit(BaseModel):
    title: Optional[str] = None
    description:Optional [str] = None 
    progress: Optional[ProgressStatus] = None

class TaskEditResponse(BaseModel):
    id: int
    title: str
    description: str
    progress: str

    class Config:
        from_attributes = True