from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities import User , Review, Place

class UserRepositoryInterface(ABC):
    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass
        
    @abstractmethod
    def get_user_by_phone(self, phone: str) -> Optional[User]:
        pass
        
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        pass
        
    @abstractmethod
    def create(self, user: User) -> User:
        pass


class ReviewRepositoryInterface(ABC):
    @abstractmethod
    def create(self, review: Review) -> Review:
        pass

    @abstractmethod
    def get_all_reviews(self) -> List[Review]:
        pass

    @abstractmethod
    def get_by_id(self, review_id: int) -> Optional[Review]:
        pass

    @abstractmethod
    def delete(self, review_id: int) -> bool:
        pass

class PlaceRepositoryInterface(ABC):
    @abstractmethod
    def create(self, place: Place) -> Place:
        pass
        
    @abstractmethod
    def get_by_id(self, place_id: int) -> Optional[Place]:
        pass
        
    @abstractmethod
    def get_all_places(self) -> List[Place]:
        pass
        
    @abstractmethod
    def delete(self, place_id: int) -> bool:
        pass