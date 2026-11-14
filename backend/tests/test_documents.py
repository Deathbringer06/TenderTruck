import asyncio
import sys
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType
from uuid import uuid4

from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.app.db.base import Base
from src.modules.auth.models import User, UserRole
from src.modules.bids.models import Bid
from src.modules.companies.models import Company
from src.modules.documents.service import generate_contract
from src.modules.tenders.models import Tender, TenderStatus

TEMPLATES = Path(__file__).parents[1] / "src" / "modules" / "documents" / "templates"


def test_contract_template_renders_contract_fields() -> None:
    environment = Environment(
        loader=FileSystemLoader(TEMPLATES), autoescape=select_autoescape(["html"])
    )
    html = environment.get_template("contract.html").render(
        contract={
            "tender_id": "tender-1",
            "tender_title": "Test tender",
            "amount": 12500,
            "customer_name": "Customer",
            "carrier_name": "Carrier",
            "carrier_inn": "1234567890",
        }
    )

    assert "Test tender" in html
    assert "Customer" in html
    assert "Carrier" in html
    assert "12500" in html


def test_act_template_exists() -> None:
    assert (TEMPLATES / "act.html").is_file()


def test_generate_contract_renders_pdf_in_worker_thread(monkeypatch) -> None:
    rendered_html: list[str] = []

    class FakeHTML:
        def __init__(self, *, string: str, base_url: str) -> None:
            rendered_html.append(string)

        def write_pdf(self) -> bytes:
            return b"%PDF-test"

    fake_weasyprint = ModuleType("weasyprint")
    fake_weasyprint.HTML = FakeHTML
    monkeypatch.setitem(sys.modules, "weasyprint", fake_weasyprint)

    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    tender_id = uuid4()
    with Session(engine) as session:
        customer = User(
            email="contract-customer@example.com",
            hashed_password="x",
            role=UserRole.customer,
        )
        carrier = User(
            email="contract-carrier@example.com",
            hashed_password="x",
            role=UserRole.carrier,
        )
        session.add_all([customer, carrier])
        session.flush()
        session.add_all(
            [
                Company(owner_id=customer.id, name="Customer Co", inn="1234567890"),
                Company(owner_id=carrier.id, name="Carrier Co", inn="0987654321"),
            ]
        )
        tender = Tender(
            id=tender_id,
            title="Contract test tender",
            start_price=20000,
            current_price=15000,
            step=100,
            deadline=datetime(2030, 1, 1, tzinfo=UTC),
            status=TenderStatus.CLOSED,
            created_by=customer.id,
        )
        session.add(tender)
        session.flush()
        session.add(
            Bid(
                tender_id=tender.id,
                carrier_id=carrier.id,
                price=15000,
                idempotency_key="contract-test-bid",
                is_winner=True,
            )
        )
        session.commit()

        pdf = asyncio.run(generate_contract(session, tender.id, customer))

    assert pdf == b"%PDF-test"
    assert "Contract test tender" in rendered_html[0]
    assert "Customer Co" in rendered_html[0]
    assert "Carrier Co" in rendered_html[0]
