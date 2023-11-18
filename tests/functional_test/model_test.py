import pytest

from app.models.book import BookModel
from app.models.user import UserModel


class TestBookModel:
    def test_serialization(self, db, insert_mock_data):
        book_data = {
            "title": "Person develop reality movement partner design.",
            "author": "John Ferguson",
            "isbn": "978-0-530-83462-7",
            "publish_date": "2008-10-12",
            "price": 29.59,
        }
        book = BookModel(**book_data)
        db.add(book)
        db.commit()
        assert book.id is not None

        get_book = db.query(BookModel).get(book.id)
        assert get_book is not None
        assert get_book.title == book_data["title"]
        assert get_book.author == book_data["author"]

    def test_invalid_price_type(self, db, insert_mock_data):
        book_data = {
            "title": "Person develop reality movement partner design.",
            "author": "John Ferguson",
            "isbn": "978-0-530-83462-7",
            "publish_date": "2008-10-12",
            "price": "29.59",
        }
        with pytest.raises(ValueError):
            BookModel(**book_data)

    def test_invalid_price_negative(self, db, insert_mock_data):
        book_data = {
            "title": "Person develop reality movement partner design.",
            "author": "John Ferguson",
            "isbn": "978-0-530-83462-7",
            "publish_date": "2008-10-12",
            "price": -20,
        }
        with pytest.raises(ValueError):
            BookModel(**book_data)


class TestUserModel:
    def test_serialization(self, db, insert_mock_data):
        user_data = {
            "email": "user1@gmail.com",
            "username": "user10",
            "password": "temp-password",
        }
        user = UserModel(**user_data)
        db.add(user)
        db.commit()
        assert user.id is not None

        get_user = db.query(UserModel).get(user.id)
        assert get_user is not None
        assert get_user.username == user_data["username"]
        assert get_user.email == user_data["email"]

    def test_invalid_email(self, db, insert_mock_data):
        user_data = {
            "email": "user20*!gmail.com",
            "username": "user20",
            "password": "temp-password",
        }
        with pytest.raises(ValueError):
            UserModel(**user_data)

    def test_password(self, db, insert_mock_data):
        user_data = {
            "email": "user3@gmail.com",
            "username": "user30",
            "password": "temp-password",
        }
        user = UserModel(**user_data)
        user.set_password("test-password")
        assert user.verify_password("test-password")
