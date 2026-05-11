# infrastructure/mappers.py
from  src.domain.entities import User as DomainUser
from  src.domain.value_objects import Email
from  src.infrastructure.models import Users as DBUser

class UserMapper:
    @staticmethod
    def to_domain(db_model: DBUser) -> DomainUser:
        if not db_model:
            return None
            
        return DomainUser(
            user_id=db_model.user_id,
            user_name=db_model.user_name,
            email=Email(db_model.email), # Перетворюємо звичайний рядок на Value Object
            password_hash=db_model.password,
            phone_number=db_model.phone_number,
            status=db_model.status,
            is_admin=db_model.is_admin
        )

    @staticmethod
    def to_db(domain_entity: DomainUser) -> DBUser:
        return DBUser(
            user_id=domain_entity.user_id,
            user_name=domain_entity.user_name,
            email=domain_entity.email.value, # Витягуємо звичайний рядок з Value Object
            password=domain_entity.password_hash,
            phone_number=domain_entity.phone_number,
            status=domain_entity.status,
            is_admin=domain_entity.is_admin
        )