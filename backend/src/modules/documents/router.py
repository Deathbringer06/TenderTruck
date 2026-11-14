from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from src.app.db.engine import get_session
from src.app.deps import require_role
from src.modules.auth.models import User, UserRole
from src.modules.documents.service import generate_contract

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/tenders/{tender_id}/contract.pdf")
async def download_contract(
    tender_id: UUID,
    user: Annotated[User, Depends(require_role(UserRole.customer))],
    session: Session = Depends(get_session),
) -> StreamingResponse:
    pdf = await generate_contract(session, tender_id, user)
    return StreamingResponse(
        iter([pdf]),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="contract-{tender_id}.pdf"'},
    )
