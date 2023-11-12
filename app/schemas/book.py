from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    author: str
    isbn: str
    publish_date: str # ISO 8601 format `2022-11-15`
    price: float


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    class Config:
        orm_mode = True
