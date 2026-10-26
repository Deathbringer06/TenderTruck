from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    phone: str = Field(min_length=1, max_length=32)
    password: str = Field(min_length=8, max_length=72)
    role: UserRole
    inn: str = Field(min_length=1, max_length=32)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()

    @field_validator("password")
    @classmethod
    def enforce_bcrypt_byte_limit(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Пароль не должен превышать 72 байта в UTF-8")
        return value

    @field_validator("phone", "inn", mode="before")
    @classmethod
    def normalize_identifiers(cls, value: str) -> str:
        return value.strip()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=72)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()

    @field_validator("password")
    @classmethod
    def enforce_bcrypt_byte_limit(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Пароль не должен превышать 72 байта в UTF-8")
        return value


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
    model_config = ConfigDict(str_strip_whitespace=True)

    company_name: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=1000)
    contact_person: str | None = Field(default=None, max_length=120)
    phone: str | None = Field(default=None, pattern=r"^\+996\d{9}$")
    address: str | None = Field(default=None, max_length=250)

    @field_validator("phone")
    @classmethod
    def phone_cannot_be_null(cls, value: str | None) -> str | None:
        if value is None:
            raise ValueError("Телефон нельзя очистить")
        return value
