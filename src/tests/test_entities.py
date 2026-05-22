import pytest

from src.modules.core.domain.entities import User, Place, Review
from src.modules.core.domain.value_objects import Email, TimeRange
from src.modules.core.domain.exceptions import EmptyReviewError


class TestUser:
    def test_create_with_defaults(self):
        user = User(user_name="аліса", email=Email("a@b.com"), password_hash="hash")
        assert user.user_name == "аліса"
        assert user.status == "cool"
        assert user.is_admin is False
        assert user.user_id is None

    def test_create_with_all_fields(self):
        user = User(
            user_name="Admin",
            email=Email("admin@b.com"),
            password_hash="hash",
            phone_number="+380671234567",
            status="vip",
            is_admin=True,
            user_id=99,
        )
        assert user.is_admin is True
        assert user.user_id == 99
        assert user.phone_number == "+380671234567"


class TestPlace:
    def test_create(self):
        place = Place(
            location="Вул. Шкільна, 2а",
            working_hours=TimeRange("14:00", "19:00"),
            status="cafe",
        )
        assert place.location == "Вул. Шкільна, 2а"
        assert place.status == "cafe"
        assert place.place_id is None


class TestReview:
    def test_create_valid(self):
        review = Review(place_id=1, user_id=2, content_in="Смачно та недорого")
        assert review.content_in == "Смачно та недорого"
        assert review.review_id is None

    def test_empty_content_raises(self):
        with pytest.raises(EmptyReviewError):
            Review(place_id=1, user_id=2, content_in="")

    def test_whitespace_only_raises(self):
        with pytest.raises(EmptyReviewError):
            Review(place_id=1, user_id=2, content_in="   ")
