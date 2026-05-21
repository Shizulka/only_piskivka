from dataclasses import dataclass
import datetime


@dataclass(frozen=True)
class UserRegisteredEvent:
    user_id: int
    email: str