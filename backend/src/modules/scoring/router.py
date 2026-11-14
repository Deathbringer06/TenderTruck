from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.app.db.engine import get_session
from src.app.deps import get_current_user
from src.modules.auth.models import User
from src.modules.scoring.schemas import ScoreRead
from src.modules.scoring.service import score_company_inn

router = APIRouter(prefix="/scoring", tags=["scoring"])


@router.get("/check", response_model=ScoreRead)
def check_company_score(
    inn: Annotated[str, Query(pattern=r"^\d{10}(\d{2})?$")],
    user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
) -> ScoreRead:
    return ScoreRead.model_validate(score_company_inn(session, user, inn))
