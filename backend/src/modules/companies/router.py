from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.core.exceptions import ForbiddenError
from src.app.db.engine import get_session
from src.app.deps import get_current_user
from src.modules.auth.models import User, UserRole
from src.modules.companies.schemas import CompanyCreate, CompanyRead, CompanyUpdate
from src.modules.companies.service import create_company, get_company_by_owner, update_company

router = APIRouter(prefix="/companies", tags=["companies"])


def require_company_role(user: Annotated[User, Depends(get_current_user)]) -> User:
    if user.role not in (UserRole.customer, UserRole.carrier, UserRole.admin):
        raise ForbiddenError()
    return user


@router.post("", response_model=CompanyRead, status_code=201)
def create(
    data: CompanyCreate,
    user: Annotated[User, Depends(require_company_role)],
    session: Session = Depends(get_session),
) -> CompanyRead:
    return CompanyRead.model_validate(create_company(session, user.id, data))


@router.get("/me", response_model=CompanyRead)
def get_me(
    user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
) -> CompanyRead:
    return CompanyRead.model_validate(get_company_by_owner(session, user.id))


@router.patch("/me", response_model=CompanyRead)
def update_me(
    data: CompanyUpdate,
    user: Annotated[User, Depends(require_company_role)],
    session: Session = Depends(get_session),
) -> CompanyRead:
    return CompanyRead.model_validate(update_company(session, user.id, data))
