from src.modules.analytics.infrastructure.repository.repo_analytics import AnalyticsRepository
from src.modules.analytics.acl.place_event_acl import PlaceEventACL


class PlaceCreatedAnalyticsHandler:
    def __init__(self, session_factory):
        self.session_factory = session_factory


    async def handle(self, event):
        place_statistics = PlaceEventACL.to_internal(event)
        print("ANALYTICS EVENT RECEIVED:", event)
        
        with self.session_factory() as db:
            analytics_repo = AnalyticsRepository(db)
            analytics_repo.save_place_statistics(place_statistics)