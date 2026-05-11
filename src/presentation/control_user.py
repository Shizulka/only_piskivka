from fastapi import APIRouter, Depends, HTTPException , status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.repository import repo_user
from src.infrastructure.dependencies import get_current_user
from src.infrastructure.get_password_hash import create_access_token
from src.infrastructure.database import get_db
from src.repository.repo_user import UserRepository
from src.application.service_user import UserService 
from src.infrastructure.schemas import UserCreate, UserOut
from src.infrastructure.models import Users  
from src.domain.exceptions import  DomainError

router = APIRouter(prefix="/users", tags=["Users"])
@router.post("/register", response_model=UserOut)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)

    try:
        new_user = user_service.register_user(user_data)
        return {
            "user_id": new_user.user_id, 
            "user_name": new_user.user_name,
            "email": new_user.email.value, 
            "message": "Успішно створено"
        }
        
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login")
def login_for_access_token( form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_service = UserService(db)
    
    user = user_service.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильний логін або пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": str(user.user_id)})
    return {"access_token": access_token, "token_type": "bearer"}