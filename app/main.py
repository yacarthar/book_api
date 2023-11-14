from functools import lru_cache
from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from config import settings
from .routers.users import router as user_router
from .routers.books import router as book_router


app = FastAPI()

app.include_router(user_router)
app.include_router(book_router)


@app.get("/info")
async def info(settings=settings):
    return settings
