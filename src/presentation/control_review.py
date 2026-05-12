from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.infrastructure.repository.repo_review import ReviewRepository
from src.infrastructure.database import get_db
from src.infrastructure.dependencies import get_current_user
from src.application.service_review import ReviewService
from src.domain.exceptions import DomainError

router = APIRouter(prefix="/review", tags=["Reviews"])

def get_review_repo(db: Session = Depends(get_db)):
    return ReviewRepository(db)


@router.post("/create")
def create_new_review( place_id: int,  content_in: str,  current_user = Depends(get_current_user), review_repo = Depends(get_review_repo) 
):
    service = ReviewService(review_repo) 
    
    try:
        new_review = service.create_review( place_id=place_id, user_id=current_user.user_id, content_in=content_in)
        return {"review_id": new_review.review_id, "place_id": new_review.place_id, "user_id": new_review.user_id,"content_in": new_review.content_in,"message": "Відгук успішно додано"
        }
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/all")
def all_reviews(review_repo = Depends(get_review_repo)):
    service = ReviewService(review_repo)
    reviews = service.all_review()
    
    return [
        {
            "id": r.review_id, 
            "place": r.place_id, 
            "user": r.user_id, 
            "content_in": r.content_in
        } for r in reviews
    ]


@router.delete("/{review_id}")
def delete_review( review_id: int,  current_user = Depends(get_current_user), review_repo = Depends(get_review_repo) ):
    service = ReviewService(review_repo)
    success = service.delete_review(review_id)
    
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Відгук не знайдено")
        
    return {"message": "Відгук успішно видалено"}