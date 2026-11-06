from datetime import UTC, datetime, timedelta

from src.app.db.base import Base
from src.app.db.engine import SessionLocal, engine
from src.modules.auth.models import User, UserRole
from src.modules.bids.service import place_bid
from src.modules.tenders.models import Tender, TenderStatus


def setup_module() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def test_place_bid_lowers_current_price() -> None:
    with SessionLocal() as session:
        carrier = User(
            email="carrier@example.com",
            hashed_password="test",
            role=UserRole.carrier,
        )
        customer = User(
            email="customer-bid@example.com",
            hashed_password="test",
            role=UserRole.customer,
        )
        session.add_all([carrier, customer])
        session.flush()
        tender = Tender(
            title="Bid test",
            start_price=10000,
            current_price=10000,
            step=100,
            deadline=datetime.now(UTC) + timedelta(hours=1),
            status=TenderStatus.ACTIVE,
            created_by=customer.id,
        )
        session.add(tender)
        session.commit()

        bid = place_bid(session, tender.id, carrier.id, 9800, "bid-1")
        assert bid.price == 9800
        assert session.get(Tender, tender.id).current_price == 9800
