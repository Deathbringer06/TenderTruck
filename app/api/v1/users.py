from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.api.deps import get_current_user, get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=schemas.UserProfile)
def read_current_user(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=schemas.UserProfile)
def update_current_user(update: schemas.UserProfileUpdate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Пользователь с таким телефоном уже зарегистрирован")
    db.refresh(current_user)
    return current_user
