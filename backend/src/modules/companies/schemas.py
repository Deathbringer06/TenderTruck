from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.modules.companies.models import VerificationStatus


class CompanyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    inn: str = Field(min_length=1, max_length=12)
    description: str | None = Field(default=None, max_length=1000)


class CompanyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    inn: str | None = Field(default=None, min_length=1, max_length=12)
    description: str | None = Field(default=None, max_length=1000)


class CompanyRead(BaseModel):
    id: UUID
    owner_id: UUID
    name: str
    inn: str
    description: str | None
    verification_status: VerificationStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
