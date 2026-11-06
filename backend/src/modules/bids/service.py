from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.core.exceptions import NotFoundError, ValidationError
from src.modules.bids.models import Bid
from src.modules.tenders.models import Tender, TenderStatus


def place_bid(
    session: Session,
    tender_id: UUID,
    carrier_id: UUID,
    price: int,
    idempotency_key: str,
) -> Bid:
    existing = session.scalar(
        select(Bid).where(
            Bid.tender_id == tender_id,
            Bid.idempotency_key == idempotency_key,
        )
    )
    if existing is not None:
        return existing

    tender = session.scalar(select(Tender).where(Tender.id == tender_id).with_for_update())
    if tender is None:
        raise NotFoundError("Tender not found")
    if tender.status != TenderStatus.ACTIVE:
        raise ValidationError("Tender is not active")
    if price >= tender.current_price or price > tender.current_price - tender.step:
        raise ValidationError("Bid must be lower than the current price by at least the step")

    bid = Bid(
        tender_id=tender_id,
        carrier_id=carrier_id,
        price=price,
        idempotency_key=idempotency_key,
    )
    tender.current_price = price
    now = datetime.now(UTC)
    deadline = tender.deadline
    if deadline.tzinfo is None:
        deadline = deadline.replace(tzinfo=UTC)
    delta = deadline - now
    if timedelta(0) < delta < timedelta(minutes=2) and tender.extension_count < tender.max_extensions:
        tender.deadline = deadline + timedelta(minutes=2)
        tender.extension_count += 1

    session.add(bid)
    session.commit()
    session.refresh(bid)
    return bid
