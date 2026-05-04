from pytest import Session
from src.infrastructure.models import Review
from src.repository.repo_place import ReviewRepository

class ReviewService:
    def __init__(self, db:Session):
        self.repository = ReviewRepository(db , Review)
        self.db = db

    