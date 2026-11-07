from __future__ import annotations

import enum
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.app.db.base import Base


class VerificationStatus(enum.StrEnum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    inn: Mapped[str] = mapped_column(String(12), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    verification_status: Mapped[VerificationStatus] = mapped_column(
        Enum(VerificationStatus), default=VerificationStatus.PENDING, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )
