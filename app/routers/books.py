from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{book_id}")
async def get_book(book_id: str):
    # if book_id not in query:
    #     raise HTTPException(status_code=404, detail="Item not found")
    return {"name": "demo book name", "book_id": book_id}
