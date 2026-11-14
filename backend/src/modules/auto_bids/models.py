from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from src.app.db.base import Base


class AutoBid(Base):
    __tablename__ = "auto_bids"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    tender_id: Mapped[UUID] = mapped_column(ForeignKey("tenders.id"), nullable=False, index=True)
    carrier_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    min_price: Mapped[int] = mapped_column(Integer, nullable=False)
    step: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
