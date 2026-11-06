from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.modules.tenders.models import TenderStatus


class TenderCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    start_price: int = Field(gt=0)
    step: int = Field(gt=0)
    deadline: datetime


class TenderUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    start_price: int | None = Field(default=None, gt=0)
    current_price: int | None = Field(default=None, gt=0)
    step: int | None = Field(default=None, gt=0)
    deadline: datetime | None = None
    status: TenderStatus | None = None


class TenderRead(BaseModel):
    id: UUID
    title: str
    start_price: int
    current_price: int
    step: int
    deadline: datetime
    status: TenderStatus
    extension_count: int
    max_extensions: int
    created_by: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
