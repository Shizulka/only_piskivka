from dataclasses import dataclass


@dataclass
class PlaceStatistics:
    external_place_id: int
    location: str
    status: str
    total_reviews: int = 0