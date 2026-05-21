from sqlalchemy.orm import Session
from typing import Optional

from  src.modules.core.infrastructure.models import Users as DBUser
from  src.modules.core.infrastructure.mappers import UserMapper
from  src.modules.core.domain.interfaces import UserRepositoryInterface
from  src.modules.core.domain.entities import User as DomainUser


class UserRepository(UserRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[DomainUser]:
        db_user = self.db.query(DBUser).filter(DBUser.email == email).first()
        return UserMapper.to_domain(db_user)

    def get_user_by_phone(self, phone: str) -> Optional[DomainUser]:
        db_user = self.db.query(DBUser).filter(DBUser.phone_number == phone).first()
        return UserMapper.to_domain(db_user)

    def get_user_by_id(self, user_id: int) -> Optional[DomainUser]:
        db_user = self.db.query(DBUser).filter(DBUser.user_id == user_id).first()
        return UserMapper.to_domain(db_user)
    
    def delete(self, user_id: int) -> bool:
        db_user = (
            self.db.query(DBUser)
            .filter(DBUser.user_id == user_id)
            .first()
    )

        if db_user is None:
            return False

        self.db.delete(db_user)
        self.db.commit()

        return True

    def create(self, domain_user: DomainUser) -> DomainUser:
        db_user = UserMapper.to_db(domain_user)
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        

        return UserMapper.to_domain(db_user)