from functools import lru_cache
from typing import Annotated

from fastapi import FastAPI, Depends
from config import Settings
from .routers.users import router as user_router
from .routers.books import router as book_router

app = FastAPI()
app.include_router(user_router)
app.include_router(book_router)


@lru_cache
def get_settings():
    return Settings()


@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {"app_name": settings.app_name}
