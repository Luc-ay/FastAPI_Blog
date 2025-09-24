from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..core.security import hash_password, verify_password
from ..models import user_models
from ..schemas.auth_schema import UserCreate, UserLogin

def register_user(db: Session, user: UserCreate):
    # Check if user already exists
    db_user = db.query(user_models.User).filter(user_models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    db_username = db.query(user_models.User).filter(user_models.User.username == user.username).first()
    if db_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    # Hash password
    hashed_password = hash_password(user.password)
    
    # Create User model instance
    new_user = user_models.User(email=user.email, username=user.username, password=hashed_password, full_name=user.full_name)
    
    # Save to DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


def login_user(db: Session, user: UserLogin):
    db_user = db.query(user_models.User).filter(user_models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    
    checkPWD = verify_password(user.password, str(db_user.password))  
    if not checkPWD:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credential password")
    
    return "User logged in successfully"
    