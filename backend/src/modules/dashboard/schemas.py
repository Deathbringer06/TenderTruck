from uuid import UUID

from pydantic import BaseModel


class CarrierWins(BaseModel):
    carrier_id: UUID
    name: str
    wins: int


class DashboardStats(BaseModel):
    total_saved: int
    active_tenders: int
    avg_bids_per_tender: float
    top_carriers: list[CarrierWins]
