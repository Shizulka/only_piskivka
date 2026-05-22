import pytest
from pydantic import ValidationError

from src.modules.core.infrastructure.schemas import UserCreate, UserOut

class TestUserCreate:
    def test_valid_with_email(self):
        u = UserCreate(user_name="Аліса", email="alice@test.com", password="password123")
        assert u.user_name == "Аліса"
        assert str(u.email) == "alice@test.com"

    def test_valid_with_phone(self):
        u = UserCreate(user_name="Борис", phone_number="0671234567", password="password123")
        assert u.phone_number == "0671234567"

    def test_valid_with_both_email_and_phone(self):
        u = UserCreate(
            user_name="Галина",
            email="g@test.com",
            phone_number="0671234567",
            password="password123",
        )
        assert u.email is not None
        assert u.phone_number is not None

    def test_missing_both_email_and_phone_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(user_name="Аліса", password="password123")
        errors = exc_info.value.errors()
        assert any("email" in str(e).lower() or "телефон" in str(e).lower() for e in errors)

    def test_username_too_short_raises(self):
        with pytest.raises(ValidationError):
            UserCreate(user_name="Ab", email="a@test.com", password="password123")

    def test_username_too_long_raises(self):
        with pytest.raises(ValidationError):
            UserCreate(user_name="A" * 51, email="a@test.com", password="password123")

    def test_password_too_short_raises(self):
        with pytest.raises(ValidationError):
            UserCreate(user_name="Аліса", email="a@test.com", password="short")

    def test_password_too_long_raises(self):
        with pytest.raises(ValidationError):
            UserCreate(user_name="Аліса", email="a@test.com", password="x" * 73)

    def test_invalid_email_raises(self):
        with pytest.raises(ValidationError):
            UserCreate(user_name="Аліса", email="notanemail", password="password123")

    def test_invalid_phone_format_raises(self):
        with pytest.raises(ValidationError):
            UserCreate(user_name="Аліса", phone_number="12345", password="password123")

    def test_phone_with_country_code(self):
        u = UserCreate(user_name="Дмитро", phone_number="+380671234567", password="password123")
        assert u.phone_number == "+380671234567"

    def test_phone_with_38_prefix(self):
        u = UserCreate(user_name="Дмитро", phone_number="380671234567", password="password123")
        assert u.phone_number is not None

class TestUserOut:
    def test_serialises_from_orm(self):
        from unittest.mock import MagicMock
        obj = MagicMock()
        obj.user_id = 5
        obj.user_name = "Тест"
        obj.email = "t@t.com"
        obj.phone_number = None

        out = UserOut.model_validate(obj)
        assert out.user_id == 5
        assert out.user_name == "Тест"

    def test_optional_fields_are_none(self):
        out = UserOut(user_id=1, user_name="Тест")
        assert out.email is None
        assert out.phone_number is None