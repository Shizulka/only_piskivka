import datetime

from src.modules.core.domain.exceptions import DomainError
from src.modules.core.application.event.user_event import UserDeletedEvent, UserRegisteredEvent
from src.modules.core.application.audit.audit_service import AuditServiceInterface
from src.shared.event_bus import EventBus
from src.security.get_password_hash import get_password_hash
from src.modules.core.domain.factory import UserFactory
from src.modules.core.domain.interfaces import UserRepositoryInterface
from src.modules.core.application.commands.user_command import CreateUserCommand, DeleteUserCommand

class CreateUserHandler:
    def __init__(self, user_repo, audit_service=None, event_bus=None, use_async=False):
        self.repository = user_repo
        self.factory = UserFactory(user_repo)
        self.audit_service = audit_service
        self.event_bus = event_bus
        self.use_async = use_async

    async def handle(self, command: CreateUserCommand):
        hashed_pwd = get_password_hash(command.password)

        new_user = self.factory.create_user(
            password_hash=hashed_pwd,
            email_str=command.email,
            phone_number=command.phone_number,
            user_name=command.user_name
        )

        created_user = self.repository.create(new_user)

        if self.event_bus:
            await self.event_bus.publish(
                UserRegisteredEvent(
                    user_id=created_user.user_id,
                    email=created_user.email
                )
            )

        elif self.audit_service:
            try:
                self.audit_service.log_user_registered(
                    user_id=created_user.user_id,
                    email=created_user.email
                )
            except Exception:
                pass

        return created_user.user_id

class DeleteUserHandler:
    def __init__(self, user_repo, event_bus=None):
        self.repository = user_repo
        self.event_bus = event_bus

    async def handle(self, command: DeleteUserCommand):
        user = self.repository.get_user_by_id(command.user_id)

        if user is None:
            raise DomainError("Користувача не знайдено")

        deleted = self.repository.delete(command.user_id)

        if not deleted:
            raise DomainError("Не вдалося видалити користувача")

        if self.event_bus:
            await self.event_bus.publish(
                UserDeletedEvent(
                    user_id=command.user_id,
                    email=user.email
                )
            )

        return True