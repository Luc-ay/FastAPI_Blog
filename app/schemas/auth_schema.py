from pydantic import BaseModel, Field
from typing import Optional


class UserCreate(BaseModel):
    email: str
    password: str = Field(min_length=6)
    username: str = Field(min_length=3, max_length=50)
    full_name: Optional[str] = None


class UserCreateResponse(BaseModel):
    email: str
    username: str
    full_name: Optional[str] = None

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    message: str = "User logged in successfully"
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[str] = None

