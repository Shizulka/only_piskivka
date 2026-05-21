import datetime

from src.modules.core.domain.exceptions import DomainError
from src.modules.core.application.event.place_event import PlaceCreatedEvent, PlaceDeletedEvent
from src.modules.core.application.audit.audit_service import AuditServiceInterface
from src.shared.event_bus import EventBus
from src.modules.core.domain.factory import PlaceFactory
from src.modules.core.domain.interfaces import PlaceRepositoryInterface
from src.modules.core.application.commands.place_commands import CreatePlaceCommand, DeletePlaceCommand

class CreatePlaceHandler:
    def __init__(self, place_repo, event_bus=None):
        self.place_repo = place_repo
        self.event_bus = event_bus

    async def handle(self, command: CreatePlaceCommand):
        place = PlaceFactory.create_place(location=command.location,open_time=command.open_time,close_time=command.close_time,status=command.status )

        created_place = self.place_repo.create(place)

        if self.event_bus:
            await self.event_bus.publish(
                PlaceCreatedEvent(
                    place_id=created_place.place_id,
                    location=created_place.location,
                    open_time=created_place.working_hours.open_time,
                    close_time=created_place.working_hours.close_time,
                    status=str(created_place.status)
                )
            )

        return created_place.place_id
    
class DeletePlaceHandler:
    def __init__(self, place_repo, event_bus=None):
        self.place_repo = place_repo
        self.event_bus = event_bus

    async def handle(self, command: DeletePlaceCommand):

        deleted = self.place_repo.delete(command.place_id)

        if not deleted:
            raise DomainError("Не вдалося видалити місце")

        if self.event_bus:
            await self.event_bus.publish(
                PlaceDeletedEvent(
                    place_id=command.place_id
                )
            )

        return True