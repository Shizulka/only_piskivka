
from src.domain.interfaces import ReviewRepositoryInterface
from src.domain.factory import ReviewFactory

class ReviewService:
    def __init__(self, review_repo: ReviewRepositoryInterface): 
        self.repository = review_repo

    def create_review(self, place_id: int, user_id: int, content_in: str):
        new_review = ReviewFactory.create_review( user_id=user_id, place_id=place_id, content_in=content_in)
        return self.repository.create(new_review)

    def all_review(self):
        return self.repository.get_all_reviews()

    def delete_review(self, review_id: int) -> bool:
        return self.repository.delete(review_id)