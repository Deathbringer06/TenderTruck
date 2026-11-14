from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class ScoreRead(BaseModel):
    company_id: UUID | None
    inn: str
    risk: Literal["LOW", "MEDIUM", "HIGH"]
    reason: str
    checked_at: datetime | None = None
