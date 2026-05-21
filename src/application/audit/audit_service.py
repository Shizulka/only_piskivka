from abc import ABC, abstractmethod
import datetime


class AuditServiceInterface(ABC):

    @abstractmethod
    def log_review_created(self, review_id: int, user_id: int, place_id: int):
        pass

    @abstractmethod
    def log_review_deleted(self, review_id: int, user_id: int):
        pass

    @abstractmethod
    def log_user_registered(self, user_id: int, email: str):
        pass

    @abstractmethod
    def log_place_created(self, place_id: int, location: str , open_time: datetime  , close_time: datetime , status: str):
        pass

    @abstractmethod
    def log_place_deleted(self, place_id: int):
        pass

class ConsoleAuditService(AuditServiceInterface):

    def log_review_created(self, review_id: int, user_id: int, place_id: int):
        print(
            f"AUDIT: user {user_id} created review {review_id} for place {place_id}"
        )

    def log_review_deleted(self, review_id: int, user_id: int):
        print(
            f"AUDIT: user {user_id} deleted review {review_id}"
        )

    def log_user_registered(self, user_id: int, email: str):
        print(f"AUDIT: user {user_id} registered with email {email}")

    def log_place_created(self,place_id: int, location: str , open_time: datetime  , close_time: datetime , status: str):
        print( f"AUDIT: place {place_id} with location {location} "
                f"and working hours from {open_time} to {close_time} is {status} created successfully")
        
    def log_place_deleted(self, place_id: int):
        print(f"AUDIT: place {place_id} deleted successfully")

    

