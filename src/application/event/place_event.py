from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class PlaceCreatedEvent:
    place_id: int
    location: str
    open_time: datetime
    close_time: datetime
    status: str 


@dataclass(frozen=True)
class PlaceDeletedEvent:
    place_id: int
