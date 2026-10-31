from datetime import datetime
from typing import Literal

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


class TenderCreate(BaseModel):
    point_a: str = Field(min_length=1, max_length=255)
    point_b: str = Field(min_length=1, max_length=255)
    cargo_weight: float | None = Field(default=None, gt=0)
    cargo_volume: float | None = Field(default=None, gt=0)
    body_type: str | None = Field(default=None, max_length=100)
    loading_date: datetime
    unloading_date: datetime | None = None
    start_price: float = Field(gt=0)


class TenderUpdate(BaseModel):
    point_a: str | None = Field(default=None, min_length=1, max_length=255)
    point_b: str | None = Field(default=None, min_length=1, max_length=255)
    cargo_weight: float | None = Field(default=None, gt=0)
    cargo_volume: float | None = Field(default=None, gt=0)
    body_type: str | None = Field(default=None, max_length=100)
    loading_date: datetime | None = None
    unloading_date: datetime | None = None
    start_price: float | None = Field(default=None, gt=0)
    status: Literal["open", "closed", "completed"] | None = None


class TenderResponse(BaseModel):
    id: int
    customer_id: int
    point_a: str
    point_b: str
    cargo_weight: float | None
    cargo_volume: float | None
    body_type: str | None
    loading_date: datetime
    unloading_date: datetime | None
    start_price: float
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
