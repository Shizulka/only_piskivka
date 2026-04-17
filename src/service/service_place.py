from datetime import time

from sqlalchemy.orm import Session

from src.infrastructure.models import Place
from src.repository.repo_place import PlaceRepository

class PlaceService :
    def __init__ (self , db: Session):
        self.repository = PlaceRepository(db , Place)
        self.db = db

    def craete_place ( self , location : int , open: time  , close: time , status: str): 
        new_place = Place ( location = location , open = open , close = close , type_place=status)

        return self.repository.create (new_place)