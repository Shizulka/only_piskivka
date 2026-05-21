from dataclasses import dataclass
from dataclasses import dataclass, field
from typing import Optional
from src.core.domain.value_objects import UserStatus

@dataclass
class UserReadModel:
    
    user_id: int
    email: Optional[str]
    phone_number: Optional[str]
    status: Optional[UserStatus]
    user_name: str
    is_admin: bool = False
    reviews: list = field(default_factory=list)