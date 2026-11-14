from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.core.exceptions import ForbiddenError
from src.modules.auth.models import User, UserRole
from src.modules.companies.models import Company
from src.modules.scoring.models import CompanyScore, RiskLevel


def check_inn(inn: str) -> dict[str, str]:
    """Return a stable mock risk assessment in place of an external INN provider."""
    digit_sum = sum(int(digit) for digit in inn)
    risk = (RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH)[digit_sum % 3]
    reasons = {
        RiskLevel.LOW: "Mock check found no elevated risk indicators.",
        RiskLevel.MEDIUM: "Mock check found indicators requiring additional review.",
        RiskLevel.HIGH: "Mock check found elevated risk indicators.",
    }
    return {"risk": risk.value, "reason": reasons[risk]}


def score_company_inn(session: Session, user: User, inn: str) -> dict[str, object]:
    company = session.scalar(select(Company).where(Company.inn == inn))
    if user.role != UserRole.admin and (company is None or company.owner_id != user.id):
        raise ForbiddenError("You may only check your own company")

    result = check_inn(inn)
    checked_at = datetime.now(UTC)
    if company is not None:
        score = CompanyScore(
            company_id=company.id,
            risk_level=RiskLevel(result["risk"]),
            checked_at=checked_at,
        )
        session.add(score)
        session.commit()
        checked_at = score.checked_at or checked_at

    return {
        "company_id": company.id if company is not None else None,
        "inn": inn,
        **result,
        "checked_at": checked_at,
    }
