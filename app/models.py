import enum
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum as SQLEnum, Integer, String, Text
from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class UserRole(str, enum.Enum):
    ZAKAZCHIK = "zakazchik"
    PEREVOZCHIK = "perevozchik"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False)
    inn = Column(String, unique=True, index=True, nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    company_name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    contact_person = Column(String, nullable=True)
    address = Column(String, nullable=True)


class Tender(Base):
    __tablename__ = "tenders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    point_a = Column(String(255), nullable=False)
    point_b = Column(String(255), nullable=False)
    cargo_weight = Column(Float, nullable=True)
    cargo_volume = Column(Float, nullable=True)
    body_type = Column(String(100), nullable=True)
    loading_date = Column(DateTime, nullable=False)
    unloading_date = Column(DateTime, nullable=True)
    start_price = Column(Float, nullable=False)
    status = Column(String(20), default="open", nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    customer = relationship("User", backref="tenders")
