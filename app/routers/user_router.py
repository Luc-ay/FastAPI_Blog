from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from ..services.auth_service import get_user_by_id, register_user, login_user
from ..schemas.auth_schema import UserCreate, UserCreateResponse, UserLogin, LoginResponse, GetUserResponse
from app.core.security import get_current_user

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

@router.post("/login", status_code = status.HTTP_200_OK, response_model=LoginResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, user)

@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=GetUserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return get_user_by_id(db, user_id)