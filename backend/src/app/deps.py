from __future__ import annotations

from collections.abc import Callable
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.core.exceptions import ForbiddenError, UnauthorizedError
from src.app.db.engine import get_session
from src.app.lib.security import decode_access_token
from src.modules.auth.models import User, UserRole

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    session: Session = Depends(get_session),
) -> User:
    if credentials is None:
        raise UnauthorizedError()
    payload = decode_access_token(credentials.credentials)
    if payload is None or payload.get("sub") is None:
        raise UnauthorizedError("Invalid access token")
    try:
        user_id = UUID(str(payload["sub"]))
    except (TypeError, ValueError) as error:
        raise UnauthorizedError("Invalid access token") from error
    user = session.scalar(select(User).where(User.id == user_id))
    if user is None or not user.is_active:
        raise UnauthorizedError()
    return user


def require_role(required_role: UserRole) -> Callable[..., User]:
    def role_dependency(user: User = Depends(get_current_user)) -> User:
        if user.role != required_role and user.role != UserRole.admin:
            raise ForbiddenError()
        return user

    return role_dependency
