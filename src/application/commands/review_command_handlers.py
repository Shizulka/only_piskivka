
from src.application.audit.audit_service import AuditServiceInterface
from src.application.event.event_bus import EventBus
from src.application.event.review_event import ReviewCreatedEvent, ReviewDeletedEvent
from src.domain.factory import ReviewFactory
from src.domain.interfaces import ReviewRepositoryInterface
from src.application.commands.review_command import ( CreateReviewCommand, DeleteReviewCommand)

class CreateReviewHandler:
    def __init__( self,review_repo: ReviewRepositoryInterface,audit_service: AuditServiceInterface = None,event_bus: EventBus = None, use_async: bool = False):
        self.repository = review_repo
        self.audit_service = audit_service
        self.event_bus = event_bus
        self.use_async = use_async

    def handle(self, command: CreateReviewCommand):
        new_review = ReviewFactory.create_review( user_id=command.user_id, place_id=command.place_id,content_in=command.content_in)
        created_review = self.repository.create(new_review)

        if self.use_async and self.event_bus:
            event = ReviewCreatedEvent(review_id=created_review.review_id, user_id=command.user_id,place_id=command.place_id,content_in=command.content_in)
            self.event_bus.publish(event)

        elif self.audit_service:
            try:
                self.audit_service.log_review_created(review_id=created_review.review_id,user_id=command.user_id,place_id=command.place_id)
            except Exception:
                pass

        return created_review.review_id

class DeleteReviewHandler:
    def __init__(self,review_repo: ReviewRepositoryInterface,audit_service: AuditServiceInterface = None,event_bus: EventBus = None,use_async: bool = False):
        self.repository = review_repo
        self.audit_service = audit_service
        self.event_bus = event_bus
        self.use_async = use_async

    def handle(self, command: DeleteReviewCommand):
        self.repository.delete(command.review_id)

        if self.use_async and self.event_bus:
            event = ReviewDeletedEvent(review_id=command.review_id,user_id=command.user_id)
            self.event_bus.publish(event)

        elif self.audit_service:
            try:
                self.audit_service.log_review_deleted(review_id=command.review_id,user_id=command.user_id)
            except Exception:
                pass