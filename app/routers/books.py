from typing import Union, Annotated

from fastapi import APIRouter, HTTPException, Depends, Query, Request
from sqlalchemy.orm import Session

from ..libs.db import get_db
from ..libs.auth import get_current_user
from ..libs.utils import build_url
from ..libs.log import logger
from ..services.book import (
    create_book,
    get_book,
    get_book_by_isbn,
    list_books,
    delete_book,
    update_book,
)
from ..schemas.book import Book, BookCreate, BookSearch, BookUpdate

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Book, dependencies=[Depends(get_current_user)])
def create_book_(
    data: BookCreate,
    db: Session = Depends(get_db),
):
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


@router.get("/", response_model_exclude_none=True, response_model=BookSearch)
def list_books_(
    request: Request,
    db: Session = Depends(get_db),
    page: Annotated[Union[int, None], Query(ge=1)] = 1,
    limit: Annotated[Union[int, None], Query(ge=5)] = 5,
    title: Union[str, None] = None,
    author: Union[str, None] = None,
    date: Annotated[
        Union[str, None], Query(pattern=r"\b(?:before|after)?(\d{4}-\d{2}-\d{" r"2})\b")
    ] = None,
):
    total, result, next_page, prev_page = list_books(
        db, page=page, limit=limit, title=title, author=author, date=date
    )
    resp = {
        "total": total,
        "result": result,
    }

    if next_page:
        url = build_url(str(request.url), dict(request.query_params), next_page)
        resp.update({"next_page": url})

    if prev_page:
        url = build_url(str(request.url), dict(request.query_params), prev_page)
        resp.update({"prev_page": url})

    return resp


@router.delete("/{book_id}", dependencies=[Depends(get_current_user)])
def delete_book_(
    book_id: int,
    db: Session = Depends(get_db),
):
    deleted_book = delete_book(db, book_id=book_id)
    if deleted_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted_book


@router.put("/{book_id}", response_model=Book, dependencies=[Depends(get_current_user)])
def update_book_(
    book_id: int,
    data: BookUpdate,
    db: Session = Depends(get_db),
):
    book = get_book(db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    parsed_data = data.model_dump(exclude_none=True)
    try:
        res = update_book(db, book, parsed_data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="Invalid Book Input!")
    return res
