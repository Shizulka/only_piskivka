from dataclasses import dataclass
from typing import Optional

@dataclass
class CreateUserCommand:
    password: str
    email: Optional[str]
    phone_number: Optional[str]
    user_name: str

@dataclass
class DeleteUserCommand:
    user_id: int