
from fastapi import FastAPI

from config import settings
from .routers.users import router as user_router
from .routers.books import router as book_router

version = settings.API_VERSION
app = FastAPI(
    redoc_url=f"/api/{version}/redoc",
    openapi_url=f"/api/{version}/openapi.json"
)

app.include_router(user_router, prefix=f"/api/{version}")
app.include_router(book_router, prefix=f"/api/{version}")
