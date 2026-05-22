import pytest
from unittest.mock import MagicMock

from src.modules.core.infrastructure.mappers import UserMapper, PlaceMapper, ReviewMapper
from src.modules.core.infrastructure.models import Users as DBUser, Place as DBPlace, Review as DBReview
from src.modules.core.domain.entities import User as DomainUser, Place as DomainPlace, Review as DomainReview
from src.modules.core.domain.value_objects import Email, TimeRange

class TestUserMapper:
    def _db_user(self, **kwargs):
        u = MagicMock(spec=DBUser)
        u.user_id = kwargs.get("user_id", 1)
        u.user_name = kwargs.get("user_name", "Аліса")
        u.email = kwargs.get("email", "alice@test.com")
        u.password = kwargs.get("password", "hashed")
        u.phone_number = kwargs.get("phone_number", None)
        u.status = kwargs.get("status", "cool")
        u.is_admin = kwargs.get("is_admin", False)
        return u

    def test_to_domain_maps_fields(self):
        db = self._db_user()
        domain = UserMapper.to_domain(db)

        assert isinstance(domain, DomainUser)
        assert domain.user_id == 1
        assert domain.user_name == "Аліса"
        assert domain.email.value == "alice@test.com"
        assert domain.password_hash == "hashed"
        assert domain.is_admin is False

    def test_to_domain_preserves_phone(self):
        db = self._db_user(phone_number="+380671234567")
        domain = UserMapper.to_domain(db)
        assert domain.phone_number == "+380671234567"

    def test_to_domain_admin_flag(self):
        db = self._db_user(is_admin=True)
        assert UserMapper.to_domain(db).is_admin is True

    def test_to_domain_none_returns_none(self):
        assert UserMapper.to_domain(None) is None

    def test_to_db_maps_fields(self):
        domain = DomainUser(
            user_id=5,
            user_name="Борис",
            email=Email("borys@test.com"),
            password_hash="secret_hash",
            phone_number="+380991234567",
            status="cool",
            is_admin=False,
        )
        db = UserMapper.to_db(domain)

        assert isinstance(db, DBUser)
        assert db.user_id == 5
        assert db.user_name == "Борис"
        assert db.email == "borys@test.com"
        assert db.password == "secret_hash"
        assert db.phone_number == "+380991234567"
        assert db.is_admin is False

    def test_roundtrip_to_db_then_to_domain(self):
        original = DomainUser(
            user_id=3,
            user_name="Галина",
            email=Email("halyna@test.com"),
            password_hash="h",
            phone_number=None,
            status="cool",
            is_admin=False,
        )
        db_obj = UserMapper.to_db(original)

        mock_db = MagicMock(spec=DBUser)
        mock_db.user_id = db_obj.user_id
        mock_db.user_name = db_obj.user_name
        mock_db.email = db_obj.email
        mock_db.password = db_obj.password
        mock_db.phone_number = db_obj.phone_number
        mock_db.status = db_obj.status
        mock_db.is_admin = db_obj.is_admin

        restored = UserMapper.to_domain(mock_db)
        assert restored.user_name == original.user_name
        assert restored.email.value == original.email.value
        assert restored.password_hash == original.password_hash

class TestPlaceMapper:
    def _db_place(self, **kwargs):
        p = MagicMock(spec=DBPlace)
        p.place_id = kwargs.get("place_id", 10)
        p.location = kwargs.get("location", "Вул. Лісова, 5")
        p.open = kwargs.get("open", "09:00")
        p.close = kwargs.get("close", "21:00")
        p.type_place = kwargs.get("type_place", "bar")
        return p

    def test_to_domain_maps_fields(self):
        db = self._db_place()
        domain = PlaceMapper.to_domain(db)

        assert isinstance(domain, DomainPlace)
        assert domain.place_id == 10
        assert domain.location == "Вул. Лісова, 5"
        assert domain.working_hours.open_time == "09:00"
        assert domain.working_hours.close_time == "21:00"
        assert domain.status == "bar"

    def test_to_domain_none_returns_none(self):
        assert PlaceMapper.to_domain(None) is None

    def test_to_db_maps_fields(self):
        domain = DomainPlace(
            place_id=7,
            location="Пл. Соборна, 1",
            working_hours=TimeRange("10:00", "22:00"),
            status="cafe",
        )
        db = PlaceMapper.to_db(domain)

        assert isinstance(db, DBPlace)
        assert db.place_id == 7
        assert db.location == "Пл. Соборна, 1"
        assert db.open == "10:00"
        assert db.close == "22:00"
        assert db.type_place == "cafe"

    def test_to_db_none_place_id(self):
        domain = DomainPlace(
            place_id=None,
            location="Нове місце",
            working_hours=TimeRange("08:00", "18:00"),
            status="shop",
        )
        db = PlaceMapper.to_db(domain)
        assert db.place_id is None

    def test_roundtrip_to_db_then_to_domain(self):
        original = DomainPlace(
            place_id=2,
            location="Вул. Козацька",
            working_hours=TimeRange("11:00", "20:00"),
            status="bar",
        )
        db_obj = PlaceMapper.to_db(original)

        mock_db = MagicMock(spec=DBPlace)
        mock_db.place_id = db_obj.place_id
        mock_db.location = db_obj.location
        mock_db.open = db_obj.open
        mock_db.close = db_obj.close
        mock_db.type_place = db_obj.type_place

        restored = PlaceMapper.to_domain(mock_db)
        assert restored.location == original.location
        assert restored.working_hours.open_time == original.working_hours.open_time
        assert restored.status == original.status

class TestReviewMapper:
    def _db_review(self, **kwargs):
        r = MagicMock(spec=DBReview)
        r.review_id = kwargs.get("review_id", 20)
        r.place_id = kwargs.get("place_id", 1)
        r.user_id = kwargs.get("user_id", 2)
        r.content_in = kwargs.get("content_in", "Чудово!")
        return r

    def test_to_domain_maps_fields(self):
        db = self._db_review()
        domain = ReviewMapper.to_domain(db)

        assert isinstance(domain, DomainReview)
        assert domain.review_id == 20
        assert domain.place_id == 1
        assert domain.user_id == 2
        assert domain.content_in == "Чудово!"

    def test_to_domain_none_returns_none(self):
        assert ReviewMapper.to_domain(None) is None

    def test_to_db_maps_fields(self):
        domain = DomainReview(
            review_id=None,
            place_id=3,
            user_id=4,
            content_in="Непогано",
        )
        db = ReviewMapper.to_db(domain)

        assert isinstance(db, DBReview)
        assert db.review_id is None
        assert db.place_id == 3
        assert db.user_id == 4
        assert db.content_in == "Непогано"

    def test_roundtrip_to_db_then_to_domain(self):
        original = DomainReview(
            review_id=5,
            place_id=1,
            user_id=1,
            content_in="Все добре",
        )
        db_obj = ReviewMapper.to_db(original)

        mock_db = MagicMock(spec=DBReview)
        mock_db.review_id = db_obj.review_id
        mock_db.place_id = db_obj.place_id
        mock_db.user_id = db_obj.user_id
        mock_db.content_in = db_obj.content_in

        restored = ReviewMapper.to_domain(mock_db)
        assert restored.content_in == original.content_in
        assert restored.review_id == original.review_id