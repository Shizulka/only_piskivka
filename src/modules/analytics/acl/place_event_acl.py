from src.modules.analytics.domain.analytics_entities import PlaceStatistics


class PlaceEventACL:

    @staticmethod
    def to_internal(event):
        return PlaceStatistics(
            external_place_id=event.place_id,
            location=event.location,
            status=event.status,
            total_reviews=0
        )