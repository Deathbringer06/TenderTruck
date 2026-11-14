import asyncio
from pathlib import Path
from uuid import UUID

from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.core.exceptions import ForbiddenError, NotFoundError, ValidationError
from src.modules.auth.models import User, UserRole
from src.modules.bids.models import Bid
from src.modules.companies.models import Company
from src.modules.documents.schemas import ContractData
from src.modules.tenders.models import Tender

TEMPLATE_DIR = Path(__file__).parent / "templates"
_templates = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html"]),
)


async def generate_contract(session: Session, tender_id: UUID, user: User) -> bytes:
    tender = session.get(Tender, tender_id)
    if tender is None:
        raise NotFoundError("Tender not found")
    if user.role != UserRole.admin and tender.created_by != user.id:
        raise ForbiddenError("You may only download contracts for your tenders")
    winner = session.scalar(
        select(Bid).where(Bid.tender_id == tender_id, Bid.is_winner.is_(True))
    )
    if winner is None:
        raise ValidationError("Tender has no winning bid")
    customer = session.scalar(select(Company).where(Company.owner_id == tender.created_by))
    carrier = session.scalar(select(Company).where(Company.owner_id == winner.carrier_id))
    if customer is None or carrier is None:
        raise ValidationError("Customer or carrier company details are missing")

    data = ContractData(
        tender_id=tender.id,
        tender_title=tender.title,
        amount=winner.price,
        customer_name=customer.name,
        carrier_name=carrier.name,
        carrier_inn=carrier.inn,
    )
    template = _templates.get_template("contract.html")
    html = template.render(contract=data.model_dump())

    def render_pdf() -> bytes:
        from weasyprint import HTML

        return HTML(string=html, base_url=str(TEMPLATE_DIR)).write_pdf()

    return await asyncio.to_thread(render_pdf)
