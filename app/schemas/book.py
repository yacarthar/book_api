from datetime import date
from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    publish_date: date  # ISO 8601 format `2022-11-15`
    price: float


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    class Config:
        orm_mode = True
