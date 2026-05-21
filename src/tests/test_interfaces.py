import pytest
from abc import ABC

from src.domain.interfaces import (
    UserRepositoryInterface,
    ReviewRepositoryInterface,
    PlaceRepositoryInterface,
)
from src.domain.entities import User, Place, Review
from src.domain.value_objects import Email, TimeRange

class ConcreteUserRepo(UserRepositoryInterface):
    def get_user_by_email(self, email): return None
    def get_user_by_phone(self, phone): return None
    def get_user_by_id(self, user_id): return None
    def create(self, user): return user
    def delete(self, user_id): return True

class ConcreteReviewRepo(ReviewRepositoryInterface):
    def create(self, review): return review
    def get_all_reviews(self): return []
    def get_by_id(self, review_id): return None
    def delete(self, review_id): return True

class ConcretePlaceRepo(PlaceRepositoryInterface):
    def create(self, place): return place
    def get_by_id(self, place_id): return None
    def get_all_places(self): return []
    def delete(self, place_id): return True

class TestUserRepositoryInterface:
    def test_is_abstract(self):
        assert issubclass(UserRepositoryInterface, ABC)

    def test_cannot_instantiate_abstract(self):
        with pytest.raises(TypeError):
            UserRepositoryInterface()

    def test_concrete_impl_is_instance(self):
        assert isinstance(ConcreteUserRepo(), UserRepositoryInterface)

    def test_missing_method_raises_type_error(self):
        class Incomplete(UserRepositoryInterface):
            def get_user_by_email(self, email): return None
            def get_user_by_phone(self, phone): return None

        with pytest.raises(TypeError):
            Incomplete()

    def test_get_user_by_email_returns_none_when_missing(self):
        repo = ConcreteUserRepo()
        assert repo.get_user_by_email("nobody@test.com") is None

    def test_get_user_by_phone_returns_none_when_missing(self):
        repo = ConcreteUserRepo()
        assert repo.get_user_by_phone("+380671234567") is None

    def test_get_user_by_id_returns_none_when_missing(self):
        repo = ConcreteUserRepo()
        assert repo.get_user_by_id(999) is None

    def test_create_returns_entity(self):
        user = User(
            user_name="Тест",
            email=Email("t@t.com"),
            password_hash="hash",
        )
        repo = ConcreteUserRepo()
        assert repo.create(user) is user

class TestReviewRepositoryInterface:
    def test_is_abstract(self):
        assert issubclass(ReviewRepositoryInterface, ABC)

    def test_cannot_instantiate_abstract(self):
        with pytest.raises(TypeError):
            ReviewRepositoryInterface()

    def test_concrete_impl_is_instance(self):
        assert isinstance(ConcreteReviewRepo(), ReviewRepositoryInterface)

    def test_missing_method_raises_type_error(self):
        class Incomplete(ReviewRepositoryInterface):
            def create(self, review): return review

        with pytest.raises(TypeError):
            Incomplete()

    def test_get_all_reviews_returns_list(self):
        assert ConcreteReviewRepo().get_all_reviews() == []

    def test_get_by_id_returns_none(self):
        assert ConcreteReviewRepo().get_by_id(1) is None

    def test_delete_returns_bool(self):
        assert ConcreteReviewRepo().delete(1) is True

class TestPlaceRepositoryInterface:
    def test_is_abstract(self):
        assert issubclass(PlaceRepositoryInterface, ABC)

    def test_cannot_instantiate_abstract(self):
        with pytest.raises(TypeError):
            PlaceRepositoryInterface()

    def test_concrete_impl_is_instance(self):
        assert isinstance(ConcretePlaceRepo(), PlaceRepositoryInterface)

    def test_missing_method_raises_type_error(self):
        class Incomplete(PlaceRepositoryInterface):
            def create(self, place): return place

        with pytest.raises(TypeError):
            Incomplete()

    def test_get_all_places_returns_list(self):
        assert ConcretePlaceRepo().get_all_places() == []

    def test_get_by_id_returns_none(self):
        assert ConcretePlaceRepo().get_by_id(1) is None

    def test_delete_returns_bool(self):
        assert ConcretePlaceRepo().delete(1) is True

    def test_create_returns_entity(self):
        place = Place(
            location="Вул. Тестова, 1",
            working_hours=TimeRange("09:00", "18:00"),
            status="bar",
        )
        assert ConcretePlaceRepo().create(place) is place