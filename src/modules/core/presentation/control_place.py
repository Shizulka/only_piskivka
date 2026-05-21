from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import time

from src.modules.core.application.audit.audit_handlers import PlaceCreatedAuditHandler, PlaceDeletedAuditHandler
from src.modules.core.application.audit.audit_service import ConsoleAuditService
from src.shared.event_bus import event_bus
from src.modules.core.application.event.place_event import PlaceCreatedEvent, PlaceDeletedEvent
from src.modules.core.infrastructure.database import get_db
from src.modules.core.infrastructure.repository.repo_place import PlaceRepository
from src.modules.core.infrastructure.dependencies import get_current_admin_user
from src.modules.core.application.commands.place_commands import ( CreatePlaceCommand,   DeletePlaceCommand )
from src.modules.core.application.queries.place_queries import GetAllPlacesQuery

from src.modules.core.application.queries.place_query_handlers import GetAllPlacesHandler
from src.modules.core.application.commands.place_command_handlers import (CreatePlaceHandler,  DeletePlaceHandler)

from src.modules.core.domain.value_objects import PlaceStatus
from src.modules.core.domain.exceptions import DomainError

router = APIRouter(prefix="/place", tags=["Place"])

def get_place_repo(db: Session = Depends(get_db)):
    return PlaceRepository(db)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_new_place(location: str,open_time: time,close_time: time,place_status: PlaceStatus, current_user=Depends(get_current_admin_user), place_repo=Depends(get_place_repo)):
    handler = CreatePlaceHandler(place_repo=place_repo,event_bus=event_bus)

    command = CreatePlaceCommand(location=location,open_time=open_time,close_time=close_time,status=place_status)

    try:
        created_id = await handler.handle(command)
        return {"place_id": created_id, "message": "Місце успішно додано"}

    except DomainError as e:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

@router.get("/all")
def all_places(place_repo = Depends(get_place_repo)):
    handler = GetAllPlacesHandler(place_repo)
    query = GetAllPlacesQuery()
    return handler.handle(query)

@router.delete("/{place_id}")
async def delete_place(place_id: int,current_user=Depends(get_current_admin_user),place_repo=Depends(get_place_repo)):
    handler = DeletePlaceHandler(place_repo=place_repo,event_bus=event_bus)

    command = DeletePlaceCommand(place_id=place_id)

    try:
        await handler.handle(command)
        return {
            "message": "Місце успішно видалено"
        }

    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))