# src/business_logic/services/user_service.py
from fastapi import HTTPException
from src.repository.repo_user import UserRepository
from src.infrastructure.models import Users
from src.infrastructure.get_password_hash import get_password_hash 

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_new_user(self, user_data):
        existing_user = self.user_repo.get_user_by_email(user_data.email)

        if user_data.email:
            if self.user_repo.get_user_by_email(user_data.email):
                raise HTTPException(status_code=400, detail="Email already registered")
        
        if user_data.phone_number:
            if self.user_repo.get_user_by_phone(user_data.phone_number):
                raise HTTPException(status_code=400, detail="Phone already registered")
        
        hashed_pwd = get_password_hash(user_data.password)
        new_user = Users(user_name=user_data.user_name, phone_number=user_data.phone_number, email=user_data.email, password=hashed_pwd, status="cool")
   
        return self.user_repo.create(new_user)