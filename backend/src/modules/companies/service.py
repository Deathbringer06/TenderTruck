from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.core.exceptions import NotFoundError
from src.modules.companies.models import Company
from src.modules.companies.schemas import CompanyCreate, CompanyUpdate


def create_company(session: Session, owner_id: UUID, data: CompanyCreate) -> Company:
    company = Company(owner_id=owner_id, **data.model_dump())
    session.add(company)
    session.commit()
    session.refresh(company)
    return company


def get_company_by_owner(session: Session, owner_id: UUID) -> Company:
    company = session.scalar(select(Company).where(Company.owner_id == owner_id))
    if company is None:
        raise NotFoundError("Company not found")
    return company


def update_company(session: Session, owner_id: UUID, data: CompanyUpdate) -> Company:
    company = get_company_by_owner(session, owner_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(company, field, value)
    session.commit()
    session.refresh(company)
    return company
