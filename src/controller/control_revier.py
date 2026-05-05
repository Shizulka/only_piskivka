from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.service.service_review import ReviewService
from src.infrastructure.database import get_db
from src.infrastructure.dependencies import get_current_user
from src.infrastructure.models import Users


router = APIRouter(prefix="/review", tags=["Review"])

@router.post("/create")
def create_review( place_id: int, content_in: str,db: Session = Depends(get_db),  current_user: Users = Depends(get_current_user) ):
    service = ReviewService(db)
    
    return service.craete_review(place_id=place_id,  user_id=current_user.user_id, content_in=content_in )

@router.post("/delete")
def delete_review(review_id : int  ,db: Session = Depends(get_db),  current_user: Users = Depends(get_current_user)):
    service = ReviewService(db)

    return service.delete_review(review_id=review_id)

@router.post("/all")
def all_review  ( db: Session = Depends (get_db) , current_user: Users = Depends(get_current_user)):
    service = ReviewService(db) 
    review = service.all_review()
    result = [{"id": r.review_id,"place": r.place_id , "user": r.user_id , "conteny_in": r.content_in } for r in review]
    return result