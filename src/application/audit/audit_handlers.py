from src.application.event.place_event import PlaceCreatedEvent, PlaceDeletedEvent
from src.application.event.user_event import UserRegisteredEvent
from src.application.event.review_event import ReviewCreatedEvent, ReviewDeletedEvent
from src.application.audit.audit_service import AuditServiceInterface


class ReviewCreatedAuditHandler:
    def __init__(self, audit_service: AuditServiceInterface):
        self.audit_service = audit_service

    def __call__(self, event: ReviewCreatedEvent):
        self.audit_service.log_review_created(review_id=event.review_id, user_id=event.user_id,place_id=event.place_id)
    
class ReviewDeletedAuditHandler:
    def __init__(self, audit_service: AuditServiceInterface):
        self.audit_service = audit_service

    def __call__(self, event: ReviewDeletedEvent):
        self.audit_service.log_review_deleted(review_id=event.review_id,user_id=event.user_id)   


class UserRegisteredAuditHandler:
    def __init__(self, audit_service: AuditServiceInterface):
        self.audit_service = audit_service

    def __call__(self, event: UserRegisteredEvent):
        self.audit_service.log_user_registered(user_id=event.user_id,email=event.email)

class PlaceCreatedAuditHandler:
    def __init__(self, audit_service: AuditServiceInterface):
        self.audit_service = audit_service

    def __call__(self, event: PlaceCreatedEvent):
        self.audit_service.log_place_created( place_id=event.place_id, location=event.location,open_time=event.open_time,close_time=event.close_time , status=event.status)
    
class PlaceDeletedAuditHandler:
    def __init__(self, audit_service: AuditServiceInterface):
        self.audit_service = audit_service

    def __call__(self, event: PlaceDeletedEvent):
        self.audit_service.log_place_deleted( place_id=event.place_id)