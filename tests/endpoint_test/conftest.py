import json

from fastapi.testclient import TestClient
import pytest

from config import settings
from app.main import app
from app.libs.auth import get_current_user
from app.libs.db import get_db


@pytest.fixture(scope="package")
def client():
    app.dependency_overrides[get_db] = lambda: None
    app.dependency_overrides[get_current_user] = lambda: None
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(scope="package")
def api():
    yield f"/api/{settings.API_VERSION}"
