import enum
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum as SQLEnum, Integer, String, Text

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
