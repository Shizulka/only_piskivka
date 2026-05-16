from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import time

from src.infrastructure.database import get_db
from src.infrastructure.repository.repo_place import PlaceRepository
from src.infrastructure.dependencies import get_current_admin_user
from src.application.commands.place_commands import ( CreatePlaceCommand,   DeletePlaceCommand )
from src.application.queries.place_queries import GetAllPlacesQuery

from src.application.queries.place_query_handlers import GetAllPlacesHandler
from src.application.commands.place_command_handlers import (CreatePlaceHandler,  DeletePlaceHandler)

from src.domain.value_objects import PlaceStatus
from src.domain.exceptions import DomainError

router = APIRouter(prefix="/place", tags=["Places"])

def get_place_repo(db: Session = Depends(get_db)):
    return PlaceRepository(db)


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_new_place(location: str, open_time: time, close_time: time, place_status: PlaceStatus,  current_user = Depends(get_current_admin_user), place_repo=Depends(get_place_repo)):
    handler = CreatePlaceHandler(place_repo)

    command = CreatePlaceCommand(location=location, open_time=open_time, close_time=close_time, status=place_status)

    try:
        created_id = handler.handle(command)
        return {
            "place_id": created_id,
            "message": "Місце успішно додано"
        }
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/all")
def all_places(place_repo = Depends(get_place_repo)):
    handler = GetAllPlacesHandler(place_repo)
    query = GetAllPlacesQuery()
    return handler.handle(query)


@router.delete("/{place_id}")
def delete_place(place_id: int, place_repo = Depends(get_place_repo) , current_user = Depends(get_current_admin_user),):
    handler = DeletePlaceHandler(place_repo)
    command = DeletePlaceCommand(place_id=place_id)
    
    handler.handle(command)
    return {"message": "Місце успішно видалено"}