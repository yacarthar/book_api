from typing import Union, Annotated

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from ..libs.db import get_db
from ..services.book import (create_book, get_book, get_book_by_isbn,
                            list_books, delete_book
                            )
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


@router.get("/{book_id}", response_model=Book)
def get_book_(book_id: int, db: Session = Depends(get_db)):
    book = get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get("/", response_model=list[Book])
def list_books_(
    query: Union[str, None] = None,
    page: Annotated[Union[int, None], Query(ge=1)] = 1,
    per_page: Annotated[Union[int, None], Query(ge=5)] = 5,
    db: Session = Depends(get_db)
):
    books = list_books(db, keyword=query, page=page, per_page=per_page)
    return books


@router.delete("/{book_id}")
def delete_book_(book_id: int, db: Session = Depends(get_db)):
    deleted_book = delete_book(db, book_id=book_id)
    if deleted_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted_book
