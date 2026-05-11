from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities import User

class UserRepositoryInterface(ABC):
    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Повертає користувача за email, або None, якщо такого немає"""
        pass