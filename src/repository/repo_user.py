from sqlalchemy.orm import Session
from src.infrastructure.models import Users  

class UserRepository:
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model  

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def get_by_id(self, id: int):
        return self.db.get(self.model, id)
    
    def get_user_by_email(self, email: str):
        return self.db.query(Users).filter(Users.email == email).first()
    
    def get_user_by_phone(self, phone: str):
        return self.db.query(self.model).filter(self.model.phone_number == phone).first()
    
    def get_user_by_id(self, user_id: int):
        return self.db.query(Users).filter(Users.user_id == user_id).first()

    def create(self, obj_data):
        self.db.add(obj_data)
        self.db.commit()   
        self.db.refresh(obj_data)
        return obj_data

    def delete(self, obj_data):
        self.db.delete(obj_data)
        self.db.commit()   
        return obj_data