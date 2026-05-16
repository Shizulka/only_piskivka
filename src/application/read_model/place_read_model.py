from dataclasses import dataclass
from datetime import time

@dataclass
class PlaceReadModel:
    id: int
    location: str
    open_time: time
    close_time: time
    status: str