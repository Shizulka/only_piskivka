
from dataclasses import dataclass
from  src.domain.exceptions import InvalidTimeRangeError, InvalidEmailError

@dataclass(frozen=True)
class TimeRange:
    open_time: str
    close_time: str

    def __post_init__(self):
        if self.open_time >= self.close_time:
            raise InvalidTimeRangeError()

@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if "@" not in self.value or "." not in self.value:
            raise InvalidEmailError()