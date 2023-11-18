from datetime import datetime

from sqlalchemy import Column, Date, DateTime, Integer, Numeric, String
from sqlalchemy.orm import validates

from ..libs.db import Base


class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), nullable=False, index=True)
    author = Column(String(60), nullable=False)
    isbn = Column(String(20), nullable=False, unique=True)
    publish_date = Column(Date)
    price = Column(Numeric(precision=10, scale=2))
    created_at = Column(DateTime, default=datetime.now)

    @validates("price")
    def validate_price(self, key, value):
        if not isinstance(value, (int, float, Numeric)):
            raise ValueError("Price must be a numeric value.")
        if value < 0:
            raise ValueError("Price must be a positive number.")
        return value
