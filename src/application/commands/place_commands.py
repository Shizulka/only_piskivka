from dataclasses import dataclass
from datetime import time

@dataclass
class CreatePlaceCommand:
    location: str
    open_time: time
    close_time: time
    status: str

@dataclass
class DeletePlaceCommand:
    place_id: int