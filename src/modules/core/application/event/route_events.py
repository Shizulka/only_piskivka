from dataclasses import dataclass
import datetime


@dataclass(frozen=True)
class RouteCreatedEvent:
    route_id: int
    user_id: int
    created_at: datetime