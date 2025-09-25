from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional
from jose import JWTError, jwt
from .config import settings


''' Password hashing and verification '''
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


''' Create a JWT token with an expiration time '''
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

    return encoded_jwt


''' Verify the token and return the payload if valid, otherwise return None '''

def verify_token(token: str):

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        return payload 
    
    except JWTError:
        return None
    


''' Dependency to get the current user from the token '''
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  

def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        user_id: Optional[str] = payload.get("user_id")
        role: Optional[str] = payload.get("role")
        exp: Optional[int] = payload.get("exp")

        if user_id is None or role is None:
            raise credentials_exception

        # Optional: Check expiration manually (though jose handles it)
        if exp:
            if datetime.now(timezone.utc).timestamp() > exp:
                raise credentials_exception

        return {
            "user_id": user_id,
            "role": role
        }

    except JWTError:
        raise credentials_exception
    

''' Dependency to require admin role '''
def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return current_user