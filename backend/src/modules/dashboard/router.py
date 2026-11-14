from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.db.engine import get_session
from src.app.deps import require_role
from src.modules.auth.models import User, UserRole
from src.modules.dashboard.schemas import DashboardStats
from src.modules.dashboard.service import get_dashboard_stats

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStats)
def dashboard_stats(
    _user: Annotated[User, Depends(require_role(UserRole.customer))],
    session: Session = Depends(get_session),
) -> DashboardStats:
    return get_dashboard_stats(session)
