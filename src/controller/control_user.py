from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
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