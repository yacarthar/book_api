import json

from httpx import Response
from app.schemas.user import User


class TestRegister:
    def test_register_ok(self, client, insert_mock_data, api):
        user_credential = {
            "username": "user3",
            "email": "user3@example.com",
            "password": "testpassword3",
        }
        res = client.post(api + "/users/", json=user_credential)
        assert res.status_code == 200
        assert User.model_validate(res.json())

    def test_email_exist(self, client, insert_mock_data, api):
        user_credential = {
            "username": "test",
            "email": "user1@example.com",
            "password": "testpassword1",
        }
        res: Response = client.post(api + "/users/", json=user_credential)
        assert res.is_client_error
        assert res.status_code == 400
        info = json.loads(res.text).get("detail")
        assert info == "Email already registered"

    def test_email_missing(self, client, insert_mock_data, api):
        user_credential = {
            "username": "test",
            "password": "testpassword1",
        }
        res: Response = client.post(api + "/users/", json=user_credential)
        assert res.is_client_error
        assert res.status_code == 422

    def test_password_missing(self, client, insert_mock_data, api):
        user_credential = {"username": "test", "email": "user999@example.com"}
        res: Response = client.post(api + "/users/", json=user_credential)
        assert res.is_client_error
        assert res.status_code == 422

    def test_username_missing(self, client, insert_mock_data, api):
        user_credential = {
            "email": "user999@example.com",
            "password": "testpassword1",
        }
        res: Response = client.post(api + "/users/", json=user_credential)
        assert res.is_client_error
        assert res.status_code == 422


class TestLogin:
    def test_login_ok(self, client, insert_mock_data, api):
        user_credential = {
            "email": "user2@example.com",
            "password": "testpassword2",
        }
        res = client.post(api + "/users/login", json=user_credential)
        assert res.status_code == 200
        assert res.json().get("access_token")

    def test_email_missing(self, client, insert_mock_data, api):
        user_credential = {
            "password": "testpassword1",
        }
        res: Response = client.post(api + "/users/login", json=user_credential)
        assert res.is_client_error
        assert res.status_code == 422

    def test_password_missing(self, client, insert_mock_data, api):
        user_credential = {"email": "user999@example.com"}
        res: Response = client.post(api + "/users/login", json=user_credential)
        assert res.is_client_error
        assert res.status_code == 422

    def test_wrong_password(self, client, insert_mock_data, api):
        user_credential = {
            "email": "user2@example.com",
            "password": "testpassword22222",
        }
        res = client.post(api + "/users/login", json=user_credential)
        assert res.status_code == 400
        info = json.loads(res.text).get("detail")
        assert info == "Invalid credential!"

    def test_wrong_email(self, client, insert_mock_data, api):
        user_credential = {
            "email": "user22222@example.com",
            "password": "testpassword2",
        }
        res = client.post(api + "/users/login", json=user_credential)
        assert res.status_code == 400
        info = json.loads(res.text).get("detail")
        assert info == "Invalid credential!"


class TestGetUser:
    def test_get_user_ok(self, client, insert_mock_data, api):
        res = client.get(api + "/users/2")
        assert res.status_code == 200
        assert User.model_validate(res.json())

    def test_user_not_found(self, client, insert_mock_data, api):
        res = client.get(api + "/users/2222")
        assert res.status_code == 404
        info = json.loads(res.text).get("detail")
        assert info == "User not found"
