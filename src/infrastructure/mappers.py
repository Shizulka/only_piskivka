
from  src.domain.entities import User as DomainUser
from  src.domain.value_objects import Email, TimeRange
from  src.infrastructure.models import Users as DBUser
from  src.infrastructure.models import Place as DBPlace
from  src.domain.entities import Place as DomainPlace
from  src.infrastructure.models import Review as DBReview
from  src.domain.entities import Review as DomainReview


class UserMapper:
    @staticmethod
    def to_domain(db_model: DBUser) -> DomainUser:
        if not db_model:
            return None
            
        return DomainUser(
            user_id=db_model.user_id,
            user_name=db_model.user_name,
            email=Email(db_model.email), 
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
            email=domain_entity.email.value, 
            password=domain_entity.password_hash,
            phone_number=domain_entity.phone_number,
            status=domain_entity.status,
            is_admin=domain_entity.is_admin
        )
    
class PlaceMapper:  
    @staticmethod
    def to_domain(db_model: DBPlace) -> DomainPlace:
        if not db_model:
            return None
            
        return DomainPlace(
            place_id=db_model.place_id,
            location=db_model.location,
            working_hours=TimeRange(
                open_time=db_model.open, 
                close_time=db_model.close
            ),
            type_place=db_model.type_place
        )
    
    @staticmethod
    def to_db(domain_entity: DomainPlace) -> DBPlace:
        return DBPlace(
            place_id=domain_entity.place_id,
            location=domain_entity.location,
            open=domain_entity.working_hours.open_time, 
            close=domain_entity.working_hours.close_time,
            type_place=domain_entity.type_place
        )

class ReviewMapper: 
    @staticmethod
    def to_domain(db_model: DBReview) -> DomainReview:
        if not db_model:
            return None
            
        return DomainReview(
            review_id=db_model.review_id,
            place_id=db_model.place_id,
            user_id=db_model.user_id,
            content_in=db_model.content_in
        )
    
    @staticmethod
    def to_db(domain_entity:  DomainReview) -> DBReview:
        return DBReview(
            review_id=domain_entity.review_id,
            place_id=domain_entity.place_id,
            user_id=domain_entity.user_id,
            content_in=domain_entity.content_in
        )