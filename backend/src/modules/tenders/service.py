from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.core.exceptions import NotFoundError
from src.modules.tenders.models import Tender, TenderStatus
from src.modules.tenders.schemas import TenderCreate


def create_tender(session: Session, creator_id: UUID, data: TenderCreate) -> Tender:
    tender = Tender(
        title=data.title,
        start_price=data.start_price,
        current_price=data.start_price,
        step=data.step,
        deadline=data.deadline,
        status=TenderStatus.ACTIVE,
        created_by=creator_id,
    )
    session.add(tender)
    session.commit()
    session.refresh(tender)
    return tender


def get_tender(session: Session, tender_id: UUID) -> Tender:
    tender = session.get(Tender, tender_id)
    if tender is None:
        raise NotFoundError("Tender not found")
    return tender


def list_tenders(session: Session) -> list[Tender]:
    return list(session.scalars(select(Tender).order_by(Tender.created_at.desc())))


def close_tender(session: Session, tender_id: UUID) -> Tender:
    tender = get_tender(session, tender_id)
    tender.status = TenderStatus.CLOSED
    session.commit()
    session.refresh(tender)
    return tender
