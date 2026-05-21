from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.modules.core.infrastructure.repository.repo_review import ReviewRepository
from src.modules.core.infrastructure.database import get_db
from src.modules.core.infrastructure.dependencies import get_current_user
from src.modules.core.domain.exceptions import DomainError
from src.shared.event_bus import event_bus
from src.modules.core.application.commands.review_command import ( CreateReviewCommand, DeleteReviewCommand)
from src.modules.core.application.commands.review_command_handlers import (  CreateReviewHandler, DeleteReviewHandler)
from src.modules.core.application.queries.review_query import GetAllReviewQuery
from src.modules.core.application.queries.review_query_handlers import GetAllReviewsHandler
from src.modules.core.application.audit.audit_service import ConsoleAuditService
from src.modules.core.application.audit.audit_handlers import ReviewCreatedAuditHandler, ReviewDeletedAuditHandler
from src.shared.event_bus import EventBus
from src.modules.core.application.event.review_event import ReviewCreatedEvent, ReviewDeletedEvent

router = APIRouter(prefix="/review", tags=["Reviews"])

def get_review_repo(db: Session = Depends(get_db)):
    return ReviewRepository(db)


@router.post("/create")
async def create_new_review(place_id: int,content_in: str,current_user=Depends(get_current_user),review_repo=Depends(get_review_repo)):
    handler = CreateReviewHandler(review_repo=review_repo,event_bus=event_bus)
    command = CreateReviewCommand( place_id=place_id,user_id=current_user.user_id,content_in=content_in)
    try:
        review_id = await handler.handle(command)
        return { "review_id": review_id, "place_id": place_id,"user_id": current_user.user_id,"content_in": content_in,"message": "Відгук успішно додано"}
    except DomainError as e:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/all")
def all_reviews(review_repo=Depends(get_review_repo)):
    handler = GetAllReviewsHandler(review_repo)
    query = GetAllReviewQuery()

    return handler.handle(query)


@router.delete("/{review_id}")
async def delete_review(review_id: int,current_user=Depends(get_current_user),review_repo=Depends(get_review_repo)):
    handler = DeleteReviewHandler(review_repo=review_repo,event_bus=event_bus)

    command = DeleteReviewCommand(review_id=review_id, user_id=current_user.user_id )

    try:
        await handler.handle(command)

        return {
            "message": "Відгук успішно видалено"
        }

    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )