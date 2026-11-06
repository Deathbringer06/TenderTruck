from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

from src.modules.auth.models import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.customer


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
