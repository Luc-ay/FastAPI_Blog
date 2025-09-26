from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..core.security import create_access_token, hash_password, verify_password
from app.schemas.auth_schema import GetUserResponse
from ..models import user_models, task_models
from ..schemas.auth_schema import UserCreate, UserLogin


''' Service functions for user authentication and registration.'''

def register_user(db: Session, user: UserCreate):
    
    db_user = db.query(user_models.User).filter(user_models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    db_username = db.query(user_models.User).filter(user_models.User.username == user.username).first()
    if db_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    
    hashed_password = hash_password(user.password)
    
    
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
    
    role = db_user.role.value if hasattr(db_user.role, "value") else db_user.role

    token_data = {
        "user_id": db_user.id,
        "role": role
    }

    access_token = create_access_token(data=token_data)

    return {
        "message": "User logged in successfully",
        "access_token": access_token,
        "token_type": "bearer"
    }
    
def get_user_by_id(db: Session, user_id: int):
    get_user = db.query(user_models.User).filter(user_models.User.id == user_id).first()

    if not get_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    tasks = db.query(task_models.Task).filter(task_models.Task.user_id == user_id).all()
    
    task_titles = [task.title for task in tasks]

    
    return {
        "id": get_user.id,
        "username": get_user.username,
        "role": get_user.role,
        "email": get_user.email,
        "full_name": get_user.full_name,
        "task_count": len(tasks),
        "task_titles": task_titles
    }

    