from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.infrastructure.repository.repo_review import ReviewRepository
from src.infrastructure.database import get_db
from src.infrastructure.dependencies import get_current_user
from src.domain.exceptions import DomainError

from src.application.commands.review_command import ( CreateReviewCommand, DeleteReviewCommand)
from src.application.commands.review_command_handlers import (  CreateReviewHandler, DeleteReviewHandler)
from src.application.queries.review_query import GetAllReviewQuery
from src.application.queries.review_query_handlers import GetAllReviewsHandler
from src.application.audit.audit_service import ConsoleAuditService
from src.application.audit.audit_handlers import ReviewCreatedAuditHandler, ReviewDeletedAuditHandler
from src.application.event.event_bus import EventBus
from src.application.event.review_event import ReviewCreatedEvent, ReviewDeletedEvent

router = APIRouter(prefix="/review", tags=["Reviews"])

def get_review_repo(db: Session = Depends(get_db)):
    return ReviewRepository(db)


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_new_review( place_id: int,  content_in: str,  current_user=Depends(get_current_user),  review_repo=Depends(get_review_repo)):
    command = CreateReviewCommand( place_id=place_id,  user_id=current_user.user_id, content_in=content_in)

    audit_service = ConsoleAuditService()
    event_bus = EventBus()
    event_bus.subscribe(ReviewCreatedEvent, ReviewCreatedAuditHandler(audit_service))


    handler = CreateReviewHandler(review_repo=review_repo,audit_service=audit_service,event_bus=event_bus,use_async=True )
    try:
        created_id = handler.handle(command)
        return {
            "review_id": created_id,
            "message": "Відгук успішно додано"
        }
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/all")
def all_reviews(review_repo=Depends(get_review_repo)):
    handler = GetAllReviewsHandler(review_repo)
    query = GetAllReviewQuery()

    return handler.handle(query)


@router.delete("/{review_id}")
def delete_review(review_id: int,current_user=Depends(get_current_user),review_repo=Depends(get_review_repo)):
    audit_service = ConsoleAuditService()
    event_bus = EventBus()

    event_bus.subscribe(ReviewCreatedEvent,ReviewCreatedAuditHandler(audit_service))

    event_bus.subscribe(ReviewDeletedEvent,ReviewDeletedAuditHandler(audit_service))

    handler = DeleteReviewHandler( review_repo=review_repo, audit_service=audit_service,event_bus=event_bus, use_async=True)

    command = DeleteReviewCommand( review_id=review_id,user_id=current_user.user_id)

    handler.handle(command)

    return {"message": "Відгук успішно видалено"}