from src.domain.factory import ReviewFactory
from src.domain.interfaces import ReviewRepositoryInterface
from src.application.commands.review_command import ( CreateReviewCommand, DeleteReviewCommand)

class CreateReviewHandler:
    def __init__(self, review_repo: ReviewRepositoryInterface):
        self.repository = review_repo

    def handle(self, command: CreateReviewCommand):

        new_review = ReviewFactory.create_review(user_id=command.user_id,place_id=command.place_id,content_in=command.content_in)

        created_review = self.repository.create(new_review)

        return created_review.review_id


class DeleteReviewHandler:
    def __init__(self, review_repo: ReviewRepositoryInterface):
        self.repository = review_repo

    def handle(self, command: DeleteReviewCommand):
        self.repository.delete(command.review_id)