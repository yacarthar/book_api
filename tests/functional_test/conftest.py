import json

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import pytest

from config import settings
from app.main import app
from app.libs import Base, UserModel, BookModel
from app.libs.db import get_db
from tests.functional_test.utils import mock_data


@pytest.fixture(scope="package")
def engine():
    engine = create_engine(settings.db_uri)
    connection = engine.connect()
    yield engine
    connection.close()


@pytest.fixture(scope="class")
def db(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    tables_to_clear = ["users", "books"]
    for table in tables_to_clear:
        query = f"DROP TABLE if exists {table} CASCADE"
        session.execute(query)
        session.commit()

    yield session

    session.rollback()
    for table in tables_to_clear:
        query = f"DROP TABLE if exists {table} CASCADE"
        session.execute(query)
        session.commit()
    session.close()


@pytest.fixture(scope="class")
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(scope="class")
def init_tables(engine, db):
    # create blank table
    Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="class")
def insert_mock_data(db: Session, init_tables):
    user1 = UserModel(
        username="user1", email="user1@example.com", password="testpassword1"
    )
    user2 = UserModel(
        username="user2", email="user2@example.com", password="testpassword2"
    )
    db.add(user1)
    db.add(user2)

    for item in mock_data:
        book = BookModel(**item)
        db.add(book)

    db.commit()


@pytest.fixture(autouse=True, scope="package")
def api():
    yield f"/api/{settings.API_VERSION}"


@pytest.fixture(scope="class")
def access_token(client, api, insert_mock_data):
    res = client.post(
        api + "/users/login",
        json={"email": "user1@example.com", "password": "testpassword1"},
    )
    return res.json()["access_token"]
