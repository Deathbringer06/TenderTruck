from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.api.deps import get_current_user, get_db

router = APIRouter(prefix="/tenders", tags=["tenders"])


def _require_role(user: models.User, role: models.UserRole) -> None:
    if user.role != role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")


def _get_tender_or_404(tender_id: int, db: Session) -> models.Tender:
    tender = db.query(models.Tender).filter(models.Tender.id == tender_id).first()
    if tender is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тендер не найден")
    return tender


@router.post("", response_model=schemas.TenderResponse, status_code=status.HTTP_201_CREATED)
def create_tender(
    payload: schemas.TenderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    _require_role(current_user, models.UserRole.ZAKAZCHIK)
    loading_date = payload.loading_date
    now = datetime.now(timezone.utc) if loading_date.tzinfo else datetime.utcnow()
    if loading_date < now:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Дата погрузки не может быть в прошлом")

    tender = models.Tender(
        **payload.model_dump(),
        customer_id=current_user.id,
        status="open",
    )
    db.add(tender)
    db.commit()
    db.refresh(tender)
    return tender


@router.get("/my", response_model=list[schemas.TenderResponse])
def get_my_tenders(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    _require_role(current_user, models.UserRole.ZAKAZCHIK)
    return (
        db.query(models.Tender)
        .filter(models.Tender.customer_id == current_user.id)
        .order_by(models.Tender.created_at.desc())
        .all()
    )


@router.get("/open", response_model=list[schemas.TenderResponse])
def get_open_tenders(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    _require_role(current_user, models.UserRole.PEREVOZCHIK)
    return (
        db.query(models.Tender)
        .filter(models.Tender.status == "open")
        .order_by(models.Tender.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.get("/{tender_id}", response_model=schemas.TenderResponse)
def get_tender(
    tender_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    tender = _get_tender_or_404(tender_id, db)
    if current_user.id != tender.customer_id and current_user.role != models.UserRole.PEREVOZCHIK:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    return tender


@router.patch("/{tender_id}", response_model=schemas.TenderResponse)
def update_tender(
    tender_id: int,
    payload: schemas.TenderUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    tender = _get_tender_or_404(tender_id, db)
    if current_user.id != tender.customer_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    if tender.status != "open":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Можно изменять только открытый тендер")

    changes = payload.model_dump(exclude_unset=True)
    required_fields = {"point_a", "point_b", "loading_date", "start_price", "status"}
    if any(field in changes and changes[field] is None for field in required_fields):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Обязательное поле не может быть null")
    if "loading_date" in changes:
        loading_date = changes["loading_date"]
        now = datetime.now(timezone.utc) if loading_date.tzinfo else datetime.utcnow()
        if loading_date < now:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Дата погрузки не может быть в прошлом")

    for field, value in changes.items():
        setattr(tender, field, value)
    db.commit()
    db.refresh(tender)
    return tender


@router.delete("/{tender_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tender(
    tender_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    tender = _get_tender_or_404(tender_id, db)
    if current_user.id != tender.customer_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    db.delete(tender)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
