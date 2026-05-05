from fastapi import APIRouter, Depends, HTTPException , status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.repository import repo_user
from src.infrastructure.dependencies import get_current_user
from src.infrastructure.get_password_hash import create_access_token
from src.infrastructure.database import get_db
from src.repository.repo_user import UserRepository
from src.service.service_user import UserService 
from src.infrastructure.schemas import UserCreate, UserOut
from src.infrastructure.models import Users  

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserOut)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user_repo = UserRepository(db, Users)
    user_service = UserService(user_repo)
    
    return user_service.register_new_user(user_data)

@router.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_repo = UserRepository(db, Users)
    user_service = UserService(user_repo)
    
    user = user_service.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірний email, телефон або пароль", 
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(data={"sub": str(user.user_id)}) 
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user