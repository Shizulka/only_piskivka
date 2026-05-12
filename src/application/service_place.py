
from src.domain.factory import PlaceFactory
from src.domain.value_objects import TimeRange
from src.domain.interfaces import PlaceRepositoryInterface

class PlaceService:
    def __init__(self, place_repo: PlaceRepositoryInterface):
        self.repository = place_repo

    def create_place(self, location: str, open_time: str, close_time: str, status: str):
        new_place = PlaceFactory.create_place( location=location, open_time=open_time, close_time=close_time,  status=status )
        return self.repository.create(new_place)

    def all_places(self):
        return self.repository.get_all_places()

    def delete_place(self, place_id: int) -> bool:
        return self.repository.delete(place_id)