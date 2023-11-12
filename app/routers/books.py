from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ..libs.db import get_db
from ..services.book import create_book, get_book, get_book_by_isbn
from ..schemas.book import Book, BookCreate

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Book)
def create_book_(data: BookCreate, db: Session = Depends(get_db)):
    _book = get_book_by_isbn(db, isbn=data.isbn)
    if _book:
        raise HTTPException(status_code=400, detail="Book already exists")
    return create_book(db=db, data=data)


@router.get("/{book_id}")
def get_book_(book_id: str, db: Session = Depends(get_db)):
    book = get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
