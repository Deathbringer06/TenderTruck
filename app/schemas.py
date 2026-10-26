from pydantic import BaseModel, EmailStr
from app.models import UserRole

class UserCreate(BaseModel):
    email: EmailStr
    phone: str
    password: str
    role: UserRole
    inn: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    phone: str
    role: UserRole
    inn: str
    is_verified: bool

    class Config:
        from_attributes = True