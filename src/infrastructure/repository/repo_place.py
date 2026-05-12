from sqlalchemy.orm import Session

from typing import List, Optional
from sqlalchemy.orm import Session

from src.infrastructure.models import Place as DBPlace 
from src.infrastructure.mappers import PlaceMapper
from src.domain.entities import Place as DomainPlace
from src.domain.interfaces import PlaceRepositoryInterface

class PlaceRepository(PlaceRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create(self, place: DomainPlace) -> DomainPlace:
        db_place = PlaceMapper.to_db(place)
        
        self.db.add(db_place)
        self.db.commit()
        self.db.refresh(db_place)
    
        return PlaceMapper.to_domain(db_place)

    def get_by_id(self, place_id: int) -> Optional[DomainPlace]:
        db_place = self.db.query(DBPlace).filter(DBPlace.place_id == place_id).first()
        return PlaceMapper.to_domain(db_place)

    def get_all_places(self) -> List[DomainPlace]:
        db_places = self.db.query(DBPlace).all()
        return [PlaceMapper.to_domain(place) for place in db_places]

    def delete(self, place_id: int) -> bool:
        db_place = self.db.query(DBPlace).filter(DBPlace.place_id == place_id).first()
        if db_place:
            self.db.delete(db_place)
            self.db.commit()
            return True
        return False