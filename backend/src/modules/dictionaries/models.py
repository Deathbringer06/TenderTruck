from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from src.app.db.base import Base


class Dictionary(Base):
    __tablename__ = "dictionaries"
    __table_args__ = (UniqueConstraint("category", "code", name="uq_dictionary_category_code"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )
