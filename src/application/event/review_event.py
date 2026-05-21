from dataclasses import dataclass
import datetime


@dataclass(frozen=True)
class ReviewCreatedEvent:
    review_id: int
    user_id: int
    place_id: int
    content_in: str


@dataclass(frozen=True)
class ReviewDeletedEvent:
    review_id: int
    user_id: int
