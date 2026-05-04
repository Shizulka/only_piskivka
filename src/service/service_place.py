from datetime import time

from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.infrastructure.models import Place
from src.repository.repo_place import PlaceRepository

class PlaceService :
    def __init__ (self , db: Session):
        self.repository = PlaceRepository(db , Place)
        self.db = db

    def craete_place ( self , location : int , open: time  , close: time , status: str): 
        new_place = Place ( location = location , open = open , close = close , type_place=status)

        return self.repository.create (new_place)

    def all_place (self): 
        return self.db.query(Place).all()

    def delete_place(self, place_id: int):
        place = self.repository.db.query(Place).filter(Place.place_id == place_id).first()

        if place is None:
            raise HTTPException(status_code=404, detail="Place not found")

        return self.repository.delete(place)
    
    