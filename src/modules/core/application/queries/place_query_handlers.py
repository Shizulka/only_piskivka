from src.modules.core.domain.interfaces import PlaceRepositoryInterface
from src.modules.core.application.queries.place_queries import GetAllPlacesQuery
from src.modules.core.application.read_model.place_read_model import PlaceReadModel

class GetAllPlacesHandler:
    def __init__(self, place_repo: PlaceRepositoryInterface):
        self.repository = place_repo

    def handle(self, query: GetAllPlacesQuery):
        places = self.repository.get_all_places()

        return [
            PlaceReadModel(id=place.place_id, location=place.location,open_time=place.working_hours.open_time, close_time=place.working_hours.close_time,status=place.status)
            for place in places
        ]