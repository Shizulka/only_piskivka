import pytest
from unittest.mock import MagicMock, patch, call

from src.modules.core.infrastructure.repository.repo_place import PlaceRepository
from src.modules.core.infrastructure.repository.repo_review import ReviewRepository
from src.modules.core.infrastructure.repository.repo_user import UserRepository
from src.modules.core.infrastructure.models import Place as DBPlace, Review as DBReview, Users as DBUser
from src.modules.core.domain.entities import Place as DomainPlace, Review as DomainReview, User as DomainUser
from src.modules.core.domain.value_objects import Email, TimeRange


def _mock_db():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None
    db.query.return_value.all.return_value = []
    return db

class TestPlaceRepository:
    def setup_method(self):
        self.db = _mock_db()
        self.repo = PlaceRepository(self.db)

    def _domain_place(self, place_id=None):
        return DomainPlace(
            place_id=place_id,
            location="Вул. Тестова, 1",
            working_hours=TimeRange("09:00", "18:00"),
            status="bar",
        )

    def test_create_adds_commits_refreshes(self):
        domain = self._domain_place()
        def fake_refresh(obj):
            obj.place_id = 42
            obj.location = domain.location
            obj.open = domain.working_hours.open_time
            obj.close = domain.working_hours.close_time
            obj.type_place = domain.status
        self.db.refresh.side_effect = fake_refresh

        result = self.repo.create(domain)

        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        assert result.place_id == 42

    def test_get_by_id_found(self):
        db_place = MagicMock(spec=DBPlace)
        db_place.place_id = 5
        db_place.location = "Вул. Центральна, 3"
        db_place.open = "10:00"
        db_place.close = "20:00"
        db_place.type_place = "cafe"
        self.db.query.return_value.filter.return_value.first.return_value = db_place

        result = self.repo.get_by_id(5)

        assert result is not None
        assert result.place_id == 5
        assert result.location == "Вул. Центральна, 3"

    def test_get_by_id_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None
        result = self.repo.get_by_id(999)
        assert result is None

    def test_get_all_places_empty(self):
        self.db.query.return_value.all.return_value = []
        assert self.repo.get_all_places() == []

    def test_get_all_places_returns_mapped_list(self):
        db_place = MagicMock(spec=DBPlace)
        db_place.place_id = 1
        db_place.location = "Вул. А"
        db_place.open = "08:00"
        db_place.close = "22:00"
        db_place.type_place = "bar"
        self.db.query.return_value.all.return_value = [db_place]

        result = self.repo.get_all_places()
        assert len(result) == 1
        assert result[0].location == "Вул. А"

    def test_delete_existing_returns_true(self):
        db_place = MagicMock(spec=DBPlace)
        self.db.query.return_value.filter.return_value.first.return_value = db_place

        result = self.repo.delete(1)

        assert result is True
        self.db.delete.assert_called_once_with(db_place)
        self.db.commit.assert_called_once()

    def test_delete_missing_returns_false(self):
        self.db.query.return_value.filter.return_value.first.return_value = None
        result = self.repo.delete(999)
        assert result is False
        self.db.delete.assert_not_called()

class TestReviewRepository:
    def setup_method(self):
        self.db = _mock_db()
        self.repo = ReviewRepository(self.db)

    def _domain_review(self, review_id=None):
        return DomainReview(place_id=1, user_id=2, content_in="Чудово!", review_id=review_id)

    def test_create_adds_commits_refreshes(self):
        domain = self._domain_review()

        def fake_refresh(obj):
            obj.review_id = 7
            obj.place_id = domain.place_id
            obj.user_id = domain.user_id
            obj.content_in = domain.content_in
        self.db.refresh.side_effect = fake_refresh

        result = self.repo.create(domain)

        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        assert result.review_id == 7

    def test_get_all_reviews_empty(self):
        self.db.query.return_value.all.return_value = []
        assert self.repo.get_all_reviews() == []

    def test_get_all_reviews_returns_mapped_list(self):
        db_review = MagicMock(spec=DBReview)
        db_review.review_id = 1
        db_review.place_id = 2
        db_review.user_id = 3
        db_review.content_in = "Непогано"
        self.db.query.return_value.all.return_value = [db_review]

        result = self.repo.get_all_reviews()
        assert len(result) == 1
        assert result[0].content_in == "Непогано"

    def test_get_by_id_found(self):
        db_review = MagicMock(spec=DBReview)
        db_review.review_id = 3
        db_review.place_id = 1
        db_review.user_id = 1
        db_review.content_in = "OK"
        self.db.query.return_value.filter.return_value.first.return_value = db_review

        result = self.repo.get_by_id(3)
        assert result is not None
        assert result.review_id == 3

    def test_get_by_id_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None
        assert self.repo.get_by_id(999) is None

    def test_delete_existing_returns_true(self):
        db_review = MagicMock(spec=DBReview)
        self.db.query.return_value.filter.return_value.first.return_value = db_review

        result = self.repo.delete(3)

        assert result is True
        self.db.delete.assert_called_once_with(db_review)
        self.db.commit.assert_called_once()

    def test_delete_missing_returns_false(self):
        self.db.query.return_value.filter.return_value.first.return_value = None
        result = self.repo.delete(999)
        assert result is False
        self.db.delete.assert_not_called()

class TestUserRepository:
    def setup_method(self):
        self.db = _mock_db()
        self.repo = UserRepository(self.db)

    def _db_user(self, user_id=1):
        u = MagicMock(spec=DBUser)
        u.user_id = user_id
        u.user_name = "Тест"
        u.email = "test@test.com"
        u.password = "hashed"
        u.phone_number = None
        u.status = "cool"
        u.is_admin = False
        return u

    def test_get_user_by_email_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = self._db_user()
        result = self.repo.get_user_by_email("test@test.com")
        assert result is not None
        assert result.email.value == "test@test.com"

    def test_get_user_by_email_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None
        assert self.repo.get_user_by_email("nope@test.com") is None

    def test_get_user_by_phone_found(self):
        u = self._db_user()
        u.phone_number = "+380671234567"
        self.db.query.return_value.filter.return_value.first.return_value = u
        result = self.repo.get_user_by_phone("+380671234567")
        assert result is not None

    def test_get_user_by_phone_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None
        assert self.repo.get_user_by_phone("+380000000000") is None

    def test_get_user_by_id_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = self._db_user(user_id=9)
        result = self.repo.get_user_by_id(9)
        assert result is not None
        assert result.user_id == 9

    def test_get_user_by_id_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None
        assert self.repo.get_user_by_id(9999) is None

    def test_create_adds_commits_refreshes(self):
        domain = DomainUser(
            user_id=None,
            user_name="Новий",
            email=Email("new@test.com"),
            password_hash="hashed",
        )

        def fake_refresh(obj):
            obj.user_id = 15
            obj.user_name = domain.user_name
            obj.email = domain.email.value
            obj.password = domain.password_hash
            obj.phone_number = None
            obj.status = "cool"
            obj.is_admin = False
        self.db.refresh.side_effect = fake_refresh

        result = self.repo.create(domain)

        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        assert result.user_id == 15
        assert result.user_name == "Новий"