import os
from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from config import settings
from .routers.users import router as user_router
from .routers.books import router as book_router


app = FastAPI()

app.include_router(user_router)
app.include_router(book_router)


@app.get("/config/")
async def config(settings=settings):
    return settings


@app.get("/config/cloud")
def config_cloud():
    return {
        "SECRET_KEY": os.environ.get("SECRET_KEY"),
        "PLATFORM_APP_DIR": os.environ.get("PLATFORM_APP_DIR"),
        "PLATFORM_APPLICATION": os.environ.get("PLATFORM_APPLICATION"),
        "PLATFORM_APPLICATION_NAME": os.environ.get("PLATFORM_APPLICATION_NAME"),
        "PLATFORM_DOCUMENT_ROOT": os.environ.get("PLATFORM_DOCUMENT_ROOT"),
        "PLATFORM_ENVIRONMENT": os.environ.get("PLATFORM_ENVIRONMENT"),
        "PLATFORM_ENVIRONMENT_TYPE": os.environ.get("PLATFORM_ENVIRONMENT_TYPE"),
        "PLATFORM_OUTPUT_DIR": os.environ.get("PLATFORM_OUTPUT_DIR"),
        "PLATFORM_ROUTES": os.environ.get("PLATFORM_ROUTES"),
        "PLATFORM_SOURCE_DIR": os.environ.get("PLATFORM_SOURCE_DIR"),
        "PLATFORM_VARIABLES": os.environ.get("PLATFORM_VARIABLES"),
        "PORT": os.environ.get("PORT"),
        "PLATFORM_APP_DIR": os.environ.get("PLATFORM_APP_DIR"),
        "PLATFORM_APP_DIR": os.environ.get("PLATFORM_APP_DIR"),
        "PLATFORM_RELATIONSHIPS": os.environ.get("PLATFORM_RELATIONSHIPS"),
    }
