import json

from httpx import Response
from app.schemas.book import Book, BookSearch


class TestGetBook:
    def test_get_book_ok(self, client, insert_mock_data, api):
        res = client.get(api + "/books/20")
        assert res.status_code == 200
        assert Book.model_validate(res.json())

    def test_get_book_notfound(self, client, insert_mock_data, api):
        res: Response = client.get(api + "/books/999")
        assert res.is_client_error
        assert res.status_code == 404
        info = json.loads(res.text).get("detail")
        assert info == "Book not found"


class TestListBooks:
    def test_no_params_success(self, client, insert_mock_data, api):
        res = client.get(api + "/books/", params={"page": 2})
        assert res.status_code == 200
        assert BookSearch.model_validate(res.json())

    def test_zero_result(self, client, insert_mock_data, api):
        res = client.get(api + "/books/", params={"title": "strange_name1"})
        assert res.status_code == 200
        assert BookSearch(**res.json()).total == 0
        assert BookSearch(**res.json()).result == []

    def test_search_title(self, client, insert_mock_data, api):
        res = client.get(api + "/books/", params={"title": "smile"})
        assert res.status_code == 200
        parsed_data = BookSearch(**res.json())
        assert parsed_data.total > 0
        assert bool(parsed_data.result)

    def test_search_author(self, client, insert_mock_data, api):
        res = client.get(api + "/books/", params={"author": "Watson"})
        assert res.status_code == 200
        parsed_data = BookSearch(**res.json())
        assert parsed_data.total > 0
        assert bool(parsed_data.result)

    def test_search_date_exact(self, client, insert_mock_data, api):
        res = client.get(api + "/books/", params={"date": "2017-03-16"})
        assert res.status_code == 200
        parsed_data = BookSearch(**res.json())
        assert parsed_data.total > 0
        assert bool(parsed_data.result)

    def test_search_date_before(self, client, insert_mock_data, api):
        res = client.get(api + "/books/", params={"date": "before2019-01-01"})
        assert res.status_code == 200
        parsed_data = BookSearch(**res.json())
        assert parsed_data.total > 0
        assert bool(parsed_data.result)

    def test_search_date_after(self, client, insert_mock_data, api):
        res = client.get(api + "/books/", params={"date": "after2019-01-01"})
        assert res.status_code == 200
        parsed_data = BookSearch(**res.json())
        assert parsed_data.total > 0
        assert bool(parsed_data.result)


class TestCreatBook:
    def test_no_token(self, client, insert_mock_data, api):
        res = client.post(api + "/books/")
        assert res.status_code == 401

    def test_with_token_and_valid_input(self, client, api, access_token):
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "888-1-444555-99-9",
            "publish_date": "1992-05-06",
            "price": 11.89,
        }
        headers = {"Authorization": "Bearer " + access_token}
        res = client.post(api + "/books/", json=book_data, headers=headers)
        assert res.status_code == 200
        assert Book.model_validate(res.json())

    def test_exist_book(self, client, api, access_token):
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "978-0-946194-15-5",
            "publish_date": "1992-05-06",
            "price": 11.89,
        }
        headers = {"Authorization": "Bearer " + access_token}
        res = client.post(api + "/books/", json=book_data, headers=headers)
        assert res.status_code == 400
        info = json.loads(res.text).get("detail")
        assert info == "Book already exists"

    def test_invalid_title(self, client, api, access_token):
        book_data = {
            "title": "Test%@ Book",
            "author": "Test Author",
            "isbn": "888-0-444555-99-9",
        }
        headers = {"Authorization": "Bearer " + access_token}
        res = client.post(api + "/books/", json=book_data, headers=headers)
        assert res.status_code == 422

    def test_missing_title(self, client, api, access_token):
        book_data = {
            "author": "Test Author",
            "isbn": "888-0-444555-99-9",
        }
        headers = {"Authorization": "Bearer " + access_token}
        res = client.post(api + "/books/", json=book_data, headers=headers)
        assert res.status_code == 422

    def test_invalid_author(self, client, api, access_token):
        book_data = {
            "title": "Test%@ Book",
            "author": "Test 111 Author",
            "isbn": "888-0-444555-99-9",
        }
        headers = {"Authorization": "Bearer " + access_token}
        res = client.post(api + "/books/", json=book_data, headers=headers)
        assert res.status_code == 422

    def test_missing_author(self, client, api, access_token):
        book_data = {
            "title": "Test%@ Book",
            "author": "Test 111 Author",
            "isbn": "888-0-444555-99-9",
        }
        headers = {"Authorization": "Bearer " + access_token}
        res = client.post(api + "/books/", json=book_data, headers=headers)
        assert res.status_code == 422

    def test_invalid_isbn(self, client, api, access_token):
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "888-0-abcdef-99-9",
        }
        headers = {"Authorization": "Bearer " + access_token}
        res = client.post(api + "/books/", json=book_data, headers=headers)
        assert res.status_code == 422

    def test_missing_isbn(self, client, api, access_token):
        book_data = {"title": "Test Book", "author": "Test Author"}
        headers = {"Authorization": "Bearer " + access_token}
        res = client.post(api + "/books/", json=book_data, headers=headers)
        assert res.status_code == 422

    def test_invalid_date(self, client, api, access_token):
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "887-0-444555-99-9",
            "publish_date": "2099-05-27",
        }
        headers = {"Authorization": "Bearer " + access_token}
        res = client.post(api + "/books/", json=book_data, headers=headers)
        assert res.status_code == 422

    def test_invalid_price(self, client, api, access_token):
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "886-0-444555-99-9",
            "price": "%17@.76",
        }
        headers = {"Authorization": "Bearer " + access_token}
        res = client.post(api + "/books/", json=book_data, headers=headers)
        assert res.status_code == 422


class TestDeleteBook:
    def test_delete_book_ok(self, client, api, access_token):
        headers = {"Authorization": "Bearer " + access_token}
        res = client.delete(api + "/books/20", headers=headers)
        assert res.status_code == 200
        assert Book.model_validate(res.json())

    def test_book_not_found(self, client, api, access_token):
        headers = {"Authorization": "Bearer " + access_token}
        res = client.delete(api + "/books/999", headers=headers)
        assert res.is_client_error
        assert res.status_code == 404
        info = json.loads(res.text).get("detail")
        assert info == "Book not found"


class TestUpdateBook:
    def test_no_token(self, client, insert_mock_data, api):
        res = client.put(api + "/books/20")
        assert res.status_code == 401

    def test_with_token_but_book_not_found(self, client, api, access_token):
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "888-0-444666-22-2",
            "publish_date": "1992-05-06",
            "price": 11.89,
        }
        headers = {"Authorization": "Bearer " + access_token}
        res = client.put(api + "/books/2222", json=book_data, headers=headers)
        assert res.status_code == 404
        info = json.loads(res.text).get("detail")
        assert info == "Book not found"

    def test_with_token_and_valid_input(self, client, api, access_token):
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "888-1-444666-99-9",
            "publish_date": "1992-05-06",
            "price": 11.89,
        }
        headers = {"Authorization": "Bearer " + access_token}
        res = client.put(api + "/books/20", json=book_data, headers=headers)
        assert res.status_code == 200
        assert Book.model_validate(res.json())

    def test_invalid_title(self, client, api, access_token):
        book_data = {
            "title": "Test%@ Book",
            "author": "Test Author",
            "isbn": "888-0-444555-99-9",
        }
        headers = {"Authorization": "Bearer " + access_token}
        res = client.put(api + "/books/20", json=book_data, headers=headers)
        assert res.status_code == 422

    def test_invalid_author(self, client, api, access_token):
        book_data = {
            "title": "Test%@ Book",
            "author": "Test 111 Author",
            "isbn": "888-0-444555-99-9",
        }
        headers = {"Authorization": "Bearer " + access_token}
        res = client.put(api + "/books/20", json=book_data, headers=headers)
        assert res.status_code == 422

    def test_invalid_isbn(self, client, api, access_token):
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "888-0-abcdef-99-9",
        }
        headers = {"Authorization": "Bearer " + access_token}
        res = client.put(api + "/books/20", json=book_data, headers=headers)
        assert res.status_code == 422

    def test_invalid_date(self, client, api, access_token):
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "887-0-444555-99-9",
            "publish_date": "2099-05-27",
        }
        headers = {"Authorization": "Bearer " + access_token}
        res = client.put(api + "/books/20", json=book_data, headers=headers)
        assert res.status_code == 422

    def test_invalid_price(self, client, api, access_token):
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "886-0-444555-99-9",
            "price": "%17@.76",
        }
        headers = {"Authorization": "Bearer " + access_token}
        res = client.put(api + "/books/20", json=book_data, headers=headers)
        assert res.status_code == 422

    def test_duplicate_book_isbn(self, client, api, access_token):
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "978-1-5402-3620-3",
            "publish_date": "1992-05-06",
            "price": 11.89,
        }
        headers = {"Authorization": "Bearer " + access_token}
        res = client.put(api + "/books/1", json=book_data, headers=headers)
        assert res.status_code == 400
        info = json.loads(res.text).get("detail")
        assert info == "Invalid Book Input!"
