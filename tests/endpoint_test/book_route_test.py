import json

from app.schemas.book import Book

from .mock_results import book_data, list_book_result


class TestGetBook:
    def test_get_book_ok(self, mocker, client, api):
        mocker.patch("app.routers.books.get_book", return_value=book_data)
        res = client.get(api + "/books/20")
        assert res.status_code == 200
        assert Book.model_validate(res.json())

    def test_get_book_notfound(self, client, mocker, api):
        mocker.patch("app.routers.books.get_book", return_value=None)
        res = client.get(api + "/books/20")
        assert res.status_code == 404
        info = json.loads(res.text).get("detail")
        assert info == "Book not found"


class TestListBooks:
    def test_params_success(self, client, mocker, api):
        mocker.patch(
            "app.routers.books.list_books", return_value=list_book_result
        )
        mocker.patch(
            "app.routers.books.build_url", return_value="http://test.url"
        )
        res = client.get(api + "/books/", params={"page": 2})
        assert res.status_code == 200


class TestCreateBook:
    def test_creat_success(self, mocker, client, api):
        mocker.patch("app.routers.books.get_book_by_isbn", return_value=None)
        mocker.patch("app.routers.books.create_book", return_value=book_data)

        res = client.post(api + "/books/", json=book_data)
        assert res.status_code == 200
        assert Book.model_validate(res.json())

    def test_create_with_exception(self, mocker, client, api):
        mocker.patch(
            "app.routers.books.get_book_by_isbn", return_value=book_data
        )
        res = client.post(api + "/books/", json=book_data)
        assert res.status_code == 400


class TestDeleteBook:
    def test_delete_book_ok(self, mocker, client, api):
        mocker.patch("app.routers.books.delete_book", return_value=book_data)
        res = client.delete(api + "/books/20")
        assert res.status_code == 200
        assert Book.model_validate(res.json())

    def test_delete_book_notfound(self, mocker, client, api):
        mocker.patch("app.routers.books.delete_book", return_value=None)
        res = client.delete(api + "/books/20")
        assert res.status_code == 404
        info = json.loads(res.text).get("detail")
        assert info == "Book not found"


class TestUpdateBook:
    def test_update_notfound(self, mocker, client, api):
        mocker.patch("app.routers.books.get_book", return_value=None)
        res = client.put(api + "/books/10", json=book_data)
        assert res.status_code == 404

    def test_update_fail(self, mocker, client, api):
        mocker.patch("app.routers.books.get_book", return_value=book_data)
        mocker.patch(
            "app.routers.books.update_book", side_effect=Exception("test")
        )
        res = client.put(api + "/books/10", json=book_data)
        assert res.status_code == 400

    def test_update_success(self, mocker, client, api):
        mocker.patch("app.routers.books.get_book", return_value=book_data)
        mocker.patch("app.routers.books.update_book", return_value=book_data)
        res = client.put(api + "/books/10", json=book_data)
        assert res.status_code == 200
        assert Book.model_validate(res.json())
