from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class BidCreate(BaseModel):
    price: int = Field(gt=0)


class BidRead(BaseModel):
    id: UUID
    tender_id: UUID
    carrier_id: UUID
    price: int
    idempotency_key: str
    is_winner: bool
    created_at: datetime

    model_config = {"from_attributes": True}
