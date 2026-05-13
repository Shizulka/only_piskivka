import pytest
from unittest.mock import MagicMock, patch

from src.domain.exceptions import UserAlreadyExistsError

class TestRegisterRoute:
    def test_success(self, client):
        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_user.user_name = "Аліса"
        mock_user.email.value = "alice@test.com"

        with patch("src.presentation.control_user.UserService") as MockSvc:
            MockSvc.return_value.register_user.return_value = mock_user
            resp = client.post(
                "/users/register",
                json={"user_name": "Аліса", "email": "alice@test.com", "password": "password123"},
            )

        assert resp.status_code == 200
        assert resp.json()["user_name"] == "Аліса"

    def test_duplicate_returns_400(self, client):
        with patch("src.presentation.control_user.UserService") as MockSvc:
            MockSvc.return_value.register_user.side_effect = UserAlreadyExistsError()
            resp = client.post(
                "/users/register",
                json={"user_name": "Аліса", "email": "alice@test.com", "password": "password123"},
            )

        assert resp.status_code == 400

    def test_missing_email_and_phone_returns_422(self, client):
        resp = client.post(
            "/users/register",
            json={"user_name": "Аліса", "password": "password123"},
        )
        assert resp.status_code == 422

class TestLoginRoute:
    def test_success_returns_token(self, client):
        mock_user = MagicMock()
        mock_user.user_id = 5

        with patch("src.presentation.control_user.UserService") as MockSvc:
            MockSvc.return_value.authenticate_user.return_value = mock_user
            resp = client.post(
                "/users/login",
                data={"username": "user@test.com", "password": "secret"},
            )

        assert resp.status_code == 200
        assert "access_token" in resp.json()
        assert resp.json()["token_type"] == "bearer"

    def test_wrong_credentials_returns_401(self, client):
        with patch("src.presentation.control_user.UserService") as MockSvc:
            MockSvc.return_value.authenticate_user.return_value = False
            resp = client.post(
                "/users/login",
                data={"username": "nobody@test.com", "password": "bad"},
            )

        assert resp.status_code == 401
