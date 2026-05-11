from dataclasses import dataclass
from typing import Optional
from  src.domain.value_objects import TimeRange, Email
from  src.domain.exceptions import EmptyReviewError

@dataclass
class User:
    user_name: str
    email: Email
    password_hash: str
    phone_number: Optional[str] = None
    status: str = "cool"
    is_admin: bool = False
    user_id: Optional[int] = None 

@dataclass
class Place:
    location: str
    working_hours: TimeRange 
    status: str
    place_id: Optional[int] = None

@dataclass
class Review:
    place_id: int
    user_id: int
    content_in: str
    review_id: Optional[int] = None

    def __post_init__(self):
        if not self.content_in or not self.content_in.strip():
            raise EmptyReviewError()