from typing import Union, Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    username: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True, pattern=r"^[a-zA-Z0-9]+$", max_length=30
        ),
    ]
    password: Annotated[str, StringConstraints(min_length=8)]


class User(UserBase):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserLogin(UserBase):
    password: Annotated[str, StringConstraints(min_length=8)]
