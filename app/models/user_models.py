from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum
from enum import Enum as PyEnum
from app.core.database import Base

class UserRole(PyEnum):
    ADMIN = "admin"
    USER = "user"
    AUTHOR = "author"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(Text, nullable=False)
    full_name = Column(String)
    role = Column(SQLEnum(UserRole, name="user_roles"), default=UserRole.USER, nullable=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
