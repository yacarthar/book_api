from typing import Optional

from sqlalchemy.orm import Session

from ..models.user import UserModel
from ..schemas.user import UserCreate


def create_user(db: Session, data: UserCreate) -> UserModel:
    new_user = UserModel(**data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(db: Session, user_id: int) -> UserModel:
    return db.query(UserModel).filter_by(id=user_id).first()


def get_user_by_email(db: Session, email: str) -> UserModel:
    return db.query(UserModel).filter_by(email=email).first()


def authenticate_user(
    db: Session, email: str, password: str
) -> Optional[UserModel]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not user.verify_password(password):
        return None
    return user
