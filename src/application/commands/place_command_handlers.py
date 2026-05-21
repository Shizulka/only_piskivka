import datetime

from src.application.event.place_event import PlaceCreatedEvent, PlaceDeletedEvent
from src.application.audit.audit_service import AuditServiceInterface
from src.application.event.event_bus import EventBus
from src.domain.factory import PlaceFactory
from src.domain.interfaces import PlaceRepositoryInterface
from src.application.commands.place_commands import CreatePlaceCommand, DeletePlaceCommand

class CreatePlaceHandler:
    def __init__(self,place_repo: PlaceRepositoryInterface,audit_service: AuditServiceInterface = None,event_bus: EventBus = None,use_async: bool = False):
        self.repository = place_repo
        self.audit_service = audit_service
        self.event_bus = event_bus
        self.use_async = use_async

    def handle(self, command: CreatePlaceCommand):

        new_place = PlaceFactory.create_place( location=command.location,open_time=command.open_time,close_time=command.close_time,status=command.status)
        created_place = self.repository.create(new_place)

        if self.use_async and self.event_bus:

            event = PlaceCreatedEvent(place_id=created_place.place_id,location=command.location,open_time=command.open_time,close_time=command.close_time,status=command.status,)
            self.event_bus.publish(event)

        elif self.audit_service:
            try:
                self.audit_service.log_place_created( place_id=created_place.place_id,location=command.location,open_time=command.open_time,close_time=command.close_time,status=command.status)

            except Exception:
                pass

        return created_place.place_id


class DeletePlaceHandler:
    def __init__(self,place_repo: PlaceRepositoryInterface,audit_service: AuditServiceInterface = None,event_bus: EventBus = None,use_async: bool = False):
        self.repository = place_repo
        self.audit_service = audit_service
        self.event_bus = event_bus
        self.use_async = use_async

    def handle(self, command: DeletePlaceCommand):
        self.repository.delete(command.place_id)
        if self.use_async and self.event_bus:

            event = PlaceDeletedEvent(
                place_id=command.place_id)

            self.event_bus.publish(event)

        elif self.audit_service:
            try:
                self.audit_service.log_place_deleted(
                    place_id=command.place_id
                )

            except Exception:
                pass