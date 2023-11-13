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
    return db.query(BookModel).get(book_id)


def get_book_by_isbn(db: Session, isbn: str):
    return db.query(BookModel).filter_by(isbn=isbn).first()


def list_books(db: Session, keyword: str, page: int, per_page: int):
    skip = (page - 1) * per_page
    limit = per_page
    if not keyword:
        return db.query(BookModel).offset(skip).limit(limit).all()
    else:
        return (
            db.query(BookModel)
            .filter(BookModel.title.ilike(f"%{keyword}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )


def delete_book(db: Session, book_id: int):
    book = db.query(BookModel).get(book_id)
    if book:
        db.delete(book)
        db.commit()
    return book
