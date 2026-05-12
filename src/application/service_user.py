
from src.domain.interfaces import UserRepositoryInterface
from src.domain.factory import  UserFactory
from src.security.get_password_hash import get_password_hash , verify_password

class UserService:
    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo
        self.factory = UserFactory(self.user_repo)

    def register_user(self, user_data):
        hashed_pwd = get_password_hash(user_data.password)
    
        new_domain_user = self.factory.create_user(user_name=user_data.user_name, email_str=user_data.email, password_hash=hashed_pwd,phone_number=user_data.phone_number )
        return self.user_repo.create(new_domain_user)
    
    def authenticate_user(self, login_data: str, password: str):
        user = self.user_repo.get_user_by_email(login_data)
        
        if not user:
            user = self.user_repo.get_user_by_phone(login_data)
            
        if not user:
            return False
            
        if not verify_password(password, user.password_hash):
            return False
            
        return user