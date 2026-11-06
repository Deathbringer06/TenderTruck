from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.lib.security import create_access_token as create_jwt
from src.app.lib.security import hash_password, verify_password
from src.modules.auth.models import User
from src.modules.auth.schemas import UserCreate


def register_user(session: Session, data: UserCreate) -> User:
    user = User(
        email=str(data.email).lower(),
        hashed_password=hash_password(data.password),
        role=data.role,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate_user(session: Session, email: str, password: str) -> User | None:
    user = session.scalar(select(User).where(User.email == email.lower()))
    if user is None or not user.is_active or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(user: User) -> str:
    return create_jwt(str(user.id), {"role": user.role.value})
