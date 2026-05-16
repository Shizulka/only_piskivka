from dataclasses import dataclass

@dataclass
class CreateReviewCommand:
    place_id: int
    user_id: int
    content_in: str

@dataclass
class DeleteReviewCommand:
    review_id: int