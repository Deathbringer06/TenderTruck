from datetime import UTC, datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.app.db.base import Base
from src.modules.auth.models import User, UserRole
from src.modules.bids.models import Bid
from src.modules.dashboard.service import get_dashboard_stats
from src.modules.tenders.models import Tender, TenderStatus


def test_dashboard_aggregates_tenders_and_winners() -> None:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine, expire_on_commit=False) as session:
        customer = User(email="dashboard-customer@example.com", hashed_password="x", role=UserRole.customer)
        carrier = User(email="dashboard-carrier@example.com", hashed_password="x", role=UserRole.carrier)
        session.add_all([customer, carrier])
        session.flush()
        customer_id = customer.id
        carrier_id = carrier.id
        closed = Tender(title="Closed", start_price=10000, current_price=8000, step=100,
                        deadline=datetime(2030, 1, 1, tzinfo=UTC), status=TenderStatus.CLOSED,
                        created_by=customer_id)
        active = Tender(title="Active", start_price=6000, current_price=6000, step=100,
                        deadline=datetime(2030, 1, 1, tzinfo=UTC), status=TenderStatus.ACTIVE,
                        created_by=customer_id)
        session.add_all([closed, active])
        session.flush()
        session.add(Bid(tender_id=closed.id, carrier_id=carrier_id, price=8000,
                        idempotency_key="dashboard-bid", is_winner=True))
        session.commit()
        stats = get_dashboard_stats(session)

    assert stats.total_saved == 2000
    assert stats.active_tenders == 1
    assert stats.avg_bids_per_tender == 0.5
    assert len(stats.top_carriers) == 1
    assert stats.top_carriers[0].carrier_id == carrier_id