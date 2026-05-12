from fastapi import APIRouter, Depends, HTTPException , status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.domain.interfaces import UserRepositoryInterface
from src.infrastructure.repository import repo_user
from src.infrastructure.dependencies import get_current_user
from src.security.get_password_hash import create_access_token
from src.infrastructure.database import get_db
from src.infrastructure.repository.repo_user import UserRepository
from src.application.service_user import UserService 
from src.infrastructure.schemas import UserCreate, UserOut

from src.domain.exceptions import  DomainError

router = APIRouter(prefix="/users", tags=["Users"])

def get_user_repo(db: Session = Depends(get_db)) -> UserRepositoryInterface:
    return UserRepository(db)

@router.post("/register", response_model=UserOut)
def register( user_data: UserCreate,  user_repo: UserRepositoryInterface = Depends(get_user_repo) ):
    user_service = UserService(user_repo)
    
    try:
        new_user = user_service.register_user(user_data)
        return {"user_id": new_user.user_id,  "user_name": new_user.user_name, "email": new_user.email.value,  "message": "Успішно створено" }
    except DomainError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.post("/login")
def login_for_access_token( form_data: OAuth2PasswordRequestForm = Depends(), user_repo: UserRepositoryInterface = Depends(get_user_repo)):
    user_service = UserService(user_repo)
    
    user = user_service.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильний логін або пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": str(user.user_id)})
    return {"access_token": access_token, "token_type": "bearer"}