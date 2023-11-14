from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..libs.db import get_db
from ..services.user import get_user, get_user_by_email, create_user, authenticate_user
from ..schemas.user import User, UserCreate, UserLogin
from ..libs.security import create_access_token


router = APIRouter(prefix="/users")


@router.post("/", response_model=User)
def create_user_(data: UserCreate, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, data=data)


@router.get("/{user_id}", response_model=User)
def get_user_(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credential!")
    return {"access_token": create_access_token(user.id)}
