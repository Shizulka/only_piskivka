from dataclasses import dataclass

@dataclass
class AuthenticateUserQuery:
    username: str 
    password: str