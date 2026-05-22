import pytest

from src.modules.core.domain.value_objects import Email, TimeRange, PlaceStatus
from src.modules.core.domain.exceptions import InvalidEmailError, InvalidTimeRangeError

class TestEmail:
    def test_valid_email(self):
        email = Email("test@example.com")
        assert email.value == "test@example.com"

    def test_missing_at_raises(self):
        with pytest.raises(InvalidEmailError):
            Email("invalidemail.com")

    def test_missing_dot_raises(self):
        with pytest.raises(InvalidEmailError):
            Email("invalid@emailcom")

    def test_no_special_chars_raises(self):
        with pytest.raises(InvalidEmailError):
            Email("notanemail")

    def test_is_frozen(self):
        email = Email("test@example.com")
        with pytest.raises(Exception):
            email.value = "other@example.com"

class TestTimeRange:
    def test_valid_range(self):
        tr = TimeRange("08:00", "20:00")
        assert tr.open_time == "08:00"
        assert tr.close_time == "20:00"

    def test_open_equals_close_raises(self):
        with pytest.raises(InvalidTimeRangeError):
            TimeRange("10:00", "10:00")

    def test_open_after_close_raises(self):
        with pytest.raises(InvalidTimeRangeError):
            TimeRange("22:00", "08:00")

    def test_is_frozen(self):
        tr = TimeRange("08:00", "20:00")
        with pytest.raises(Exception):
            tr.open_time = "09:00"

class TestPlaceStatus:
    def test_values(self):
        assert PlaceStatus.OPEN == "bar"
        assert PlaceStatus.CLOSED == "cafe"
        assert PlaceStatus.MAINTENANCE == "shop"
