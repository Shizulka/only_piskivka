from src.domain.factory import PlaceFactory
from src.domain.interfaces import PlaceRepositoryInterface
from src.application.commands.place_commands import CreatePlaceCommand, DeletePlaceCommand

class CreatePlaceHandler:
    def __init__(self, place_repo: PlaceRepositoryInterface):
        self.repository = place_repo

    def handle(self, command: CreatePlaceCommand):
        new_place = PlaceFactory.create_place(location=command.location,open_time=command.open_time,close_time=command.close_time,status=command.status)
        created_place = self.repository.create(new_place)
        return created_place.place_id

class DeletePlaceHandler:
    def __init__(self, place_repo: PlaceRepositoryInterface):
        self.repository = place_repo

    def handle(self, command: DeletePlaceCommand):
        self.repository.delete(command.place_id)