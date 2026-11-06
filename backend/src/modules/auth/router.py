from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.core.exceptions import UnauthorizedError
from src.app.db.engine import get_session
from src.modules.auth.schemas import Token, UserCreate, UserLogin, UserRead
from src.modules.auth.service import authenticate_user, create_access_token, register_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=201)
def register(data: UserCreate, session: Session = Depends(get_session)) -> UserRead:
    return UserRead.model_validate(register_user(session, data))


@router.post("/login", response_model=Token)
def login(data: UserLogin, session: Session = Depends(get_session)) -> Token:
    user = authenticate_user(session, data.email, data.password)
    if user is None:
        raise UnauthorizedError("Invalid email or password")
    return Token(access_token=create_access_token(user))
