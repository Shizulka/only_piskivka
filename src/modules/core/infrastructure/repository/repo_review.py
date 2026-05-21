from typing import List, Optional

from sqlalchemy.orm import Session
from src.modules.core.domain.interfaces import ReviewRepositoryInterface
from src.modules.core.infrastructure.models import Review as DBReview
from src.modules.core.infrastructure.mappers import ReviewMapper
from src.modules.core.domain.entities import Review as DomainReview

class ReviewRepository(ReviewRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_all_reviews(self) -> List[DomainReview]:
        db_reviews = self.db.query(DBReview).all()
        return [ReviewMapper.to_domain(review) for review in db_reviews]
    
    
    def get_by_id(self, review_id: int) -> Optional[DomainReview]:
        db_review = self.db.query(DBReview).filter(DBReview.review_id == review_id).first()
        return ReviewMapper.to_domain(db_review)
    

    def create(self, domain_review: DomainReview) -> DomainReview:
        db_review = ReviewMapper.to_db(domain_review)
    
        self.db.add(db_review)
        self.db.commit()
        self.db.refresh(db_review)

        return ReviewMapper.to_domain(db_review)

    def  delete(self, review_id: int) -> bool:
        db_review = self.db.query(DBReview).filter(DBReview.review_id == review_id).first()

        if db_review:
            self.db.delete(db_review)
            self.db.commit()
            return True
        
        return False