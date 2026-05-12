
from datetime import time

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.dependencies import get_current_user
from src.domain.value_objects import PlaceStatus
from src.infrastructure.database import get_db
from src.infrastructure.repository.repo_place import PlaceRepository
from src.application.service_place import PlaceService
from src.domain.exceptions import DomainError

router = APIRouter(prefix="/place", tags=["Places"])

def get_place_repo(db: Session = Depends(get_db)):
    return PlaceRepository(db)

@router.post("/create")
def create_new_place( location: str,  open: time,  close: time,  place_status: PlaceStatus, current_user = Depends(get_current_user), place_repo = Depends(get_place_repo)):
    service = PlaceService(place_repo)
    try:
        new_place = service.create_place( location=location, open_time=open,close_time=close,status=place_status)
        return {
            "place_id": new_place.place_id,"location": new_place.location, "working_hours": f"{new_place.working_hours.open_time} - {new_place.working_hours.close_time}",
            "type_place": new_place.status,"message": "Місце успішно додано"
        }
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/all")
def all_places(place_repo = Depends(get_place_repo)):
    service = PlaceService(place_repo)
    places = service.all_places()
    
    return [
        {
            "id": p.place_id, 
            "location": p.location, 
            "open": p.working_hours.open_time,
            "close": p.working_hours.close_time,
            "type_place": p.status
        } for p in places
    ]

@router.delete("/{place_id}")
def delete_place(place_id: int,  current_user = Depends(get_current_user), place_repo = Depends(get_place_repo)):
    service = PlaceService(place_repo)
    success = service.delete_place(place_id)
    
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Місце не знайдено")
        
    return {"message": "Місце успішно видалено"}