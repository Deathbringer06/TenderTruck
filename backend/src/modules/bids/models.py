from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from src.app.db.base import Base


class Bid(Base):
    __tablename__ = "bids"
    __table_args__ = (UniqueConstraint("tender_id", "idempotency_key", name="uq_bid_idempotency"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    tender_id: Mapped[UUID] = mapped_column(ForeignKey("tenders.id"), nullable=False, index=True)
    carrier_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(255), nullable=False)
    is_winner: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
