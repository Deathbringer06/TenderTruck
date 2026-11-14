from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AutoBidCreate(BaseModel):
    tender_id: UUID
    min_price: int = Field(gt=0)
    step: int = Field(gt=0)


class AutoBidRead(BaseModel):
    id: UUID
    tender_id: UUID
    carrier_id: UUID
    min_price: int
    step: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
