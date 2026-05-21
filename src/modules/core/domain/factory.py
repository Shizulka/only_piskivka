
from  src.modules.core.domain.entities import User, Place
from  src.modules.core.domain.value_objects import Email, TimeRange
from  src.modules.core.domain.exceptions import UserAlreadyExistsError
from  src.modules.core.domain.interfaces import UserRepositoryInterface

from datetime import time

from src.modules.core.domain.entities import User, Place, Review
from src.modules.core.domain.value_objects import Email, TimeRange
from src.modules.core.domain.exceptions import ( UserAlreadyExistsError,EmptyReviewError,)
from src.modules.core.domain.interfaces import UserRepositoryInterface


class UserFactory:
    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo

    def create_user( self, user_name: str, email_str: str, password_hash: str, phone_number: str | None = None
    ) -> User:
        email_vo = Email(email_str)

        if self.user_repo.get_user_by_email(email_vo.value):
            raise UserAlreadyExistsError()

        return User( user_name=user_name, email=email_vo,password_hash=password_hash, phone_number=phone_number
        )


class PlaceFactory:
    @staticmethod
    def create_place( location: str, open_time: time, close_time: time, status: str
    ) -> Place:
        working_hours = TimeRange(open_time, close_time)

        return Place(location=location,  working_hours=working_hours,  status=status
        )


class ReviewFactory:
    @staticmethod
    def create_review(user_id: int, place_id: int, content_in: str) -> Review:
        if content_in is None or content_in.strip() == "":
            raise EmptyReviewError("Review content cannot be empty")
        return Review(user_id=user_id, place_id=place_id, content_in=content_in)