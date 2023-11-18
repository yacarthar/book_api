from datetime import date, datetime
from typing import Union, List, Annotated

from pydantic import BaseModel, StringConstraints, PastDate, PositiveFloat, ConfigDict


class BookCreate(BaseModel):
    title: Annotated[
        str, StringConstraints(strip_whitespace=True, pattern=r"^[a-zA-Z0-9. ']+$")
    ]
    author: Annotated[
        str, StringConstraints(strip_whitespace=True, pattern=r"^[a-zA-Z. ']+$")
    ]
    isbn: Annotated[
        str, StringConstraints(strip_whitespace=True, pattern=r"^[0-9\-]{10,20}$")
    ]
    publish_date: Union[PastDate, None] = None
    price: Union[PositiveFloat, None] = None


class Book(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    publish_date: date  # ISO 8601 format `2022-11-15`
    price: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BookSearch(BaseModel):
    total: int
    result: List[Book]
    next_page: Union[str, None] = None
    prev_page: Union[str, None] = None


class BookUpdate(BaseModel):
    title: Annotated[
        str, StringConstraints(strip_whitespace=True, pattern=r"^[a-zA-Z0-9. ']+$")
    ] = None
    author: Annotated[
        str, StringConstraints(strip_whitespace=True, pattern=r"^[a-zA-Z. ']+$"), None
    ] = None
    isbn: Annotated[
        str, StringConstraints(strip_whitespace=True, pattern=r"^[0-9\-]{10,20}$"), None
    ] = None
    publish_date: Union[PastDate, None] = None
    price: Union[PositiveFloat, None] = None
