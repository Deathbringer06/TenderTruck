from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import engine, get_db
from app import models, schemas

# Создаем таблицы в БД автоматически при запуске
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="TenderTruck API")

# Утилита для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

@app.get("/")
def read_root():
    return {"message": "Сервер TenderTruck успешно запущен и готов к работе!"}

@app.post("/api/v1/auth/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли пользователь с таким email
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже зарегистрирован"
        )
    
    # Проверяем ИНН
    db_inn = db.query(models.User).filter(models.User.inn == user.inn).first()
    if db_inn:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Компания с таким ИНН уже зарегистрирована в системе"
        )

    hashed_password = get_password_hash(user.password)
    
    new_user = models.User(
        email=user.email,
        phone=user.phone,
        hashed_password=hashed_password,
        role=user.role,
        inn=user.inn
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user