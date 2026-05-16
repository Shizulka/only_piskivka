from src.domain.interfaces import ReviewRepositoryInterface
from src.application.queries.review_query import GetAllReviewQuery
from src.application.read_model.review_read_model import ReviewReadModel

class GetAllReviewsHandler:
    def __init__(self, review_repo: ReviewRepositoryInterface):
        self.repository = review_repo

    def handle(self, query: GetAllReviewQuery):
        reviews = self.repository.get_all_reviews()

        return [
            ReviewReadModel(review_id=review.review_id,user_id=review.user_id,place_id=review.place_id,content_in=review.content_in)
            
            for review in reviews
        ]