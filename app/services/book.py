import math
import re
from datetime import date
from typing import Union

from sqlalchemy.orm import Session

from ..models.book import BookModel
from ..schemas.book import Book, BookCreate


def create_book(db: Session, data: BookCreate) -> BookModel:
    new_book = BookModel(**data.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def get_book(db: Session, book_id: int) -> Union[BookModel, None]:
    return db.query(BookModel).get(book_id)


def get_book_by_isbn(db: Session, isbn: str) -> Union[BookModel, None]:
    return db.query(BookModel).filter_by(isbn=isbn).first()


def list_books(db: Session, page: int, limit: int, **kwargs):
    query = db.query(BookModel)
    for key, value in kwargs.items():
        if key in ["title", "author"] and value is not None:
            query = query.filter(getattr(BookModel, key).ilike(f"%{value}%"))

        if key == "date" and value is not None:
            pattern = r"\d{4}-\d{2}-\d{2}"  # yyyy-mm-dd
            dates: list[str] = re.findall(pattern, value)
            exact_date = date.fromisoformat(dates[0])
            date_search_type = value.strip(dates[0])  # before/after/empty
            if date_search_type == "before":
                query = query.filter(BookModel.publish_date < exact_date)
            if date_search_type == "after":
                query = query.filter(BookModel.publish_date > exact_date)
            if not date_search_type:
                query = query.filter(BookModel.publish_date == exact_date)

    total = query.count()
    last_page = math.ceil(total / limit)
    page = min(page, last_page)

    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)
    result = query.all()

    next_page = page + 1 if page < last_page else None
    prev_page = page - 1 if page > 1 else None

    return total, result, next_page, prev_page


def delete_book(db: Session, book_id: int) -> Union[BookModel, None]:
    book = db.query(BookModel).get(book_id)
    if book:
        db.delete(book)
        db.commit()
    return book


def update_book(db: Session, book: BookModel, data: dict) -> Union[BookModel, None]:
    for key, value in data.items():
        setattr(book, key, value)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book
