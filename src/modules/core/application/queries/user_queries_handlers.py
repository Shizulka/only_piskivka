from dataclasses import dataclass
from src.modules.core.application.queries.user_queries import AuthenticateUserQuery
from src.modules.core.domain.interfaces import UserRepositoryInterface
from src.security.get_password_hash import verify_password

class AuthenticateUserHandler:
    def __init__(self, user_repo: UserRepositoryInterface):
        self.repository = user_repo

    def handle(self, query: AuthenticateUserQuery):
        user = self.repository.get_user_by_email(query.username)
        
        if not user:
            user = self.repository.get_user_by_phone(query.username)
            
        if not user:
            return False
            
        if not verify_password(query.password, user.password_hash):
            return False
            
        return user