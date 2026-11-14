from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.app.db.engine import get_session
from src.app.deps import require_role
from src.modules.auth.models import User, UserRole
from src.modules.auto_bids.schemas import AutoBidCreate, AutoBidRead
from src.modules.auto_bids.service import (
    deactivate_auto_bid,
    list_auto_bids,
    place_auto_bid,
)

router = APIRouter(prefix="/auto-bids", tags=["auto-bids"])


@router.post("", response_model=AutoBidRead, status_code=status.HTTP_201_CREATED)
def create_auto_bid(
    data: AutoBidCreate,
    user: Annotated[User, Depends(require_role(UserRole.carrier))],
    session: Session = Depends(get_session),
) -> AutoBidRead:
    return AutoBidRead.model_validate(
        place_auto_bid(session, data.tender_id, user.id, data.min_price, data.step)
    )


@router.get("/me", response_model=list[AutoBidRead])
def get_my_auto_bids(
    user: Annotated[User, Depends(require_role(UserRole.carrier))],
    session: Session = Depends(get_session),
) -> list[AutoBidRead]:
    return [AutoBidRead.model_validate(item) for item in list_auto_bids(session, user.id)]


@router.delete("/{auto_bid_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_auto_bid(
    auto_bid_id: UUID,
    user: Annotated[User, Depends(require_role(UserRole.carrier))],
    session: Session = Depends(get_session),
) -> Response:
    deactivate_auto_bid(session, auto_bid_id, user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
