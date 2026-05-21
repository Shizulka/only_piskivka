from dataclasses import dataclass

@dataclass
class ReviewReadModel:
    review_id: int
    place_id: int
    user_id: int
    content_in: str