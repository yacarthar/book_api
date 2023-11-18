from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.libs.log import logger
from app.models.user import UserModel
from app.schemas.token import TokenPayload
from app.services.user import get_user
from config import settings

from .db import get_db
from .security import ALGORITHM

token_getter = OAuth2PasswordBearer(
    tokenUrl=f"/api/{settings.API_VERSION}/users/login"
)


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(token_getter)
) -> UserModel:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError) as e:
        logger.error(e)
        raise HTTPException(
            status_code=403,
            detail="Invalid credential!",
        )
    user = get_user(db, user_id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
