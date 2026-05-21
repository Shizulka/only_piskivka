
from src.modules.core.domain.exceptions import DomainError
from src.modules.core.application.audit.audit_service import AuditServiceInterface
from src.shared.event_bus import EventBus
from src.modules.core.application.event.review_event import ReviewCreatedEvent, ReviewDeletedEvent
from src.modules.core.domain.factory import ReviewFactory
from src.modules.core.domain.interfaces import ReviewRepositoryInterface
from src.modules.core.application.commands.review_command import ( CreateReviewCommand, DeleteReviewCommand)

class CreateReviewHandler:
    def __init__(self,review_repo: ReviewRepositoryInterface,audit_service: AuditServiceInterface = None,event_bus: EventBus = None,use_async: bool = False):
        self.repository = review_repo
        self.audit_service = audit_service
        self.event_bus = event_bus
        self.use_async = use_async

    async def handle(self, command: CreateReviewCommand):
        new_review = ReviewFactory.create_review( user_id=command.user_id,place_id=command.place_id,content_in=command.content_in)

        created_review = self.repository.create(new_review)

        if self.event_bus:
            await self.event_bus.publish(
                ReviewCreatedEvent( review_id=created_review.review_id,place_id=created_review.place_id,user_id=created_review.user_id,content_in=created_review.content_in)
            )

        elif self.audit_service:
            try:
                self.audit_service.log_review_created( review_id=created_review.review_id,user_id=command.user_id,place_id=command.place_id )
            except Exception:
                pass

        return created_review.review_id

class DeleteReviewHandler:
    def __init__(self, review_repo, event_bus=None):
        self.repository = review_repo
        self.event_bus = event_bus

    async def handle(self, command):
        review = self.repository.get_by_id(command.review_id)

        if not review:
            raise DomainError("Відгук не знайдено")

        place_id = review.place_id

        deleted = self.repository.delete(command.review_id)

        if not deleted:
            raise DomainError("Не вдалося видалити відгук")

        if self.event_bus:
            await self.event_bus.publish(
                ReviewDeletedEvent(
                    review_id=command.review_id,
                    place_id=place_id
                )
            )

        return True