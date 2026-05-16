from src.security.get_password_hash import get_password_hash
from src.domain.factory import UserFactory
from src.domain.interfaces import UserRepositoryInterface
from src.application.commands.user_command import CreateUserCommand, DeleteUserCommand

class CreateUserHandler:
    def __init__(self, user_repo: UserRepositoryInterface):
        self.repository = user_repo
        self.factory = UserFactory(user_repo) 

    def handle(self, command: CreateUserCommand):
        hashed_pwd = get_password_hash(command.password)
        
        new_user = self.factory.create_user(
            password_hash=hashed_pwd, 
            email_str=command.email,  
            phone_number=command.phone_number,
            user_name=command.user_name
        )
        created_user = self.repository.create(new_user)
        return created_user.user_id

class DeleteUserHandler:
    def __init__(self, user_repo: UserRepositoryInterface):
        self.repository = user_repo

    def handle(self, command: DeleteUserCommand):
        self.repository.delete(command.user_id)