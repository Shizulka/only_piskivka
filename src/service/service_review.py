from fastapi import HTTPException
from pytest import Session
from src.infrastructure.models import Review
from src.repository.repo_review import ReviewRepository

class ReviewService:
    def __init__(self, db:Session):
        self.repository = ReviewRepository(db , Review)
        self.db = db

    def craete_review (self, place_id: int , user_id : int  ,content_in : str ):
        new_review = Review (place_id = place_id , user_id=user_id ,content_in = content_in)

        return self.repository.create (new_review)
    
    def all_review  (self): 
        return self.db.query(Review ).all()
    
    def delete_review(self , review_id : int ):
        review = self.repository.db.query(Review).filter(Review.review_id == review_id).first()

        if review is None:
            raise HTTPException(status_code=404, detail="Review not found")

        return self.repository.delete(review)
