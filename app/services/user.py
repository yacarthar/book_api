from sqlalchemy.orm import Session

from ..models.user import UserModel
from ..schemas.user import User, UserCreate


def create_user(db: Session, data: UserCreate) -> UserModel:
    new_user = UserModel(**data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(db: Session, user_id: int) -> UserModel:
    return db.query(UserModel).filter_by(id=user_id).first()


def get_user_by_email(db: Session, email: str) -> UserModel:
    return db.query(UserModel).filter_by(email=email).first()
