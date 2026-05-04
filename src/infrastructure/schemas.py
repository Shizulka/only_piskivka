from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
import re

class UserCreate(BaseModel):
    user_name: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    password: str = Field(..., min_length=8, max_length=72)

    @model_validator(mode='after')
    def check_either_email_or_phone(self):
        if not self.email and not self.phone_number:
            raise ValueError('Ви повинні вказати або email, або номер телефону')
        return self
    
    @field_validator('phone_number')
    @classmethod
    def validate_phone(cls, v):
        if not re.match(r'^\+?3?8?(0\d{9})$', v):
            raise ValueError('Invalid phone number format. Use +380XXXXXXXXX')
        return v

class UserOut(BaseModel):
    user_id: int
    user_name: str
    email: Optional[EmailStr] = None 
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True