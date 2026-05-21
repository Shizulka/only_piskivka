from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.modules.core.infrastructure.dependencies import get_current_admin_user
from src.modules.core.application.audit.audit_handlers import UserRegisteredAuditHandler
from src.shared.event_bus import event_bus
from src.modules.core.application.event.user_event import UserRegisteredEvent
from src.modules.core.application.audit.audit_service import ConsoleAuditService
from src.modules.core.domain.interfaces import UserRepositoryInterface
from src.modules.core.infrastructure.database import get_db
from src.modules.core.infrastructure.repository.repo_user import UserRepository
from src.modules.core.infrastructure.schemas import UserCreate
from src.modules.core.domain.exceptions import DomainError

from src.modules.core.application.commands.user_command import CreateUserCommand, DeleteUserCommand
from src.modules.core.application.commands.user_command_handlers import CreateUserHandler, DeleteUserHandler

from src.modules.core.application.queries.user_queries import AuthenticateUserQuery
from src.modules.core.application.queries.user_queries_handlers import AuthenticateUserHandler
from src.security.get_password_hash import create_access_token


router = APIRouter(prefix="/users", tags=["Users"])


def get_user_repo(db: Session = Depends(get_db)) -> UserRepositoryInterface:
    return UserRepository(db)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    user_repo: UserRepositoryInterface = Depends(get_user_repo)
):
    command = CreateUserCommand(
        password=user_data.password,
        email=user_data.email,
        phone_number=user_data.phone_number,
        user_name=user_data.user_name
    )

    handler = CreateUserHandler(
        user_repo=user_repo,
        event_bus=event_bus
    )

    try:
        created_id = await handler.handle(command)

        return {
            "user_id": created_id,
            "message": "Успішно створено"
        }

    except DomainError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.post("/login")
def login_for_access_token(  form_data: OAuth2PasswordRequestForm = Depends(),  user_repo: UserRepositoryInterface = Depends(get_user_repo)):
    handler = AuthenticateUserHandler(user_repo)
    query = AuthenticateUserQuery(username=form_data.username, password=form_data.password)
    
    user = handler.handle(query)
    
    if not user:
        raise HTTPException(  status_code=status.HTTP_401_UNAUTHORIZED,  detail="Неправильний логін або пароль",  headers={"WWW-Authenticate": "Bearer"},)
    
    access_token = create_access_token(data={"sub": str(user.user_id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.delete("/{user_id}")
async def delete_user(user_id: int,current_user=Depends(get_current_admin_user),user_repo=Depends(get_user_repo)):
    handler = DeleteUserHandler(user_repo=user_repo,event_bus=event_bus)
    command = DeleteUserCommand(user_id=user_id)

    try:
        await handler.handle(command)
        return { "message": "Користувача успішно видалено" }

    except DomainError as e:
        raise HTTPException(status_code=400, detail=str(e))