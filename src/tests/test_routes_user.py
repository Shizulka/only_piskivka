import pytest
from unittest.mock import MagicMock, patch, AsyncMock

from src.modules.core.domain.exceptions import UserAlreadyExistsError

class TestRegisterRoute:
    def test_success_returns_201(self, client):
        with patch("src.modules.core.presentation.control_user.CreateUserHandler") as MockHandler:
            MockHandler.return_value.handle = AsyncMock(return_value=1)
            resp = client.post(
                "/users/register",
                json={
                    "user_name": "Аліса",
                    "email": "alice@test.com",
                    "password": "password123",
                },
            )

        assert resp.status_code == 201
        assert resp.json()["user_id"] == 1
        assert "message" in resp.json()

    def test_duplicate_email_returns_400(self, client):
        with patch("src.modules.core.presentation.control_user.CreateUserHandler") as MockHandler:
            MockHandler.return_value.handle = AsyncMock(side_effect=UserAlreadyExistsError())
            resp = client.post(
                "/users/register",
                json={
                    "user_name": "Аліса",
                    "email": "alice@test.com",
                    "password": "password123",
                },
            )

        assert resp.status_code == 400

    def test_missing_email_and_phone_returns_422(self, client):
        resp = client.post(
            "/users/register",
            json={"user_name": "Аліса", "password": "password123"},
        )
        assert resp.status_code == 422

    def test_short_password_returns_422(self, client):
        resp = client.post(
            "/users/register",
            json={"user_name": "Аліса", "email": "a@test.com", "password": "short"},
        )
        assert resp.status_code == 422

    def test_short_username_returns_422(self, client):
        resp = client.post(
            "/users/register",
            json={"user_name": "ab", "email": "a@test.com", "password": "password123"},
        )
        assert resp.status_code == 422

    def test_register_with_phone_only_succeeds(self, client):
        with patch("src.modules.core.presentation.control_user.CreateUserHandler") as MockHandler:
            MockHandler.return_value.handle = AsyncMock(return_value=2)
            resp = client.post(
                "/users/register",
                json={
                    "user_name": "Борис",
                    "phone_number": "0671234567",
                    "password": "password123",
                },
            )

        assert resp.status_code == 201

    def test_handler_receives_correct_command(self, client):
        with patch("src.modules.core.presentation.control_user.CreateUserHandler") as MockHandler:
            MockHandler.return_value.handle = AsyncMock(return_value=3)
            client.post(
                "/users/register",
                json={
                    "user_name": "Галина",
                    "email": "halyna@test.com",
                    "password": "securepass1",
                },
            )

        command = MockHandler.return_value.handle.call_args[0][0]
        assert command.user_name == "Галина"
        assert command.email == "halyna@test.com"
        assert command.password == "securepass1"


class TestLoginRoute:
    def test_success_returns_token(self, client):
        mock_user = MagicMock()
        mock_user.user_id = 5

        with patch("src.modules.core.presentation.control_user.AuthenticateUserHandler") as MockHandler:
            MockHandler.return_value.handle.return_value = mock_user
            resp = client.post(
                "/users/login",
                data={"username": "user@test.com", "password": "secret"},
            )

        assert resp.status_code == 200
        assert "access_token" in resp.json()
        assert resp.json()["token_type"] == "bearer"

    def test_wrong_credentials_returns_401(self, client):
        with patch("src.modules.core.presentation.control_user.AuthenticateUserHandler") as MockHandler:
            MockHandler.return_value.handle.return_value = False
            resp = client.post(
                "/users/login",
                data={"username": "nobody@test.com", "password": "bad"},
            )

        assert resp.status_code == 401

    def test_login_missing_password_returns_422(self, client):
        resp = client.post("/users/login", data={"username": "user@test.com"})
        assert resp.status_code == 422

    def test_handler_receives_correct_query(self, client):
        mock_user = MagicMock()
        mock_user.user_id = 1

        with patch("src.modules.core.presentation.control_user.AuthenticateUserHandler") as MockHandler:
            MockHandler.return_value.handle.return_value = mock_user
            client.post(
                "/users/login",
                data={"username": "user@test.com", "password": "mypassword"},
            )

        query = MockHandler.return_value.handle.call_args[0][0]
        assert query.username == "user@test.com"
        assert query.password == "mypassword"