from datetime import date
from typing import Union, List
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
        from_attributes = True

class BookSearch(BaseModel):
    total: int
    result: List[Book]
    next_page: Union[str, None] = None
    prev_page: Union[str, None] = None
