import json

from app.schemas.user import User
from .mock_results import (
    book_data,
    list_book_result,
    user_data,
    user_cred_reg,
    user_cred_login,
)


class TestRegister:
    def test_register_fail(self, mocker, client, api):
        mocker.patch("app.routers.users.get_user_by_email", return_value=user_data)
        res = client.post(api + "/users", json=user_cred_reg)
        assert res.status_code == 400


    def test_register_success(self, mocker, client, api):
        mocker.patch("app.routers.users.get_user_by_email", return_value=None)
        mocker.patch("app.routers.users.create_user", return_value=user_data)
        res = client.post(api + "/users", json=user_cred_reg)
        assert res.status_code == 200


class TestGetUser:
    def test_user_success(self, client, mocker, api):
        mocker.patch("app.routers.users.get_user", return_value=user_data)
        res = client.get(api + "/users/2")
        assert res.status_code == 200

    def test_user_fail(self, client, mocker, api):
        mocker.patch("app.routers.users.get_user", return_value=None)
        res = client.get(api + "/users/2")
        assert res.status_code == 404


class TestLogin:
    def test_login_fail(self, mocker, client, api):
        mocker.patch("app.routers.users.authenticate_user", return_value=None)
        res = client.post(api + "/users/login", json=user_cred_login)
        assert res.status_code == 400

    def test_login_success(self, mocker, client, api):
        mocker.patch(
            "app.routers.users.authenticate_user",
            return_value=User.model_validate(user_data),
        )
        mocker.patch("app.routers.users.create_access_token", return_value="test_token")
        res = client.post(api + "/users/login", json=user_cred_login)
        assert res.status_code == 200
