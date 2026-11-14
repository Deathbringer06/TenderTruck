from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.core.exceptions import NotFoundError, ValidationError
from src.modules.auth.models import User, UserRole
from src.modules.auto_bids.models import AutoBid
from src.modules.bids.models import Bid
from src.modules.tenders.models import Tender, TenderStatus


def place_auto_bid(
    session: Session, tender_id: UUID, carrier_id: UUID, min_price: int, step: int
) -> AutoBid:
    carrier = session.get(User, carrier_id)
    if carrier is None or carrier.role != UserRole.carrier:
        raise NotFoundError("Carrier not found")
    tender = session.scalar(select(Tender).where(Tender.id == tender_id).with_for_update())
    if tender is None:
        raise NotFoundError("Tender not found")
    if tender.status != TenderStatus.ACTIVE:
        raise ValidationError("Tender is not active")
    if min_price <= 0 or min_price >= tender.current_price:
        raise ValidationError("Minimum price must be lower than the current price")
    if step <= 0:
        raise ValidationError("Step must be positive")

    auto_bid = AutoBid(
        tender_id=tender_id,
        carrier_id=carrier_id,
        min_price=min_price,
        step=step,
    )
    session.add(auto_bid)
    session.commit()
    session.refresh(auto_bid)
    return auto_bid


def list_auto_bids(session: Session, carrier_id: UUID) -> list[AutoBid]:
    return list(
        session.scalars(
            select(AutoBid)
            .where(AutoBid.carrier_id == carrier_id)
            .order_by(AutoBid.created_at.desc())
        )
    )


def deactivate_auto_bid(session: Session, auto_bid_id: UUID, carrier_id: UUID) -> AutoBid:
    auto_bid = session.scalar(
        select(AutoBid).where(
            AutoBid.id == auto_bid_id,
            AutoBid.carrier_id == carrier_id,
        )
    )
    if auto_bid is None:
        raise NotFoundError("Auto-bid not found")
    auto_bid.is_active = False
    session.commit()
    session.refresh(auto_bid)
    return auto_bid


def process_auto_bids(session: Session, tender_id: UUID, new_bid_price: int) -> None:
    """Place successively lower bids while an active proxy can meet its minimum."""
    tender = session.scalar(select(Tender).where(Tender.id == tender_id).with_for_update())
    if tender is None or tender.status != TenderStatus.ACTIVE:
        return
    current_price = min(tender.current_price, new_bid_price)

    while tender.status == TenderStatus.ACTIVE:
        auto_bids = list(
            session.scalars(
                select(AutoBid)
                .where(AutoBid.tender_id == tender_id, AutoBid.is_active.is_(True))
                .order_by(AutoBid.min_price.desc(), AutoBid.created_at.asc())
            )
        )
        candidate = next(
            (
                (auto_bid, current_price - auto_bid.step)
                for auto_bid in auto_bids
                if current_price - auto_bid.step >= auto_bid.min_price
            ),
            None,
        )
        if candidate is None:
            break

        auto_bid, price = candidate
        price = current_price - auto_bid.step
        bid = Bid(
            tender_id=tender_id,
            carrier_id=auto_bid.carrier_id,
            price=price,
            idempotency_key=f"auto:{auto_bid.id}:{uuid4()}",
        )
        session.add(bid)
        tender.current_price = price
        current_price = price
        session.flush()

    session.commit()