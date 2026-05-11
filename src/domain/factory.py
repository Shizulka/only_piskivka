
from  src.domain.entities import User, Place
from  src.domain.value_objects import Email, TimeRange
from  src.domain.exceptions import UserAlreadyExistsError
from  src.domain.interfaces import UserRepositoryInterface

class DomainFactory:
    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo

    def create_user(self, user_name: str, email_str: str, password_hash: str, phone_number: str = None) -> User:
        email_vo = Email(email_str)

        if self.user_repo.get_user_by_email(email_vo.value):
            raise UserAlreadyExistsError()
        
        return User(
            user_name=user_name,
            email=email_vo,
            password_hash=password_hash,
            phone_number=phone_number
        )

    def create_place(self, location: str, open_time: str, close_time: str, status: str) -> Place:
        time_range = TimeRange(open_time, close_time)

        return Place(
            location=location,
            working_hours=time_range,
            status=status
        )