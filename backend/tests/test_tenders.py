from datetime import UTC, datetime, timedelta

from src.app.db.base import Base
from src.app.db.engine import SessionLocal, engine
from src.modules.auth.models import User, UserRole
from src.modules.tenders.schemas import TenderCreate
from src.modules.tenders.service import create_tender


def setup_module() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def test_create_tender() -> None:
    with SessionLocal() as session:
        user = User(
            email="customer@example.com",
            hashed_password="test",
            role=UserRole.customer,
        )
        session.add(user)
        session.commit()
        tender = create_tender(
            session,
            user.id,
            TenderCreate(
                title="Bishkek delivery",
                start_price=10000,
                step=100,
                deadline=datetime.now(UTC) + timedelta(days=1),
            ),
        )
        assert tender.current_price == tender.start_price
