from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.application.audit.audit_handlers import UserRegisteredAuditHandler
from src.application.event.event_bus import EventBus
from src.application.event.user_event import UserRegisteredEvent
from src.application.audit.audit_service import ConsoleAuditService
from src.domain.interfaces import UserRepositoryInterface
from src.infrastructure.database import get_db
from src.infrastructure.repository.repo_user import UserRepository
from src.infrastructure.schemas import UserCreate
from src.domain.exceptions import DomainError

from src.application.commands.user_command import CreateUserCommand
from src.application.commands.user_command_handlers import CreateUserHandler

from src.application.queries.user_queries import AuthenticateUserQuery
from src.application.queries.user_queries_handlers import AuthenticateUserHandler
from src.security.get_password_hash import create_access_token


router = APIRouter(prefix="/users", tags=["Users"])


def get_user_repo(db: Session = Depends(get_db)) -> UserRepositoryInterface:
    return UserRepository(db)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(   user_data: UserCreate,  user_repo: UserRepositoryInterface = Depends(get_user_repo)):

    command = CreateUserCommand( password=user_data.password, email=user_data.email, phone_number=user_data.phone_number, user_name=user_data.user_name )
    audit_service = ConsoleAuditService()
    event_bus = EventBus()

    event_bus.subscribe(UserRegisteredEvent,UserRegisteredAuditHandler(audit_service))

    handler = CreateUserHandler(user_repo=user_repo,audit_service=audit_service,event_bus=event_bus,use_async=True)
    
    try:
        created_id = handler.handle(command)

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