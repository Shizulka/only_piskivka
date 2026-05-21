import pytest
from unittest.mock import MagicMock, patch

from src.application.commands.user_command import CreateUserCommand, DeleteUserCommand
from src.application.commands.user_command_handlers import CreateUserHandler, DeleteUserHandler
from src.application.commands.place_commands import CreatePlaceCommand, DeletePlaceCommand
from src.application.commands.place_command_handlers import CreatePlaceHandler, DeletePlaceHandler
from src.application.commands.review_command import CreateReviewCommand, DeleteReviewCommand
from src.application.commands.review_command_handlers import CreateReviewHandler, DeleteReviewHandler

from src.application.queries.user_queries import AuthenticateUserQuery
from src.application.queries.user_queries_handlers import AuthenticateUserHandler
from src.application.queries.place_queries import GetAllPlacesQuery
from src.application.queries.place_query_handlers import GetAllPlacesHandler
from src.application.queries.review_query import GetAllReviewQuery
from src.application.queries.review_query_handlers import GetAllReviewsHandler

from src.domain.exceptions import (
    UserAlreadyExistsError,
    InvalidTimeRangeError,
    EmptyReviewError,
)
from src.domain.value_objects import TimeRange
from src.domain.entities import User, Place, Review
from src.domain.value_objects import Email

class TestCreateUserHandler:
    def setup_method(self):
        self.mock_repo = MagicMock()
        self.handler = CreateUserHandler(self.mock_repo)

    def test_create_success_returns_user_id(self):
        self.mock_repo.get_user_by_email.return_value = None
        created = MagicMock()
        created.user_id = 42
        self.mock_repo.create.return_value = created

        command = CreateUserCommand(
            password="securepass",
            email="vasyl@test.com",
            phone_number=None,
            user_name="Василь",
        )
        with patch("src.application.commands.user_command_handlers.get_password_hash", return_value="hashed"):
            result = self.handler.handle(command)

        assert result == 42
        self.mock_repo.create.assert_called_once()

    def test_create_duplicate_email_raises(self):
        self.mock_repo.get_user_by_email.return_value = MagicMock()

        command = CreateUserCommand(
            password="securepass",
            email="vasyl@test.com",
            phone_number=None,
            user_name="Василь",
        )
        with patch("src.application.commands.user_command_handlers.get_password_hash", return_value="hashed"):
            with pytest.raises(UserAlreadyExistsError):
                self.handler.handle(command)

    def test_create_invalid_email_raises(self):
        self.mock_repo.get_user_by_email.return_value = None

        command = CreateUserCommand(
            password="securepass",
            email="notanemail",
            phone_number=None,
            user_name="Василь",
        )
        with patch("src.application.commands.user_command_handlers.get_password_hash", return_value="hashed"):
            with pytest.raises(Exception):
                self.handler.handle(command)

    def test_password_is_hashed_before_storage(self):
        self.mock_repo.get_user_by_email.return_value = None
        created = MagicMock()
        created.user_id = 1
        self.mock_repo.create.return_value = created

        command = CreateUserCommand(
            password="plaintext",
            email="new@test.com",
            phone_number=None,
            user_name="Тест",
        )
        with patch("src.application.commands.user_command_handlers.get_password_hash", return_value="hashed_value") as mock_hash:
            self.handler.handle(command)

        mock_hash.assert_called_once_with("plaintext")
        user_arg = self.mock_repo.create.call_args[0][0]
        assert user_arg.password_hash == "hashed_value"

class TestDeleteUserHandler:
    def setup_method(self):
        self.mock_repo = MagicMock()
        self.handler = DeleteUserHandler(self.mock_repo)

    def test_delete_calls_repo(self):
        command = DeleteUserCommand(user_id=5)
        self.handler.handle(command)
        self.mock_repo.delete.assert_called_once_with(5)

class TestCreatePlaceHandler:
    def setup_method(self):
        self.mock_repo = MagicMock()
        self.handler = CreatePlaceHandler(self.mock_repo)

    def test_create_success_returns_place_id(self):
        created = MagicMock()
        created.place_id = 7
        self.mock_repo.create.return_value = created

        command = CreatePlaceCommand(
            location="Вул. Садова, 1",
            open_time="09:00",
            close_time="21:00",
            status="bar",
        )
        result = self.handler.handle(command)

        assert result == 7
        self.mock_repo.create.assert_called_once()

    def test_invalid_hours_raises(self):
        command = CreatePlaceCommand(
            location="Десь",
            open_time="22:00",
            close_time="08:00",
            status="cafe",
        )
        with pytest.raises(InvalidTimeRangeError):
            self.handler.handle(command)

    def test_equal_hours_raises(self):
        command = CreatePlaceCommand(
            location="Десь",
            open_time="10:00",
            close_time="10:00",
            status="shop",
        )
        with pytest.raises(InvalidTimeRangeError):
            self.handler.handle(command)

class TestDeletePlaceHandler:
    def setup_method(self):
        self.mock_repo = MagicMock()
        self.handler = DeletePlaceHandler(self.mock_repo)

    def test_delete_calls_repo(self):
        command = DeletePlaceCommand(place_id=3)
        self.handler.handle(command)
        self.mock_repo.delete.assert_called_once_with(3)

class TestCreateReviewHandler:
    def setup_method(self):
        self.mock_repo = MagicMock()
        self.handler = CreateReviewHandler(self.mock_repo)

    def test_create_success_returns_review_id(self):
        created = MagicMock()
        created.review_id = 99
        self.mock_repo.create.return_value = created

        command = CreateReviewCommand(place_id=1, user_id=2, content_in="Чудово!")
        result = self.handler.handle(command)

        assert result == 99
        self.mock_repo.create.assert_called_once()

    def test_empty_content_raises(self):
        command = CreateReviewCommand(place_id=1, user_id=2, content_in="")
        with pytest.raises((EmptyReviewError, TypeError)):
            self.handler.handle(command)

    def test_whitespace_content_raises(self):
        command = CreateReviewCommand(place_id=1, user_id=2, content_in="   ")
        with pytest.raises((EmptyReviewError, TypeError)):
            self.handler.handle(command)

class TestDeleteReviewHandler:
    def setup_method(self):
        self.mock_repo = MagicMock()
        self.handler = DeleteReviewHandler(self.mock_repo)

    def test_delete_calls_repo(self):
        command = DeleteReviewCommand(review_id=11)
        self.handler.handle(command)
        self.mock_repo.delete.assert_called_once_with(11)

class TestAuthenticateUserHandler:
    def setup_method(self):
        self.mock_repo = MagicMock()
        self.handler = AuthenticateUserHandler(self.mock_repo)

    def test_authenticate_by_email_success(self):
        mock_user = MagicMock()
        mock_user.password_hash = "hashed"
        self.mock_repo.get_user_by_email.return_value = mock_user

        query = AuthenticateUserQuery(username="user@test.com", password="pw")
        with patch("src.application.queries.user_queries_handlers.verify_password", return_value=True):
            result = self.handler.handle(query)

        assert result == mock_user

    def test_authenticate_by_phone_fallback(self):
        mock_user = MagicMock()
        mock_user.password_hash = "hashed"
        self.mock_repo.get_user_by_email.return_value = None
        self.mock_repo.get_user_by_phone.return_value = mock_user

        query = AuthenticateUserQuery(username="+380671234567", password="pw")
        with patch("src.application.queries.user_queries_handlers.verify_password", return_value=True):
            result = self.handler.handle(query)

        assert result == mock_user

    def test_authenticate_wrong_password_returns_false(self):
        mock_user = MagicMock()
        mock_user.password_hash = "hashed"
        self.mock_repo.get_user_by_email.return_value = mock_user

        query = AuthenticateUserQuery(username="user@test.com", password="wrong")
        with patch("src.application.queries.user_queries_handlers.verify_password", return_value=False):
            result = self.handler.handle(query)

        assert result is False

    def test_user_not_found_returns_false(self):
        self.mock_repo.get_user_by_email.return_value = None
        self.mock_repo.get_user_by_phone.return_value = None

        query = AuthenticateUserQuery(username="nobody@test.com", password="pw")
        result = self.handler.handle(query)

        assert result is False

class TestGetAllPlacesHandler:
    def setup_method(self):
        self.mock_repo = MagicMock()
        self.handler = GetAllPlacesHandler(self.mock_repo)

    def test_returns_read_models(self):
        mock_place = MagicMock()
        mock_place.place_id = 1
        mock_place.location = "Вул. Лісова, 5"
        mock_place.working_hours.open_time = "08:00"
        mock_place.working_hours.close_time = "20:00"
        mock_place.status = "bar"
        self.mock_repo.get_all_places.return_value = [mock_place]

        result = self.handler.handle(GetAllPlacesQuery())

        assert len(result) == 1
        assert result[0].location == "Вул. Лісова, 5"
        assert result[0].id == 1

    def test_returns_empty_list(self):
        self.mock_repo.get_all_places.return_value = []
        result = self.handler.handle(GetAllPlacesQuery())
        assert result == []

class TestGetAllReviewsHandler:
    def setup_method(self):
        self.mock_repo = MagicMock()
        self.handler = GetAllReviewsHandler(self.mock_repo)

    def test_returns_read_models(self):
        mock_review = MagicMock()
        mock_review.review_id = 3
        mock_review.user_id = 1
        mock_review.place_id = 2
        mock_review.content_in = "Непогано"
        self.mock_repo.get_all_reviews.return_value = [mock_review]

        result = self.handler.handle(GetAllReviewQuery())

        assert len(result) == 1
        assert result[0].content_in == "Непогано"
        assert result[0].review_id == 3

    def test_returns_empty_list(self):
        self.mock_repo.get_all_reviews.return_value = []
        result = self.handler.handle(GetAllReviewQuery())
        assert result == []