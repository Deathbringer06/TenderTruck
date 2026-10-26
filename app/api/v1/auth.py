from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.api.deps import get_db
from app.core.security import create_access_token, get_password_hash, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже зарегистрирован")
    if db.query(models.User).filter(models.User.inn == user.inn).first():
        raise HTTPException(status_code=400, detail="Компания с таким ИНН уже зарегистрирована в системе")
    if db.query(models.User).filter(models.User.phone == user.phone).first():
        raise HTTPException(status_code=400, detail="Пользователь с таким телефоном уже зарегистрирован")
    new_user = models.User(
        email=user.email,
        phone=user.phone,
        hashed_password=get_password_hash(user.password),
        role=user.role,
        inn=user.inn,
    )
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Пользователь с такими данными уже зарегистрирован")
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=schemas.Token)
def login(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if user is None or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный email или пароль", headers={"WWW-Authenticate": "Bearer"})
    return {"access_token": create_access_token(str(user.id)), "token_type": "bearer"}
