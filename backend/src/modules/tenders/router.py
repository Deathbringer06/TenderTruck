from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.db.engine import get_session
from src.app.deps import require_role
from src.modules.auth.models import User, UserRole
from src.modules.tenders.schemas import TenderCreate, TenderRead
from src.modules.tenders.service import close_tender, create_tender, get_tender, list_tenders

router = APIRouter(prefix="/tenders", tags=["tenders"])


@router.post("", response_model=TenderRead, status_code=201)
def create(
    data: TenderCreate,
    user: Annotated[User, Depends(require_role(UserRole.customer))],
    session: Session = Depends(get_session),
) -> TenderRead:
    return TenderRead.model_validate(create_tender(session, user.id, data))


@router.get("", response_model=list[TenderRead])
def list_all(session: Session = Depends(get_session)) -> list[TenderRead]:
    return [TenderRead.model_validate(tender) for tender in list_tenders(session)]


@router.get("/{tender_id}", response_model=TenderRead)
def get(tender_id: UUID, session: Session = Depends(get_session)) -> TenderRead:
    return TenderRead.model_validate(get_tender(session, tender_id))


@router.patch("/{tender_id}/close", response_model=TenderRead)
def close(
    tender_id: UUID,
    user: Annotated[User, Depends(require_role(UserRole.customer))],
    session: Session = Depends(get_session),
) -> TenderRead:
    return TenderRead.model_validate(close_tender(session, tender_id))
