from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from src.app.db.engine import get_session
from src.app.deps import require_role
from src.modules.auth.models import User, UserRole
from src.modules.bids.schemas import BidCreate, BidRead
from src.modules.bids.service import place_bid

router = APIRouter(prefix="/tenders", tags=["bids"])


@router.post("/{tender_id}/bids", response_model=BidRead, status_code=201)
def submit_bid(
    tender_id: UUID,
    data: BidCreate,
    x_idempotency_key: Annotated[str, Header(alias="X-Idempotency-Key")],
    user: Annotated[User, Depends(require_role(UserRole.carrier))],
    session: Session = Depends(get_session),
) -> BidRead:
    bid = place_bid(session, tender_id, user.id, data.price, x_idempotency_key)
    return BidRead.model_validate(bid)
