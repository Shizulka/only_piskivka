import pytest
from unittest.mock import MagicMock

from src.modules.core.domain.factory import UserFactory, PlaceFactory, ReviewFactory
from src.modules.core.domain.exceptions import (
    UserAlreadyExistsError,
    InvalidEmailError,
    InvalidTimeRangeError,
    EmptyReviewError,
)

class TestUserFactory:
    def setup_method(self):
        self.mock_repo = MagicMock()
        self.factory = UserFactory(self.mock_repo)

    def test_create_success(self):
        self.mock_repo.get_user_by_email.return_value = None
        user = self.factory.create_user("Іван", "iwan@example.com", "hashed_pw")
        assert user.user_name == "Іван"
        assert user.email.value == "iwan@example.com"

    def test_duplicate_email_raises(self):
        self.mock_repo.get_user_by_email.return_value = MagicMock()
        with pytest.raises(UserAlreadyExistsError):
            self.factory.create_user("Іван", "iwan@example.com", "pw")

    def test_invalid_email_raises(self):
        self.mock_repo.get_user_by_email.return_value = None
        with pytest.raises(InvalidEmailError):
            self.factory.create_user("Іван", "notanemail", "pw")

class TestPlaceFactory:
    def test_create_success(self):
        place = PlaceFactory.create_place("Вул. Лісова ,??", "08:00", "22:00", "bar")
        assert place.location == "Вул. Лісова ,??"
        assert place.working_hours.open_time == "08:00"

    def test_invalid_hours_raises(self):
        with pytest.raises(InvalidTimeRangeError):
            PlaceFactory.create_place("Десь", "22:00", "08:00", "cafe")

class TestReviewFactory:
    def test_create_success(self):
        review = ReviewFactory.create_review(user_id=1, place_id=2, content_in="Класно")
        assert review.content_in == "Класно"
        assert review.user_id == 1
        assert review.place_id == 2

    def test_empty_content_raises(self):
        with pytest.raises((EmptyReviewError, TypeError)):
            ReviewFactory.create_review(user_id=1, place_id=2, content_in="")

    def test_whitespace_content_raises(self):
        with pytest.raises((EmptyReviewError, TypeError)):
            ReviewFactory.create_review(user_id=1, place_id=2, content_in="   ")
