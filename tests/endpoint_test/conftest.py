import pytest
from fastapi.testclient import TestClient

from app.libs.auth import get_current_user
from app.libs.db import get_db
from app.main import app
from config import settings


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
