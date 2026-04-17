
from datetime import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.infrastructure.models import PlaceStatus
from src.infrastructure.database import get_db
from src.service.service_place import PlaceService  

router = APIRouter()

@router.post("/create")
def craete_place (  location : str , open: time  , close: time  , status: PlaceStatus ,db: Session = Depends (get_db)):
    service = PlaceService(db)  
    place = service.craete_place( location = location , open = open , close = close , status=status)

    return place

@router.post("/all")
def all_place  ( db: Session = Depends (get_db)):
    service = PlaceService(db) 
    places = service.all_place()
    result = [{"id": p.place_id, "location": p.location} for p in places]
    return result