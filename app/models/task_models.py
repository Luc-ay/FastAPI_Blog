from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.core.database import Base


class ProgressStatus(PyEnum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    progress = Column(SQLEnum(ProgressStatus, name="task_progress"), default=ProgressStatus.NOT_STARTED, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id")) 
    user = relationship("User", back_populates="tasks")