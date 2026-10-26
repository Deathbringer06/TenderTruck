from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    phone: str
    password: str
    role: UserRole
    inn: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    phone: str
    role: UserRole
    inn: str
    is_verified: bool
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class UserProfile(UserResponse):
    company_name: str | None = None
    description: str | None = None
    contact_person: str | None = None
    address: str | None = None


class UserProfileUpdate(BaseModel):
    company_name: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=1000)
    contact_person: str | None = None
    phone: str | None = Field(default=None, pattern=r"^\+996\d{9}$")
    address: str | None = None
