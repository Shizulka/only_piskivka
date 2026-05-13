import pytest
from unittest.mock import MagicMock, patch

from src.application.service_user import UserService
from src.application.service_place import PlaceService
from src.application.service_review import ReviewService
from src.domain.exceptions import (
    UserAlreadyExistsError,
    InvalidTimeRangeError,
    EmptyReviewError,
)

class TestUserService:
    def setup_method(self):
        self.mock_repo = MagicMock()
        self.service = UserService(self.mock_repo)

    def _user_data(self, email="k@test.com", password="pass123"):
        data = MagicMock()
        data.user_name = "катя"
        data.email = email
        data.phone_number = None
        data.password = password
        return data

    def test_register_success(self):
        self.mock_repo.get_user_by_email.return_value = None
        expected = MagicMock()
        expected.user_id = 42
        self.mock_repo.create.return_value = expected

        with patch("src.application.service_user.get_password_hash", return_value="hashed"):
            result = self.service.register_user(self._user_data())

        assert result.user_id == 42
        self.mock_repo.create.assert_called_once()

    def test_register_duplicate_raises(self):
        self.mock_repo.get_user_by_email.return_value = MagicMock()
        with patch("src.application.service_user.get_password_hash", return_value="hashed"):
            with pytest.raises(UserAlreadyExistsError):
                self.service.register_user(self._user_data())

    def test_authenticate_by_email_success(self):
        mock_user = MagicMock()
        mock_user.password_hash = "hashed_pw"
        self.mock_repo.get_user_by_email.return_value = mock_user

        with patch("src.application.service_user.verify_password", return_value=True):
            result = self.service.authenticate_user("k@test.com", "pass123")

        assert result == mock_user

    def test_authenticate_wrong_password(self):
        mock_user = MagicMock()
        mock_user.password_hash = "hashed_pw"
        self.mock_repo.get_user_by_email.return_value = mock_user

        with patch("src.application.service_user.verify_password", return_value=False):
            result = self.service.authenticate_user("k@test.com", "wrong")

        assert result is False

    def test_authenticate_user_not_found(self):
        self.mock_repo.get_user_by_email.return_value = None
        self.mock_repo.get_user_by_phone.return_value = None
        assert self.service.authenticate_user("nobody@test.com", "pw") is False

    def test_authenticate_by_phone_fallback(self):
        mock_user = MagicMock()
        mock_user.password_hash = "hashed_pw"
        self.mock_repo.get_user_by_email.return_value = None
        self.mock_repo.get_user_by_phone.return_value = mock_user

        with patch("src.application.service_user.verify_password", return_value=True):
            result = self.service.authenticate_user("+380671234567", "pw123")

        assert result == mock_user

class TestPlaceService:
    def setup_method(self):
        self.mock_repo = MagicMock()
        self.service = PlaceService(self.mock_repo)

    def test_create_success(self):
        mock_place = MagicMock()
        mock_place.place_id = 1
        self.mock_repo.create.return_value = mock_place

        result = self.service.create_place("Вул. Дачна, 66", "09:00", "23:00", "shop")
        assert result.place_id == 1
        self.mock_repo.create.assert_called_once()

    def test_create_invalid_hours_raises(self):
        with pytest.raises(InvalidTimeRangeError):
            self.service.create_place("X", "23:00", "09:00", "cafe")

    def test_all_places(self):
        self.mock_repo.get_all_places.return_value = [MagicMock(), MagicMock()]
        assert len(self.service.all_places()) == 2

    def test_delete_success(self):
        self.mock_repo.delete.return_value = True
        assert self.service.delete_place(1) is True

    def test_delete_not_found(self):
        self.mock_repo.delete.return_value = False
        assert self.service.delete_place(999) is False

class TestReviewService:
    def setup_method(self):
        self.mock_repo = MagicMock()
        self.service = ReviewService(self.mock_repo)

    def test_create_success(self):
        mock_review = MagicMock()
        mock_review.review_id = 7
        self.mock_repo.create.return_value = mock_review

        result = self.service.create_review(place_id=1, user_id=2, content_in="Так собі")
        assert result.review_id == 7
        self.mock_repo.create.assert_called_once()

    def test_create_empty_raises(self):
        with pytest.raises((EmptyReviewError, TypeError)):
            self.service.create_review(place_id=1, user_id=2, content_in="")

    def test_all_reviews(self):
        self.mock_repo.get_all_reviews.return_value = [MagicMock()]
        assert len(self.service.all_review()) == 1

    def test_delete_success(self):
        self.mock_repo.delete.return_value = True
        assert self.service.delete_review(1) is True

    def test_delete_not_found(self):
        self.mock_repo.delete.return_value = False
        assert self.service.delete_review(999) is False
