from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from ..services.auth_service import register_user, login_user
from ..schemas.auth_schema import UserCreate, UserCreateResponse, UserLogin, LoginResponse

router = APIRouter(
      prefix="/auth",
      tags=["user"],
      responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.post("/register", response_model = UserCreateResponse, status_code = status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user)

@router.post("/login", status_code = status.HTTP_200_OK)
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, user)

@router.get("/profile")
def get_profile(current_user: dict = Depends(get_current_user)):
    return {
        "message": "This is your profile",
        "user": current_user
    }