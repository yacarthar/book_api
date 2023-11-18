from typing import Union

from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    username: str
    password: str


class User(UserBase):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserLogin(UserBase):
    password: str
