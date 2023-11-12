from sqlalchemy.orm import Session

from ..models.book import BookModel
from ..schemas.book import Book, BookCreate


def create_book(db: Session, data: BookCreate):
    new_book = BookModel(**data.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def get_book(db: Session, book_id: int):
    return db.query(BookModel).filter_by(id=book_id).first()


def get_book_by_isbn(db: Session, isbn: str):
    return db.query(BookModel).filter_by(isbn=isbn).first()
